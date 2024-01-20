import abc
from . import dataclasses


class AbstractAccountsService(abc.ABC):
    """Abstract base class for accounts services."""

    @abc.abstractmethod
    def login_with_username_and_password(self, username, password):
        """
        Log in a user using their username and password.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Raises:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def modify_user(self, user):
        """
        Modify user information.

        Args:
            user: User information.

        Raises:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def modify_agent(self, user):
        """
        Modify agent information.

        Args:
            user: Agent information.

        Raises:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def create_agent(self, user):
        """
        Create a new agent.

        Args:
            user: Agent information.

        Raises:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def create_organization(self, organization: dataclasses.Organization):
        """
        Create a new organization.

        Args:
            organization (dataclasses.Organization): Organization information.

        Raises:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def modify_organization(self, organization: dataclasses.Organization):
        """
        Modify organization information.

        Args:
            organization (dataclasses.Organization): Organization information.

        Raises:
        """
        raise NotImplementedError

