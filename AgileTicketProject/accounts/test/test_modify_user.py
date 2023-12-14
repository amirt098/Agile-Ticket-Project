
from django.test import TestCase
from runner.bootstraper import get_bootstrapper
from accounts import exceptions
from accounts.models import User
from accounts.dataclasses import User as UserDataclass


class TestModifyUser(TestCase):

    def setUp(self):
        self.service = get_bootstrapper().get_account_service()
        self.test_user = User.objects.create_user(username='test_user', password='password123')

    def tearDown(self):
        self.test_user.delete()

    def test_modify_user_successful(self):
        modified_data = UserDataclass(username='test_user', first_name='NewFirstName', last_name='NewLastName',
                                      email='new.email@example.com')
        self.service.modify_user(modified_data)

        updated_user = User.objects.get(username='test_user')
        self.assertEqual(updated_user.first_name, 'NewFirstName')
        self.assertEqual(updated_user.last_name, 'NewLastName')
        self.assertEqual(updated_user.email, 'new.email@example.com')

    def test_modify_user_password_successful(self):
        modified_data = UserDataclass(username='test_user', password='NewPassword123', first_name='NewFirstName2', last_name='NewLastName',
                                      email='new.email@example.com')
        self.service.modify_user(modified_data)

        updated_user = User.objects.get(username='test_user')
        self.assertTrue(updated_user.check_password(modified_data.password), True)
        self.assertEqual(updated_user.first_name, 'NewFirstName2')
        self.assertEqual(updated_user.last_name, 'NewLastName')
        self.assertEqual(updated_user.email, 'new.email@example.com')

    def test_modify_user_not_found(self):
        non_existent_user_data = UserDataclass(username='nonexistent_user', first_name='NewFirstName',
                                               last_name='NewLastName', email='new.email@example.com')

        with self.assertRaises(exceptions.UserNotFound):
            self.service.modify_user(non_existent_user_data)
