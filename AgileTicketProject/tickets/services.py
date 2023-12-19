import logging

from accounts import dataclasses as account_dataclasses
from accounts.models import Organization as account_organization
from . import dataclasses
from . import interfaces
from .models import Product, Ticket

logger = logging.getLogger(__name__)


class BadRequest(Exception):
    def __init__(self, message):
        super().__init__(f"{message}")


class NotFound(Exception):
    pass


class UserNeedPermission(BadRequest):
    def __init__(self):
        super().__init__("You need Permission to do that.")


class TicketService(interfaces.AbstractTicketServices):
    def create_product(self, agent_data: account_dataclasses.Agent,
                       product_data: dataclasses.Product) -> dataclasses.Product:
        if not agent_data.is_agent:
            logger.info("You need Permission to do that.")
            raise UserNeedPermission()
        try:
            created_product = Product.objects.create(
                name=product_data.name,
                owner=agent_data.organization,
                description=product_data.description,
                pre_set_reply=product_data.pre_set_reply,
                image=product_data.image,
            )
            logger.info(
                f'product: {created_product.name} created successfully in organization {created_product.owner} by user: {agent_data.username}')
            result = self._convert_product_to_dataclass(created_product)
            logger.info(f"result: {result}")
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
            pre_set_reply=product.pre_set_reply,
            image=product.image,
            uid=product.uid,
        )

    def modify_product(self, username: str, product_data: dataclasses.Product):
        try:
            product = Product.objects.get(product_data.uid)
            if product_data.description:
                product.description = product_data.description
            if product_data.name:
                product.name = product_data.name
            if product_data.owner:
                product.owner = product_data.owner
            product.save()
            logger.info(f"User {username} modified product {product.uid} successfully.")
            return self._convert_product_to_dataclass(product)
        except Exception as e:
            logger.error(f"Error during ticket creation: {e}", exc_info=True)
            raise e

    def create_ticket(self, username: str, ticket_data: dataclasses.Ticket, product: dataclasses.Product):
        try:
            ticket = dataclasses.Ticket.objects.create(title=ticket_data.title, owner=ticket_data.owner,
                                                       product_uid=product.uid, )
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

    def modify_ticket(self, username: str, ticket_data: dataclasses.Ticket):
        # user = User.objects.get(username=username)
        #
        #     raise Exception()
        try:
            ticket = Ticket.objects.get(ticket_data.uid)
            if ticket_data.status:
                ticket.status = ticket_data.status
            if ticket_data.title:
                ticket.title = ticket_data.title
            if ticket_data.assigned_to:
                ticket.assigned_to = ticket_data.assigned_to
            if ticket_data.priority:
                ticket.priority = ticket_data.priority
            if ticket_data.description:
                ticket.description = ticket_data.description
            ticket.save()
            logger.info(f"ticket {ticket.uid} modified successfully")
            return self._convert_ticket_to_dataclass(ticket)
        except Exception as e:
            logger.error(f"Error during ticket modified: {e}", exc_info=True)
            raise e

    def change_ticket_priority(self, user, ticket, priority):
        # in ticket modify handled
        pass

    def assign_ticket(self, username: str, ticket_data: dataclasses.Ticket, to_be_assigned_username: str):
        try:
            ticket = Ticket.objects.get(ticket_data.uid)
            ticket.assigned_to = to_be_assigned_username
            ticket.save()
            logger.info(f"User {username} assigned a ticket {ticket.uid} to {to_be_assigned_username} successfully.")
            return self._convert_ticket_to_dataclass(ticket)
        except Exception as e:
            logger.error(f"Error during ticket assignment: {e}", exc_info=True)
            raise e

    def change_status_ticket(self, username: str, ticket_data: dataclasses.Ticket, status: str):
        try:
            ticket = Ticket.objects.get(ticket_data.uid)
            ticket.status = status
            ticket.save()
            logger.info(f"User {username} change status ticket {ticket.uid} to {status} successfully.")
            return self._convert_ticket_to_dataclass(ticket)
        except Exception as e:
            logger.error(f"Error during ticket status change: {e}", exc_info=True)
            raise e

    def add_follow_up(self, username: str, ticket_data: dataclasses.Ticket, follow_up_data: dataclasses.FollowUp):
        try:

            follow_up = dataclasses.FollowUp.objects.create(title=follow_up_data.title, owner=username,
                                                            ticket_uid=ticket_data.uid)
            follow_up.save()
            logger.info(f"User {username} created a followup to ticket {ticket_data.uid}  successfully.")
            return self._convert_followup_to_dataclass(follow_up)
        except Exception as e:
            logger.error(f"Error during ticket creation: {e}", exc_info=True)
            raise e

    def add_attachment_to_ticket(self, user, attachment, ticket):
        pass

    def get_tickets(self, **filters):
        return Ticket.objects.filter(**filters)

        # add proper filters to be usable for agent, user, .....

    def get_products(self, filters: dataclasses.ProductFilter = None):
        logger.info(f'filters: {filters}')

        queryset = Product.objects.all()

        if filters:
            if filters.owner:
                queryset = queryset.filter(owner__icontains=filters.owner)
            # Add more filter conditions as needed

        result = dataclasses.ProductList(
            results=[self._convert_product_to_dataclass(product) for product in queryset]
        )

        logger.info(f"result: {result}")
        return result

    def get_organizations(self, **filters):
        return account_organization.objects.filter(**filters)

    @staticmethod
    def _convert_ticket_to_dataclass(ticket: dataclasses.Ticket) -> dataclasses.Ticket:
        return dataclasses.Ticket(
            title=ticket.title,
            owner=ticket.owner,
            description=ticket.description,
            status=ticket.status,
        )

    @staticmethod
    def _convert_followup_to_dataclass(followup: dataclasses.FollowUp) -> dataclasses.FollowUp:
        return dataclasses.FollowUp(
            title=followup.title,
            user=followup.user,
            ticket_uid=followup.ticket_uid,
            text=followup.text,
            date=followup.date,
        )
