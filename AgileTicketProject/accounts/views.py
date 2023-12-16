from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .dataclasses import Organization, Agent
from runner.bootstraper import get_bootstrapper
from . import dataclasses, exceptions
from .forms import create_dataclass_form, CreateUserForm, CreateOrganizationForm, UserProfileForm, \
    AgentProfileForm, AgentForm, UserForm
import logging

from .models import User

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'base.html')


# class UserLoginView(LoginView):
#     template_name = 'accounts/user_login.html'
#     redirect_authenticated_user = True
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['user_type'] = 'user'
#         return context


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('login')


class LoginView(View):
    template_name = 'accounts/agent_login.html'
    service = get_bootstrapper().get_account_service()

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = self.service.login_with_username_and_password(username, password, request)
            return render(request, 'base.html', {'user': user, 'messages:': [f'Wellcome: {user.get_full_name()}']})
        except exceptions.LoginFailed as e:
            return render(request, self.template_name, {'error': str(e)})
        except Exception as e:
            logger.info(f"error: {e}")
            return render(request, self.template_name, {'error': str(e)})


class ModifyUserView(View):
    @login_required
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = UserForm(instance=user)
        return render(request, 'modify_user.html', {'form': form, 'user': user})

    @login_required
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('accounts/user_profile')  # Adjust the redirect URL as needed
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
            agent = form.save(commit=False)
            self.service.modify_agent(agent)
            return redirect('profile')
        return render(request, 'accounts/modify_agent.html', {'form': form, 'agent': agent})


class CreateAgentView(View):
    service = get_bootstrapper().get_account_service()

    def get(self, request):
        form = AgentForm()
        return render(request, 'accounts/create_agent.html', {'form': form})

    def post(self, request):
        form = AgentForm(request.POST)
        if form.is_valid():
            agent = form.save(commit=False)
            agent.is_agent = True
            self.service.create_user(agent)

            return redirect('login')
        return render(request, 'accounts/create_agent.html', {'form': form})


class CreateUserView(View):
    @login_required
    def get(self, request):
        form = UserForm()
        return render(request, 'accounts/create_user.html', {'form': form})

    @login_required
    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts/user_profile')  # Adjust the redirect URL as needed
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
                # Create dataclass instance using **kwargs
                organization_data = dataclasses.Organization(**form.cleaned_data)
                result = self.service.create_organization(organization_data)
                return render(request, 'base.html', {'messages': [f'Organization {result.name} created successfully.']})
            except Exception as e:
                logger.error(f"Error during organization creation: {e}", exc_info=True)
                return HttpResponse(f"Error during organization creation: {e}")
        else:
            return render(request, self.template_name, {'form': form})


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        print(request)
        print(request.user)
        user = request.user
        logger.info(f'profile: {user}')
        if user.is_agent:
            return render(request, 'accounts/agent_profile.html', {'agent': user})
        return render(request, 'accounts/user_profile.html', {'user': user})


class AgentManagementView(View):
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
            return redirect('user_management')  # Redirect to the user management page

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

        return redirect('user_management')  # Redirect to the user management page

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
