import logging

from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404

from .models import User, Agent, Role, Organization
from . import dataclasses
from . import interfaces
from . import exceptions

logger = logging.getLogger(__name__)


class AccountsService(interfaces.AbstractAccountsService):

    def get_user_profile(self, user):
        try:
            if isinstance(user, Agent):
                return Agent.objects.get(pk=user.pk)
            elif isinstance(user, User):
                return user
        except Agent.DoesNotExist:
            # Handle the case where the agent does not exist
            return None

    def login_with_username_and_password(self, username, password, request):
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return user
            else:
                logger.warning(f"User {username} is not active.")
                raise exceptions.LoginFailed("User is not active.")
        else:
            # Check if the user is an Agent
            agent = get_object_or_404(Agent, username=username)
            if agent.check_password(password):
                if agent.is_active:
                    login(request, agent)
                    return agent
                else:
                    logger.warning(f"Agent {username} is not active.")
                    raise exceptions.LoginFailed("Agent is not active.")
            else:
                logger.info(f"Invalid credentials for user or agent {username}.")
                raise exceptions.LoginFailed("Invalid credentials.")

    def modify_user(self, user_data: dataclasses.User):
        logger.info(f'user: {user_data}')
        try:
            user = User.objects.get(username=user_data.username)
            if user_data.first_name:
                user.first_name = user_data.first_name
            if user_data.last_name:
                user.last_name = user_data.last_name
            if user_data.email:
                user.email = user_data.email
            if user_data.password:
                user.set_password(user_data.password)
            user.save()
            logger.info(f"User {user.username} modified successfully.")
            result = self._convert_user_to_data_class(user)
            logger.info(f"result: {result}")
            return result
        except User.DoesNotExist:
            logger.warning(f"User {user_data.username} does not exist.")
            raise exceptions.UserNotFound()
        except Exception as e:
            logger.error(f"Error during user modification: {e}", exc_info=True)
            raise e

    def modify_agent(self, agent_data: dataclasses.Agent):
        try:
            agent = Agent.objects.get(username=agent_data.username)
            if agent_data.first_name:
                agent.first_name = agent_data.first_name
            if agent_data.last_name:
                agent.last_name = agent_data.last_name
            if agent_data.email:
                agent.email = agent_data.email
            if agent_data.organization:
                org = Organization.objects.get(name=agent_data.organization)
                agent.organization = org
            created = False
            if agent_data.role:
                role, created = Role.objects.get_or_create(
                    name=agent_data.role.name,
                    defaults={
                        "description": agent_data.role.description})
                agent.role = role
            if agent_data.password:
                agent.set_password(agent_data.password)
            agent.save()
            logger.info(f"Agent {agent.username} modified successfully.")

            if created:
                logger.info(f"Role: {role}, created.")
            result = self._convert_agent_to_data_class(agent)
            logger.info(f"result: {result}")
            return result
        except Organization.DoesNotExist:
            raise exceptions.OrganizationNotFound()
        except Agent.DoesNotExist:
            logger.warning(f"Agent {agent_data.username} does not exist.")
            raise exceptions.UserNotFound()
        except Exception as e:
            logger.error(f"Error during agent modification: {e}", exc_info=True)
            raise e

    def create_agent(self, agent_data: dataclasses.Agent):
        try:
            organization = Organization.objects.get(name=agent_data.organization)
            agent = Agent.objects.create(username=agent_data.username, organization=organization)
            agent.set_password(agent_data.password)
            if agent_data.role:
                role, created = Role.objects.get_or_create(
                    name=agent_data.role.name,
                    defaults={
                        "description": agent_data.role.description})
                agent.role = role
            if agent_data.email:
                agent.email = agent_data.email
            if agent_data.first_name:
                agent.first_name = agent_data.first_name
            if agent_data.last_name:
                agent.last_name = agent_data.last_name
            agent.save()
            logger.info(f"Agent {agent.username} created successfully.")
            result = self._convert_agent_to_data_class(agent)
            logger.info(f"result: {result}")
            return result
        except Organization.DoesNotExist:
            logger.warning(f"Organization with name {agent_data.organization} does not exist.")
            raise exceptions.OrganizationNotFound()
        except Exception as e:
            logger.error(f"Error during agent creation: {e}", exc_info=True)
            raise e

    def create_user(self, user_data: dataclasses.User):
        try:
            logger.info(f'user_data: {user_data}')
            user = User.objects.create(username=user_data.username)
            user.set_password(user_data.password)
            if user_data.email:
                user.email = user_data.email
            if user_data.first_name:
                user.first_name = user_data.first_name
            if user_data.last_name:
                user.last_name = user_data.last_name
            user.save()
            logger.info(f"User {user.username} created successfully.")
            logger.info(f"User {user.username} returned")
            return self._convert_user_to_data_class(user)
        except Exception as e:
            logger.error(f"Error during user creation: {e}", exc_info=True)
            raise e

    def create_organization(self, organization_data: dataclasses.Organization) -> dataclasses.Organization:
        try:
            if Organization.objects.filter(name=organization_data.name).exists():
                logger.warning(f'Organization Name: {organization_data.name} is Duplicated!')
                raise exceptions.OrganizationNotFound()

            organization = Organization(**vars(organization_data))
            # vars convert dataclass to dictionary
            organization.save()
            logger.info(f"Organization {organization.name} created successfully.")
            result = self._convert_organization_to_data_class(organization)
            logger.info(f"result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error during organization creation: {e}", exc_info=True)
            raise e

    def modify_organization(self, organization_data: dataclasses.Organization):
        try:
            organization = Organization.objects.get(name=organization_data.name)
            if organization_data.address:
                organization.address = organization_data.address
            if organization_data.phone:
                organization.phone = str(organization_data.phone)
            if organization_data.description:
                organization.description = organization_data.description
            organization.save()
            logger.info(f"Organization {organization.name} modified successfully.")
            result = self._convert_organization_to_data_class(organization)
            logger.info(f"result: {result}")
        except Organization.DoesNotExist:
            logger.warning(f"Organization {organization_data.name} does not exist.")
            raise exceptions.OrganizationNotFound()
        except Exception as e:
            logger.error(f"Error during organization modification: {e}", exc_info=True)
            raise e

    def create_role(self, role_data: dataclasses.Role):
        logger.info(f'role data: {role_data}')
        try:
            role = Role.objects.create(
                name=role_data.name
            )
            if role_data.description:
                role.description = role_data.description
            if role_data.organization:
                organization = Organization.objects.get(name=role_data.organization)
                role.organization = organization
            role.save()
            logger.info(f"Role {role.name} created successfully in organization {organization.name}.")
            result = self._convert_role_to_data_class(role)
            logger.info(f"result: {result}")
        except Organization.DoesNotExist:
            logger.warning(f"Organization with Name {role_data.organization} does not exist.")
            raise exceptions.OrganizationNotFound()
        except Exception as e:
            logger.error(f"Error during role creation: {e}", exc_info=True)
            raise e

    def change_agent_role(self, role_data: dataclasses.Role, agent_data: dataclasses.Agent):
        try:
            agent = Agent.objects.get(username=agent_data.username)
            # if not role_data or not agent_data:
            #     logger.info(f'Did not provided essential data.')
            #     raise exceptions.NotProvidedData()
            role, created = Role.objects.get_or_create(
                name=role_data.name,
                defaults={
                    "description": role_data.description})
            agent.role = role
            agent.save()
            logger.info(f"Role of Agent {agent.username} changed to {role.name} successfully.")
            result = self._convert_agent_to_data_class(agent)
            logger.info(f"result: {result}")
        except Agent.DoesNotExist:
            logger.warning(f"Agent with username {agent_data.username} does not exist.")
            raise exceptions.UserNotFound()
        except Exception as e:
            logger.error(f"Error during changing agent role: {e} ", exc_info=True)
            raise e

    @staticmethod
    def _convert_user_to_data_class(user: User) -> dataclasses.User:
        return dataclasses.User(
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )

    @staticmethod
    def _convert_organization_to_data_class(org: Organization) -> dataclasses.Organization:
        return dataclasses.Organization(
            name=org.name,
            description=org.description,
            address=org.address,
            phone=int(org.phone) if org.phone else None,
        )

    def _convert_agent_to_data_class(self, agent: Agent) -> dataclasses.Agent:
        return dataclasses.Agent(
            username=agent.username,
            first_name=agent.first_name,
            last_name=agent.last_name,
            email=agent.email,
            organization=agent.organization.name if agent.organization else None,
            role=self._convert_role_to_data_class(agent.role) if agent.role else None
        )

    @staticmethod
    def _convert_role_to_data_class(role: Role) -> dataclasses.Role:
        return dataclasses.Role(
            name=role.name,
            description=role.description,
        )
