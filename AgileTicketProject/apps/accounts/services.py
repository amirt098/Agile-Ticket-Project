import logging
from .models import User, Agent, Role, Organization
from . import dataclasses
from . import interfaces
from . import exceptions

logger = logging.getLogger(__name__)


class AccountsService(interfaces.AbstractAccountsService):

    def login_with_username_and_password(self, username, password):

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            logger.warning(f"User {username} does not exist.")
            raise exceptions.LoginFailed()

        except Exception as e:
            logger.error(f"Error during login: {e}", exc_info=True)
        if user.check_password(password):
            logger.info(f"User {username} logged in successfully.")
            # Todo:!!!
        else:
            logger.info(f"Invalid password for user {username}.")
            raise exceptions.LoginFailed()

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
        except Organization.DoesNotExist:
            logger.warning(f"Organization with name {agent_data.organization} does not exist.")
            raise exceptions.OrganizationNotFound()
        except Exception as e:
            logger.error(f"Error during agent creation: {e}", exc_info=True)

    def create_organization(self, organization_data: dataclasses.Organization):
        try:
            if Organization.objects.filter(name=organization_data.name).exists():
                logger.warning(f'Organization Name: {organization_data.name} is Duplicated!')
                raise exceptions.OrganizationNotFound()

            organization = Organization(**vars(organization_data))
            # vars convert dataclass to dictionary
            organization.save()
            logger.info(f"Organization {organization.name} created successfully.")
        except Exception as e:
            logger.error(f"Error during organization creation: {e}", exc_info=True)
            raise e

    def modify_organization(self, organization_data: dataclasses.Organization):
        try:
            organization = Organization.objects.get(name=organization_data.name)
            if organization_data.Address:
                organization.Address = organization_data.Address
            if organization_data.phone:
                organization.phone = str(organization_data.phone)
            if organization_data.description:
                organization.description = organization_data.description
            organization.save()
            logger.info(f"Organization {organization.name} modified successfully.")
        except Organization.DoesNotExist:
            logger.warning(f"Organization {organization_data.name} does not exist.")
            raise exceptions.OrganizationNotFound()
        except Exception as e:
            logger.error(f"Error during organization modification: {e}", exc_info=True)

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
        except Organization.DoesNotExist:
            logger.warning(f"Organization with Name {role_data.organization} does not exist.")
            raise exceptions.OrganizationNotFound()
        except Exception as e:
            logger.error(f"Error during role creation: {e}", exc_info=True)

    def change_agent_role(self, role_data: dataclasses.Role, agent_data: dataclasses.Agent):
        try:
            agent = Agent.objects.get(uid=agent_data.username)
            role = Role.objects.get(uid=role_data.name)
            agent.role = role
            agent.save()
            logger.info(f"Role of Agent {agent.username} changed to {role.name} successfully.")
        except Agent.DoesNotExist:
            logger.warning(f"Agent with username {agent_data.username} does not exist.")
            raise exceptions.UserNotFound()
        except Role.DoesNotExist:
            logger.warning(f"Role with name {role_data.name} does not exist.")
            raise exceptions.RoleNotFound()
        except Exception as e:
            logger.error(f"Error during changing agent role: {e} ", exc_info=True)
