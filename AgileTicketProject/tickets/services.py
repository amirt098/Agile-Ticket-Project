import logging
from . import interfaces

logger = logging.getLogger(__name__)


class BadRequest(Exception):
    def __init__(self, message):
        super().__init__(f"{message}")


class NotFound(Exception):
    pass


class TicketService(interfaces.AbstractTicketServices):
    def create_product(self, user, product):
        pass

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
