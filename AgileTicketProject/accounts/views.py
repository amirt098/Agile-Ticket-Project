import logging

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from runner.bootstraper import get_bootstrapper
from . import dataclasses, exceptions
from .forms import CreateOrganizationForm, AgentForm, UserForm
from .models import User

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'base.html')


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Thank you for visiting us.')
        return redirect('login')


class LoginView(View):
    template_name = 'accounts/agent_login.html'
    service = get_bootstrapper().get_account_service()

    def get(self, request, ):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = self.service.login_with_username_and_password(username, password, request)
            request.session['is_agent'] = user.is_agent
            request.session['organization'] = user.organization.name
            messages.success(request, f'Wellcome: {user.get_full_name()}')
            return render(request, 'base.html', {'user': user})
        except exceptions.LoginFailed as e:
            messages.error(request, f'{str(e)}')
            return render(request, self.template_name)
        except Exception as e:
            messages.error(request, f'Error Login: {str(e)}')
            return render(request, self.template_name)


class ModifyUserView(LoginRequiredMixin, View):
    service = get_bootstrapper().get_account_service()

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = UserForm(instance=user)
        return render(request, 'accounts/modify_user.html', {'form': form, 'user': user})

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            try:
                user = dataclasses.User(**form.cleaned_data)
                result = self.service.modify_user(user)
                messages.success(request, f'User modified successfully: {result.username}')
                return redirect('profile')

            except Exception as e:
                messages.error(request, f'Error Modify user: {e}')
                return render(request, 'accounts/modify_user.html', {'form': form, 'user': user})
        return render(request, 'accounts/modify_user.html', {'form': form, 'user': user})


class ModifyAgentView(LoginRequiredMixin, View):
    service = get_bootstrapper().get_account_service()

    def get(self, request, agent_id):
        agent = get_object_or_404(User, id=agent_id, is_agent=True)
        form = AgentForm(instance=agent)
        return render(request, 'accounts/modify_agent.html', {'form': form, 'agent': agent})

    def post(self, request, agent_id):
        agent = get_object_or_404(User, id=agent_id, is_agent=True)
        form = AgentForm(request.POST, instance=agent)
        if form.is_valid():
            try:
                agent = dataclasses.Agent(**form.cleaned_data)
                self.service.modify_agent(agent)
                messages.success(request, "Agent modified successfully.")
                return redirect('profile')
            except Exception as e:
                messages.error(request, f'Error modify user: {str(e)}')
        return render(request, 'accounts/modify_agent.html', {'form': form, 'agent': agent})


class CreateAgentView(View):
    service = get_bootstrapper().get_account_service()

    def get(self, request):
        form = AgentForm()
        organization_name = self.request.session.get('organization')
        return render(request, 'accounts/create_agent.html', {'form': form, 'organization': organization_name})

    def post(self, request):
        form = AgentForm(request.POST)
        if form.is_valid():
            try:
                agent = dataclasses.Agent(**form.cleaned_data)
                organization_name = self.request.session.get('organization')
                agent.organization = organization_name
                agent.is_agent = True
                self.service.create_user(agent)
                messages.success(request, f'Agent: {agent.username}'
                                          f' created Success Fully for organization {organization_name}')
                return redirect('login')

            except Exception as e:
                messages.error(request, f"Error during user creation: {e}")
                return redirect('login')
        return render(request, 'accounts/create_agent.html', {'form': form})


class CreateUserView(View):
    service = get_bootstrapper().get_account_service()

    def get(self, request):
        form = UserForm()
        return render(request, 'accounts/create_user.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_agent = False

            try:
                result = self.service.create_user(user)
                messages.success(request, f'User: {result.username} Created Success Fully.')
                return redirect('profile')
            except Exception as e:
                messages.error(request, f"Error during user creation: {e}")
                return redirect('register_user')

        return render(request, 'accounts/create_user.html', {'form': form})


class CreateOrganizationView(View):
    template_name = 'accounts/create_organization.html'
    service = get_bootstrapper().get_account_service()
    organization_form = CreateOrganizationForm

    def get(self, request):
        form = self.organization_form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.organization_form(request.POST)
        if form.is_valid():
            try:
                organization_data = dataclasses.Organization(**form.cleaned_data)
                result = self.service.create_organization(organization_data)
                request.session['organization'] = result.name
                messages.success(request, f'Organization {result.name} created success fully.')
                return redirect('register_agent')
            except Exception as e:
                messages.error(request, f"Error during organization creation: {e}")
                return redirect('register_organization')
        else:
            return render(request, self.template_name, {'form': form})


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        logger.info(f'profile: {user}')
        if user.is_agent:
            return render(request, 'accounts/agent_profile.html', {'agent': user})
        return render(request, 'accounts/user_profile.html', {'user': user})


class AgentManagementView(LoginRequiredMixin, View):
    template_name = 'accounts/agent_management.html'
    accounts_service = get_bootstrapper().get_account_service()

    def get(self, request, *args, **kwargs):
        users = self.accounts_service.get_agents(request.user)
        create_form = AgentForm()
        modify_form = AgentForm()
        return render(request, self.template_name,
                      {'users': users, 'create_form': create_form, 'modify_form': modify_form})

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', '')
        if action == 'create_user':
            return self.create_user(request)
        elif action == 'modify_user':
            return self.modify_user(request)
        else:
            messages.error(request, 'Invalid action.')
            return redirect('user_management')

    def create_user(self, request):
        create_form = AgentForm(request.POST)
        if create_form.is_valid():
            user_data = create_form.cleaned_data
            try:
                self.accounts_service.create_user(user_data)
                messages.success(request, 'User created successfully.')
            except Exception as e:
                messages.error(request, f'Error creating user: {e}')
        else:
            messages.error(request, 'Invalid form submission for user creation.')

        return redirect('user_management')

    def modify_user(self, request):
        modify_form = AgentForm(request.POST)
        if modify_form.is_valid():
            user_data = modify_form.cleaned_data
            try:
                self.accounts_service.modify_agent(user_data)
                messages.success(request, 'User modified successfully.')
            except Exception as e:
                messages.error(request, f'Error modifying user: {e}')
        else:
            messages.error(request, 'Invalid form submission for user modification.')

        return redirect('user_management')


class AboutUsView(View):
    def get(self, request):
        return render(request, 'about_us.html')


class OrganizationListView(LoginRequiredMixin, View):
    service = get_bootstrapper().get_account_service()

    def get(self, request):
        user = request.user
        organizations = self.service.get_organizations(user)
        return render(request, 'accounts/organization_list.html', {'organizations': organizations})
