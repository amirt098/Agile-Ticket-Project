import abc
from dataclasses import dataclass

# Todo: add dataclasses of Role, User, Product, Ticket, ...


class AbstractTicketServices(abc.ABC):
    """
    Abstract base class for managing tickets and related operations.
    """

    def create_product(self, user, product):
        """
        Create a new product.

        Args:
            user (User): The user associated with the ticket.
            product (Product): The product object to be created.

        Raises:
            NotImplementedError: If the method is not implemented in a concrete subclass.
        """
        raise NotImplementedError

    def modify_product(self, user, product,):
        """
        Modify an existing product.

        Args:
            user (User): The user associated with the product.
            product (Ticket): The product object to be modified.

        Raises:
            NotImplementedError: If the method is not implemented in a concrete subclass.

        """
        raise NotImplementedError

    def create_ticket(self, user, ticket):
        """
        Create a new ticket.

        Args:
            user (User): The user associated with the ticket.
            ticket (Ticket): The ticket object to be created.

        Raises:
            NotImplementedError: If the method is not implemented in a concrete subclass.
        """
        raise NotImplementedError

    def modify_ticket(self, user, ticket):
        """
        Modify an existing ticket.

        Args:
            user (User): The user associated with the ticket.
            ticket (Ticket): The ticket object to be modified.

        Raises:
            NotImplementedError: If the method is not implemented in a concrete subclass.
        """
        raise NotImplementedError

    def change_ticket_priority(self, user, ticket, priority):
        """
        Change the priority of a ticket.

        Args:
            user (User): The user associated with the ticket.
            ticket (Ticket): The ticket object to be updated.
            priority (str): The new priority level.

        Raises:
            NotImplementedError: If the method is not implemented in a concrete subclass.
        """
        raise NotImplementedError

    def assign_ticket(self, user, ticket, to_be_assigned_user):
        """
        Assign a ticket to a user.

        Args:
            user (User): The user assigning ticket to to_be_assigned_user.
            to_be_assigned_user (User): The user to be assigned to the ticket.
            ticket (Ticket): The ticket object to be assigned.

        Raises:
            NotImplementedError: If the method is not implemented in a concrete subclass.
        """
        raise NotImplementedError

    def add_follow_up(self, user, ticket, follow_up):
        """
        Add a new follow-up to a ticket.

        Args:
            user (User): The user associated with the follow-up.
            ticket (Ticket): The ticket object to which the follow-up is being added.
            follow_up (FollowUp): The follow-up object to be added.

        Raises:
            NotImplementedError: If the method is not implemented in a concrete subclass.
        """
        raise NotImplementedError

    def add_attachment_to_ticket(self, user, attachment, ticket):
        """
        Add an attachment to a ticket.

        Args:
            user (User): The user associated with the attachment.
            attachment (Attachment): The attachment object to be added.
            ticket (Ticket): The ticket object to which the attachment is being added.

        Raises:
            NotImplementedError: If the method is not implemented in a concrete subclass.
        """
        raise NotImplementedError


class AbstractAccountsService(abc.ABC):
    def login_with_username_and_password(self, username, password):
        raise NotImplementedError

    def modify_user(self, user):
        raise NotImplementedError

    def create_organization(self, organization):
        raise NotImplementedError

    def modify_organization(self, organization):
        raise NotImplementedError

    def create_role(self, role, organization):
        raise NotImplementedError

    def change_agent_role(self, role, agent):
        raise NotImplementedError

    def add_pre_set_reply(self, agent, pre_set_reply):
        raise NotImplementedError

