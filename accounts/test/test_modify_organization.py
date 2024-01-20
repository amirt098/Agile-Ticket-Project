from django.test import TestCase
from runner.bootstraper import get_bootstrapper
from accounts import exceptions
from accounts.models import Organization
from accounts.dataclasses import Organization as OrganizationDataclass


class TestModifyOrganization(TestCase):

    def setUp(self):
        self.service = get_bootstrapper().get_account_service()
        self.organization = Organization.objects.create(name='TestOrganization', address='123 Main St')

    def test_modify_organization_successful(self):
        organization_data = OrganizationDataclass(
            name='TestOrganization',
            address='456 Oak St',
            phone=9876543210,
            description='Updated organization details'
        )

        self.service.modify_organization(organization_data)

        modified_organization = Organization.objects.get(name='TestOrganization')
        self.assertIsNotNone(modified_organization)
        self.assertEqual(modified_organization.address, '456 Oak St')
        self.assertEqual(modified_organization.phone, '9876543210')
        self.assertEqual(modified_organization.description, 'Updated organization details')

    def test_modify_organization_non_existent(self):
        organization_data = OrganizationDataclass(
            name='NonExistentOrganization',
            address='789 Elm St',
            phone=5551234567,
            description='Attempt to modify a non-existent organization'
        )

        with self.assertRaises(exceptions.OrganizationNotFound):
            self.service.modify_organization(organization_data)

    def test_modify_organization_partial_data(self):
        partial_organization_data = OrganizationDataclass(
            name='TestOrganization',
            phone=5555555555,
        )

        self.service.modify_organization(partial_organization_data)

        modified_organization = Organization.objects.get(name='TestOrganization')
        self.assertIsNotNone(modified_organization)
        self.assertEqual(modified_organization.address, '123 Main St')  # Address should not be modified
        self.assertEqual(modified_organization.phone, '5555555555')  # Only phone should be modified
        self.assertIsNone(modified_organization.description)  # Description should remain None
    #
    # def test_modify_organization_invalid_data(self):
    #     invalid_organization_data = OrganizationDataclass(
    #         name='TestOrganization',
    #         phone='invalid_phone',
    #     )
    #
    #     with self.assertRaises(exceptions.OrganizationNotFound):
    #         self.service.modify_organization(invalid_organization_data)
