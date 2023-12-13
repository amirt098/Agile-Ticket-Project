from django.test import TestCase
from runner.bootstraper import get_bootstrapper
from apps.accounts import exceptions
from apps.accounts.models import User, Agent, Organization, Role
from apps.accounts.dataclasses import Agent as AgentDataclass, Role as RoleDataclass


class TestModifyAgent(TestCase):

    def setUp(self):
        self.service = get_bootstrapper().get_account_service()
        self.test_organization = Organization.objects.create(name='TestOrganization')
        self.test_role = Role.objects.create(name='TestRole', description='Test Role Description')
        self.test_agent = Agent.objects.create(
            username='test_agent',
            organization=self.test_organization,
            role=self.test_role
        )

    def test_modify_agent_successful(self):
        Organization.objects.create(name='NewOrganization')
        modified_data = AgentDataclass(
            username='test_agent',
            first_name='NewFirstName',
            last_name='NewLastName',
            email='new.email@example.com',
            organization='NewOrganization',
            role=RoleDataclass(name='NewRole', description='New Role Description'),
            password='new_password123'
        )

        self.service.modify_agent(modified_data)

        # Fetch the agent from the database to verify modifications
        updated_agent = Agent.objects.get(username='test_agent')
        self.assertEqual(updated_agent.first_name, 'NewFirstName')
        self.assertEqual(updated_agent.last_name, 'NewLastName')
        self.assertEqual(updated_agent.email, 'new.email@example.com')
        self.assertEqual(updated_agent.organization.name, 'NewOrganization')
        self.assertEqual(updated_agent.role.name, 'NewRole')
        self.assertTrue(updated_agent.check_password('new_password123'))

    def test_modify_agent_not_found(self):
        non_existent_agent_data = AgentDataclass(username='nonexistent_agent')

        with self.assertRaises(exceptions.UserNotFound):
            self.service.modify_agent(non_existent_agent_data)

    def test_modify_agent_not_found(self):
        modified_data = AgentDataclass(
            username='test_agent',
            first_name='NewFirstName',
            last_name='NewLastName',
            email='new.email@example.com',
            organization='Invalid_Organization',
            role=RoleDataclass(name='NewRole', description='New Role Description'),
            password='new_password123'
        )

        with self.assertRaises(exceptions.OrganizationNotFound):
            self.service.modify_agent(modified_data)

