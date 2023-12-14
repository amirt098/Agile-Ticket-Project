from django.test import TestCase
from runner.bootstraper import get_bootstrapper
from accounts import exceptions
from accounts.models import Organization
from accounts.dataclasses import Organization as OrganizationDataclass


class TestCreateOrganization(TestCase):

    def setUp(self):
        self.service = get_bootstrapper().get_account_service()

    def test_create_organization_successful(self):
        organization_data = OrganizationDataclass(
            name='NewOrganization',
            Address='123 Main St',
            phone=1234567890,
            description='A test organization'
        )

        self.service.create_organization(organization_data)

        created_organization = Organization.objects.get(name='NewOrganization')
        self.assertIsNotNone(created_organization)
        self.assertEqual(created_organization.Address, '123 Main St')
        self.assertEqual(created_organization.phone, "1234567890")
        self.assertEqual(created_organization.description, 'A test organization')

    def test_create_organization_duplicate_name(self):
        organization_data = OrganizationDataclass(
            name='DuplicateOrganization',
            Address='456 Oak St',
            phone=9876543210,
            description='Another test organization'
        )

        self.service.create_organization(organization_data)

        with self.assertRaises(exceptions.OrganizationNotFound):
            self.service.create_organization(organization_data)

    def test_create_organization_partial_data(self):
        partial_organization_data = OrganizationDataclass(
            name='PartialOrganization',
            Address='789 Elm St',
        )

        self.service.create_organization(partial_organization_data)

        created_organization = Organization.objects.get(name='PartialOrganization')
        self.assertIsNotNone(created_organization)
        self.assertEqual(created_organization.Address, '789 Elm St')
        self.assertIsNone(created_organization.phone)
        self.assertIsNone(created_organization.description)

    # def test_create_organization_invalid_data_missing_name(self):
    #     invalid_organization_data = OrganizationDataclass(
    #         name='123'
    #         Address='456 Pine St',
    #         phone=5551234567,
    #         description='Invalid organization without a name'
    #     )
    #
    #     with self.assertRaises(exceptions.OrganizationNotFound):
    #         self.service.create_organization(invalid_organization_data)
