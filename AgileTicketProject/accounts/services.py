import logging

from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import get_object_or_404

from .models import User, Role, Organization
from . import dataclasses
from . import interfaces
from . import exceptions

logger = logging.getLogger(__name__)


class AccountsService:

    def login_with_username_and_password(self, username, password, request):
        logger.info(f'username: {username}, password: {password}')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            logger.info('invalid user name')
            raise exceptions.LoginFailed()
        if not user.check_password(password):
            logger.info('invalid password')
            raise exceptions.LoginFailed()

        logger.info(f'user: {user}')
        if user.is_active:
            login(request, user)
            logger.info(f'login user: {user}')
            return user
        else:
            logger.warning(f"User {username} is not active.")
            raise exceptions.LoginFailed()

    def get_agents(self, agent):
        logger.info(f'agent: {agent}')
        if not agent.is_agent:
            raise Exception('You do not have Permission to do this')
        agents = User.objects.filter(organization=agent.organization)
        result = agents
        logger.info(f'agents: {agents}')
        return result

    def get_user_profile(self, user):
        user_model = get_user_model()

        try:
            if isinstance(user, user_model):
                return user
        except user_model.DoesNotExist:
            # Handle the case where the user does not exist
            return None

    def modify_user(self, user_data: dataclasses.User):
        return self._modify_user(user_data)

    def modify_agent(self, agent_data: dataclasses.Agent):
        return self._modify_user(agent_data)

    def _modify_user(self, data):
        try:
            user = get_object_or_404(User, username=data.username)

            if data.first_name:
                user.first_name = data.first_name
            if data.last_name:
                user.last_name = data.last_name
            if data.email:
                user.email = data.email
            if data.password:
                user.set_password(data.password)

            if user.is_agent:
                if data.organization:
                    org = get_object_or_404(Organization, name=data.organization)
                    user.organization = org
                if data.role:
                    role, _ = Role.objects.get_or_create(
                        name=data.role.name,
                        defaults={"description": data.role.description}
                    )
                    user.role = role

            user.save()
            logger.info(f"User {user.username} modified successfully.")

            result = self._convert_user_to_data_class(user)
            logger.info(f"result: {result}")
            return result
        except User.DoesNotExist:
            raise exceptions.UserNotFound()
        except (Organization.DoesNotExist, Role.DoesNotExist):
            raise exceptions.OrganizationOrRoleNotFound()
        except Exception as e:
            logger.error(f"Error during user modification: {e}", exc_info=True)
            raise e

    def create_user(self, user_data):
        logger.info(f'user_data: {user_data}')
        try:
            organization = get_object_or_404(Organization, name=user_data.organization)

            if User.objects.filter(username=user_data.username).exists():
                logger.info(f'user name is duplicated.')
                raise exceptions.DuplicatedUsername()

            user = User.objects.create(username=user_data.username, organization=organization,
                                       is_agent=user_data.is_agent)
            user.set_password(user_data.password)

            if user_data.email:
                user.email = user_data.email
            if user_data.first_name:
                user.first_name = user_data.first_name
            if user_data.last_name:
                user.last_name = user_data.last_name

            if user.is_agent:
                if user_data.role:
                    role, _ = Role.objects.get_or_create(
                        name=user_data.role.name,
                        defaults={"description": user_data.role.description}
                    )
                    user.role = role

            user.save()
            logger.info(f"User {user.username} created successfully.")

            result = self._convert_user_to_data_class(user)
            logger.info(f"result: {result}")
            return result
        except Organization.DoesNotExist:
            raise exceptions.OrganizationNotFound()
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
            agent = User.objects.get(username=agent_data.username)
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
        except User.DoesNotExist:
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

    def _convert_agent_to_data_class(self, agent: User) -> dataclasses.Agent:
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
