from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from .dataclasses import Organization
from runner.bootstraper import get_bootstrapper
from . import dataclasses, exceptions
from .forms import create_dataclass_form, CreateUserForm, CreateAgentForm, CreateOrganizationForm
import logging

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'base.html')


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'  # Replace with your actual template name
    success_url = 'home'  # Replace with the URL name or path where the user should be redirected after login


class CreateUserView(View):
    template_name = 'accounts/create_user.html'
    accounts_service = get_bootstrapper().get_account_service()
    form_class = CreateUserForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # user_data = dataclasses.User(
            #     username=form.cleaned_data['username'],
            #     password=form.cleaned_data['password'],
            #     first_name=form.cleaned_data.get('first_name', ''),
            #     last_name=form.cleaned_data.get('last_name', ''),
            #     email=form.cleaned_data.get('email', ''),
            # )
            user_data = dataclasses.User(**form.cleaned_data)
            try:
                result = self.accounts_service.create_user(user_data)
                return HttpResponse(f"User {result.username} created successfully.")
            except Exception as e:
                logger.error(f"Error during user creation: {e}", exc_info=True)
                return HttpResponse(f"Error during user creation: {e}")
        else:
            return render(request, self.template_name, {'form': form})


class CreateAgentView(View):
    template_name = 'accounts/create_agent.html'
    accounts_service = get_bootstrapper().get_account_service()
    agent_form = CreateAgentForm

    def get(self, request):
        form = self.agent_form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.agent_form(request.POST)
        if form.is_valid():
            try:
                # Extract relevant form data
                agent_data = dataclasses.Agent(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    first_name=form.cleaned_data.get('first_name', ''),
                    last_name=form.cleaned_data.get('last_name', ''),
                    email=form.cleaned_data.get('email', ''),
                    organization=form.cleaned_data['organization'],
                    role=dataclasses.Role(
                        name=form.cleaned_data.get('role_name', ''),
                        description=form.cleaned_data.get('role_description', '')
                    ) if form.cleaned_data.get('role_name') else None
                )

                # Create agent using the service
                result = self.accounts_service.create_agent(agent_data)

                return HttpResponse(f"Agent {result.username} created successfully.")
            except Organization.DoesNotExist:
                logger.warning(f"Organization with name {form.cleaned_data['organization']} does not exist.")
                raise exceptions.OrganizationNotFound()
            except Exception as e:
                logger.error(f"Error during agent creation: {e}", exc_info=True)
                return HttpResponse(f"Error during agent creation: {e}")
        else:
            return render(request, self.template_name, {'form': form})


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
                return HttpResponse(f"Organization {result.name} created successfully.")
            except Exception as e:
                logger.error(f"Error during organization creation: {e}", exc_info=True)
                return HttpResponse(f"Error during organization creation: {e}")
        else:
            return render(request, self.template_name, {'form': form})
