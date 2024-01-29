from django.test import TestCase
from runner.bootstraper import get_bootstrapper
from accounts import exceptions
from accounts.models import User, Organization
from accounts.dataclasses import Agent as AgentDataclass


class TestCreateAgent(TestCase):

    def setUp(self):
        self.service = get_bootstrapper().get_account_service()
        self.Org = Organization.objects.create(name='TestOrganization')

    def test_create_agent_successful(self):
        agent_data = AgentDataclass(
            username='good_agent',
            organization='TestOrganization',
            password='password123',
            first_name='first_name',
            last_name='last_name',
            email='agent@email.com'
        )
        agent_data.is_agent = True

        self.service.create_user(agent_data)

        created_agent = User.objects.get(username=agent_data.username)
        self.assertIsNotNone(created_agent)
        self.assertEqual(created_agent.organization.name, 'TestOrganization')
        self.assertEqual(created_agent.first_name, 'first_name')
        self.assertEqual(created_agent.last_name, 'last_name')
        self.assertEqual(created_agent.email, 'agent@email.com')
        self.assertTrue(created_agent.check_password('password123'))

    def test_create_agent_organization_not_found(self):
        agent_data = AgentDataclass(
            username='agent num2',
            organization='NonExistentOrganization'
        )
        agent_data.is_agent=True

        with self.assertRaises(exceptions.OrganizationNotFound):
            self.service.create_user(agent_data)

    # Add more tests as needed, for example, testing creation with partial data, etc.
