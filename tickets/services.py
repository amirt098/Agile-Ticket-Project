import logging

from django.utils import timezone
from datetime import datetime
from accounts import dataclasses as account_dataclasses
from accounts.models import Organization as account_organization
from . import dataclasses
from . import interfaces
from .models import Product, Ticket, FollowUp

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

    def create_ticket(self, username: str, ticket_data: dataclasses.Ticket):
        logger.info(f'username: {username}, ticket_data: {ticket_data}')
        if ticket_data.dead_line_date:
            self._validate_future_datetime(ticket_data.dead_line_date)
        try:
            ticket = Ticket.objects.create(title=ticket_data.title, owner=username,
                                           product_uid=ticket_data.product.uid, )
            if ticket_data.description:
                ticket.description = ticket_data.description
            if ticket_data.priority:
                ticket.priority = ticket_data.priority
            if ticket_data.dead_line_date:
                ticket.dead_line_date = ticket_data.dead_line_date
            ticket.status = 'Open'
            ticket.save()
            logger.info(f"User {username} created a ticket with title {ticket.title} successfully.")
            logger.info(f"ticket {username} returned")
            result = self._convert_ticket_to_dataclass(ticket)
            logger.info(f'result: {result}')
            if ticket_data.product.pre_set_reply:
                self.add_follow_up(
                    username='System',
                    ticket_data=result,
                    follow_up_data=dataclasses.FollowUp(
                        title=ticket_data.product.owner,
                        text=ticket_data.product.pre_set_reply,
                    )
                )
            return result
        except Exception as e:
            logger.error(f"Error during ticket creation: {e}", exc_info=True)
            raise e

    @staticmethod
    def _validate_future_datetime(value):
        if value <= timezone.now():
            raise Exception('The date and time must be in the future.')

    def modify_ticket(self, username: str, ticket_data: dataclasses.Ticket):
        logger.info(f'username: {username}, ticket_data: {ticket_data}')
        try:
            ticket = Ticket.objects.get(uid=ticket_data.uid)
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

    def assign_ticket(self, username: str, ticket_data: dataclasses.Ticket, to_be_assigned_username: str):
        logger.info(
            f'username: {username}, ticket_data: {ticket_data}, to_be_assigned_username: {to_be_assigned_username}')
        try:
            ticket = Ticket.objects.get(uid=ticket_data.uid)
            ticket.assigned_to = to_be_assigned_username
            ticket.save()
            logger.info(f"User {username} assigned a ticket {ticket.uid} to {to_be_assigned_username} successfully.")
            return self._convert_ticket_to_dataclass(ticket)
        except Exception as e:
            logger.error(f"Error during ticket assignment: {e}", exc_info=True)
            raise e

    def change_status_ticket(self, username: str, ticket_data: dataclasses.Ticket, status: str):
        try:
            ticket = Ticket.objects.get(uid=ticket_data.uid)
            ticket.status = status
            ticket.save()
            logger.info(f"User {username} change status ticket {ticket.uid} to {status} successfully.")
            return self._convert_ticket_to_dataclass(ticket)
        except Exception as e:
            logger.error(f"Error during ticket status change: {e}", exc_info=True)
            raise e

    def add_follow_up(self, username: str, ticket_data: dataclasses.Ticket, follow_up_data: dataclasses.FollowUp):
        try:
            logger.info(f'username: {username}, ticket: {ticket_data}, follow_up_data:{follow_up_data}')
            follow_up = FollowUp.objects.create(
                title=follow_up_data.title,
                text=follow_up_data.text,
                user=username,
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
        logger.info(f'filter: {filters}')
        tickets = Ticket.objects.filter(**filters)
        result = [self._convert_ticket_to_dataclass(ticket) for ticket in tickets]
        logger.info(result)
        return result

    def get_products(self, organization_name: str = None):
        logger.info(f'organization_name: {organization_name}')

        queryset = Product.objects.all()

        if organization_name:
            logger.info('filtering')
            queryset = queryset.filter(owner=organization_name)

        result = dataclasses.ProductList(
            results=[self._convert_product_to_dataclass(product) for product in queryset]
        )

        logger.info(f"result: {result}")
        return result

    def get_organizations(self, **filters):
        return account_organization.objects.filter(**filters)

    def _convert_ticket_to_dataclass(self, ticket: Ticket) -> dataclasses.Ticket:
        if ticket.dead_line_date:
            ticket_deadline_date = ticket.dead_line_date.replace(tzinfo=timezone.get_current_timezone())
            time_until_deadline = ticket_deadline_date - datetime.now(timezone.utc)
        else:
            time_until_deadline = None

        return dataclasses.Ticket(
            uid=ticket.uid,
            title=ticket.title,
            owner=ticket.owner,
            description=ticket.description,
            status=ticket.status,
            priority=ticket.priority,
            assigned_to=ticket.assigned_to,
            product=self._convert_product_to_dataclass(Product.objects.get(uid=ticket.product_uid)),
            closed_date=str(ticket.closed_date),
            created_at=str(ticket.created_at),
            updated_at=str(ticket.updated_at),
            dead_line_date=ticket.dead_line_date,
            time_until_deadline=time_until_deadline,
            have_answer=self._check_answer(ticket)
        )

    @staticmethod
    def _check_answer(ticket: Ticket) -> bool:
        product = Product.objects.get(uid=ticket.product_uid)
        followups = len(FollowUp.objects.filter(ticket_uid=ticket.uid))
        if product.pre_set_reply and followups > 1:
            return True
        if not product.pre_set_reply and followups > 0:
            return True
        return False

    @staticmethod
    def _convert_followup_to_dataclass(followup: FollowUp) -> dataclasses.FollowUp:
        return dataclasses.FollowUp(
            title=followup.title,
            user=followup.user,
            ticket_uid=followup.ticket_uid,
            text=followup.text,
            date=str(followup.date),
            created_at=str(followup.created_at),
            modified_at=str(followup.modified_at),
        )

    def get_product(self, product_uid):
        logger.info(f'Product_uid; {product_uid}')
        try:
            product = Product.objects.get(uid=product_uid)
        except Product.DoesNotExist:
            logger.info('Product with that uid does not exist')
            raise NotFound('Product with that uid does not exist')
        result = self._convert_product_to_dataclass(product)
        logger.info(f'result: {result}')
        return result

    def get_follow_ups(self, **filters):
        logger.info(f'filter: {filters}')
        follow_ups = FollowUp.objects.filter(**filters)
        result = [self._convert_followup_to_dataclass(follow_up) for follow_up in follow_ups]
        logger.info(result)
        return result
