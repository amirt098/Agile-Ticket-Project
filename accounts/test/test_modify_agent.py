from django.test import TestCase

from accounts.models import Organization, User
from runner.bootstraper import get_bootstrapper
from accounts import exceptions
from accounts.dataclasses import Agent as AgentDataclass


class TestModifyAgent(TestCase):

    def setUp(self):
        self.service = get_bootstrapper().get_account_service()
        self.test_organization = Organization.objects.create(name='TestOrganization')
        self.test_agent = User.objects.create(
            username='test_agent',
            organization=self.test_organization,
        )

    def test_modify_agent_successful(self):
        Organization.objects.create(name='NewOrganization')
        modified_data = AgentDataclass(
            username='test_agent',
            first_name='NewFirstName',
            last_name='NewLastName',
            email='new.email@example.com',
            password='new_password123'
        )

        self.service.modify_agent(modified_data)

        # Fetch the agent from the database to verify modifications
        updated_agent = User.objects.get(username='test_agent')
        self.assertEqual(updated_agent.first_name, 'NewFirstName')
        self.assertEqual(updated_agent.last_name, 'NewLastName')
        self.assertEqual(updated_agent.email, 'new.email@example.com')
        self.assertTrue(updated_agent.check_password('new_password123'))

    def test_modify_agent_not_found(self):
        non_existent_agent_data = AgentDataclass(username='nonexistent_agent')

        with self.assertRaises(exceptions.UserNotFound):
            self.service.modify_agent(non_existent_agent_data)

    # def test_modify_agent_not_found(self):
    #     agent_data = AgentDataclass(
    #         username='test_agent_to_modify',
    #         organization='TestOrganization'
    #     )
    #     agent_data.is_agent = True
    #     self.service.create_user(agent_data)
    #
    #     modified_data = AgentDataclass(
    #         username='test_agent_to_modify',
    #         first_name='NewFirstName',
    #         last_name='NewLastName',
    #         email='new.email@example.com',
    #         organization='Invalid_Organization',
    #         password='new_password123'
    #     )
    #     modified_data.is_agent = True
    #
    #     with self.assertRaises(exceptions.OrganizationNotFound):
    #         self.service.modify_agent(modified_data)

