from django.test import TestCase
from runner.bootstraper import get_bootstrapper
from apps.accounts import exceptions
from apps.accounts.models import Role, Organization
from apps.accounts.dataclasses import Role as RoleDataclass, Organization as OrganizationDataclass


class TestCreateRole(TestCase):

    def setUp(self):
        self.service = get_bootstrapper().get_account_service()
        self.organization = Organization.objects.create(name='TestOrganization')

    def test_create_role_successful(self):
        role_data = RoleDataclass(
            name='Admin',
            description='Administrator role',
            organization='TestOrganization'
        )

        self.service.create_role(role_data)

        created_role = Role.objects.get(name='Admin')
        self.assertIsNotNone(created_role)
        self.assertEqual(created_role.description, 'Administrator role')

    def test_create_role_organization_not_found(self):
        role_data = RoleDataclass(
            name='Moderator',
            description='Moderator role',
            organization="invalid org"
        )

        with self.assertRaises(exceptions.OrganizationNotFound):
            self.service.create_role(role_data)
