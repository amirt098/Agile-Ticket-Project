from django.test import TestCase
from runner.bootstraper import get_bootstrapper
from apps.accounts import exceptions
from apps.accounts.models import User


class TestLoginWithUserNameAndPassword(TestCase):

    def setUp(self):
        self.service = get_bootstrapper().get_account_service()
        self.test_user = User.objects.create_user(username='test_user', password='password123')

    def test_login_with_username_and_password_successful(self):
        result = self.service.login_with_username_and_password('test_user', 'password123')
        self.assertIsNone(result)

    def test_login_with_username_and_password_invalid_password(self):
        with self.assertRaises(exceptions.LoginFailed):
            self.service.login_with_username_and_password('test_user', 'invalid_password')

    def test_login_with_username_and_password_user_not_found(self):
        with self.assertRaises(exceptions.LoginFailed):
            self.service.login_with_username_and_password('nonexistent_user', 'password123')
