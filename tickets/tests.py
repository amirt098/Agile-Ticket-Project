import uuid

from django.test import TestCase

from accounts import dataclasses as account_dataclasses
from runner.bootstraper import get_bootstrapper
from tickets import dataclasses as ticket_dataclasses
from tickets.models import FollowUp


class TicketAndFollowUpTestCase(TestCase):
    def setUp(self) -> None:
        self.account_service = get_bootstrapper().get_account_service()
        self.ticket_service = get_bootstrapper().get_ticket_service()

        org = self.account_service.create_organization(account_dataclasses.Organization(name='ORG1'))

        agent_user_data = account_dataclasses.Agent(username='agent1', password='pass1', organization=org.name)
        agent_user_data.is_agent = True

        self.agent_user = self.account_service.create_user(agent_user_data)
        self.agent_user.is_agent = True
        self.agent_user.organization = org.name

        product_data = ticket_dataclasses.Product(name='Product1', owner='ORG1', uid=str(uuid.uuid4()),
                                                  pre_set_reply='Fast')
        self.product = self.ticket_service.create_product(agent_data=self.agent_user, product_data=product_data)

    def test_create_ticket(self):
        user_data = account_dataclasses.User(username='user1', password='pass1')
        user_data.is_agent = False
        user = self.account_service.create_user(user_data)
        ticket_data = ticket_dataclasses.Ticket(title='ticket1', product=self.product, uid=str(uuid.uuid4()),
                                                owner=user.username)
        self.ticket = self.ticket_service.create_ticket(username=user.username, ticket_data=ticket_data)

        self.assertEqual(self.ticket.owner, user.username)
        self.assertEqual(self.ticket.product.uid, str(self.product.uid))

    def test_create_follow_up(self):
        follow_up_data = ticket_dataclasses.FollowUp(title='follow up', ticket_uid=str(uuid.uuid4()))
        self.ticket_service.add_follow_up(
            username=self.agent_user.username,
            follow_up_data=follow_up_data,
            ticket_data=self.ticket)

        follow_up = FollowUp.objects.get(ticket_uid=self.ticket.uid)
        self.assertEqual(follow_up.title, follow_up_data.title)
