import logging

from accounts import dataclasses as account_dataclasses
from . import interfaces
from . import dataclasses
from .models import Product, PreSetReply

logger = logging.getLogger(__name__)


class BadRequest(Exception):
    def __init__(self, message):
        super().__init__(f"{message}")


class NotFound(Exception):
    pass


class TicketService(interfaces.AbstractTicketServices):
    def create_product(self, agent_data: account_dataclasses.Agent, product_data: dataclasses.Product) -> dataclasses.Product:
        try:
        # pre_set_repley = PreSetReply.objects.get_or_create(
        #     name=product_data
        # )
            created_product = Product.objects.create(
                name=product_data.name,
                owner=agent_data.organization,
                description=product_data.description,

            )
            logger.info(f'product: {created_product.name} created successfully in organization {created_product.owner} by user: {agent_data.username}')
            result = self._convert_product_to_dataclass(created_product)
            return result
        except Exception as e:
            logger.error(f"Error during user creation: {e}", exc_info=True)
            raise e

    @staticmethod
    def _convert_product_to_dataclass(product: Product) -> dataclasses.Product:
        return dataclasses.Product(
            name=product.name,
            owner=product.owner,
            description=product.description,
            uid=product.uid,
        )

    def modify_product(self, user, product):
        pass

    def create_ticket(self, username: str, ticket_data: dataclasses.Ticket, product: dataclasses.Product):
        try:
            ticket = dataclasses.Ticket.objects.create(title= ticket_data.title, owner= ticket_data.owner, product_uid=product.uid,)
            if ticket_data.description:
                ticket.description = ticket_data.description
            if ticket_data.priority:
                ticket.priority = ticket_data.priority
            ticket.status = 'Open'
            ticket.save()
            logger.info(f"User {username} created a ticket with title {ticket.title} successfully.")
            logger.info(f"ticket {username} returned")
            return self._convert_ticket_to_dataclass(ticket)
        except Exception as e:
            logger.error(f"Error during ticket creation: {e}", exc_info=True)
            raise e

    def modify_ticket(self, user, ticket):
        pass

    def change_ticket_priority(self, user, ticket, priority):
        pass

    def assign_ticket(self, user, ticket, to_be_assigned_user):
        pass

    def add_follow_up(self, username: str, ticket, follow_up):
        try:
            ticket = dataclasses.Ticket.objects.create(title= ticket_data.title, owner= ticket_data.owner)
            if ticket_data.description:
                ticket.description = ticket_data.description
            if ticket_data.priority:
                ticket.priority = ticket_data.priority
            ticket.status = 'waiting for awnser'
            ticket.save()
            logger.info(f"User {username} created a ticket with title {ticket.title} successfully.")
            logger.info(f"ticket {username} returned")
            return self._convert_ticket_to_dataclass(ticket)
        except Exception as e:
            logger.error(f"Error during ticket creation: {e}", exc_info=True)
            raise e
        pass

    def add_attachment_to_ticket(self, user, attachment, ticket):
        pass

    def get_tickets(self, user, organization, agent):
        # add proper filters to be usable for agent, user, .....
        pass

    def get_products(self, user, organization):
        pass

    @staticmethod
    def _convert_ticket_to_dataclass(ticket: dataclasses.Ticket) -> dataclasses.Ticket:
        return dataclasses.Ticket(
            title=ticket.title,
            owner=ticket.owner,
            description=ticket.description,
            status=ticket.status,
        )

    # def add_pre_set_reply(self, agent: dataclasses.Agent, pre_set_reply: dataclasses.Agent):
    #     pass
