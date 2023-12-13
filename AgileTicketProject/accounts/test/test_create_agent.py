from django.test import TestCase
from runner.bootstraper import get_bootstrapper
from apps.accounts import exceptions
from apps.accounts.models import Agent, Organization, Role
from apps.accounts.dataclasses import Agent as AgentDataclass, Role as RoleDataclass


class TestCreateAgent(TestCase):

    def setUp(self):
        self.service = get_bootstrapper().get_account_service()
        self.Org = Organization.objects.create(name='TestOrganization')

    def test_create_agent_successful(self):
        agent_data = AgentDataclass(
            username='good_agent',
            organization='TestOrganization',
            role=RoleDataclass(name='TestRole', description='Test Role Description'),
            password='password123'
        )

        self.service.create_agent(agent_data)

        created_agent = Agent.objects.get(username=agent_data.username)
        self.assertIsNotNone(created_agent)
        self.assertEqual(created_agent.organization.name, 'TestOrganization')
        self.assertEqual(created_agent.role.name, 'TestRole')
        self.assertTrue(created_agent.check_password('password123'))

    def test_create_agent_organization_not_found(self):
        agent_data = AgentDataclass(
            username='agent num2',
            organization='NonExistentOrganization',
            role=RoleDataclass(name='TestRole', description='Test Role Description')
        )

        with self.assertRaises(exceptions.OrganizationNotFound):
            self.service.create_agent(agent_data)

    # Add more tests as needed, for example, testing creation with partial data, etc.
