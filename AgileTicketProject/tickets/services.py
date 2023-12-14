import logging
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
    def create_product(self, user, product_data: dataclasses.Product) -> dataclasses.Product:
        logger.info(f"user: {user}, product: {product_data}")
        # pre_set_repley = PreSetReply.objects.get_or_create(
        #     name=product_data
        # )
        created_product = Product.objects.create(
            name=product_data.name,
            owner=product_data.owner,
            description=product_data.description,

        )
        result = self._convert_product_to_dataclasses(created_product)
        logger.info(f'result: {result}')
        return result

    @staticmethod
    def _convert_product_to_dataclasses(product: Product) -> dataclasses.Product:
        return dataclasses.Product(
            name=product.name,
            owner=product.owner,
            description=product.description,
        )

    def modify_product(self, user, product):
        pass

    def create_ticket(self, user, ticket):
        pass

    def modify_ticket(self, user, ticket):
        pass

    def change_ticket_priority(self, user, ticket, priority):
        pass

    def assign_ticket(self, user, ticket, to_be_assigned_user):
        pass

    def add_follow_up(self, user, ticket, follow_up):
        pass

    def add_attachment_to_ticket(self, user, attachment, ticket):
        pass

    def get_tickets(self, user, organization, agent):
        # add proper filters to be usable for agent, user, .....
        pass

    def get_products(self, user, organization):
        pass

    # def add_pre_set_reply(self, agent: dataclasses.Agent, pre_set_reply: dataclasses.Agent):
    #     pass
