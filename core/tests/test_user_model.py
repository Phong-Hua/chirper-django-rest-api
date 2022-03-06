from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError


class UserModelTests(TestCase):
    """
    Test the model
    """

    def sample_user_info(self):
        """
        Create a sample user info.
        """
        return {
            'email': 'user1@test.com',
            'name': 'user1',
            'password': 'testpass123',
            'avatarURL': 'user1avatar'
        }

    def test_create_user_with_email_successful(self):
        """
        Test create user with email successful
        """
        payload = self.sample_user_info()
        # Create user
        user = get_user_model().objects.create_user(**payload)

        # Expect email, name, password, avatar match
        self.assertEqual(user.email, payload['email'])
        self.assertEqual(user.name, payload['name'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertEqual(user.avatarURL, payload['avatarURL'])

    def test_create_user_with_duplicated_email(self):
        """
        Test create user with duplicate email.
        This should fail
        """
        payload = self.sample_user_info()
        # Create user
        get_user_model().objects.create_user(**payload)

        another_payload = {
            'email': payload['email'],
            'name': 'another user',
            'password': 'testpassERTD123',
            'avatarURL': 'my_url'
        }

        # Because email is already exist, we expect this to raise
        #  IntegrityError
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(**another_payload)

    def test_create_user_with_invalid_email(self):
        """
        Test create a user with invalid email.
        This should fail
        """
        payload = self.sample_user_info()
        payload['email'] = 'invalid_email'

        # Because email is invalid, we expect this to raise an error
        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(**payload)

    def test_create_user_with_empty_email(self):
        """
        Test create a user with empty email.
        This should fail
        """
        payload = self.sample_user_info()
        payload['email'] = ''

        # Because email is invalid, we expect this to raise an error
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(**payload)

    def test_create_user_with_no_email(self):
        """
        Test create a user with no email.
        This should fail
        """
        payload = self.sample_user_info()
        payload['email'] = None

        # Because email is invalid, we expect this to raise an error
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(**payload)

    def test_create_user_with_empty_password(self):
        """
        Test create a user with empty password.
        This should fail
        """
        payload = self.sample_user_info()
        payload['password'] = ''

        # Because email is invalid, we expect this to raise an error
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(**payload)

    def test_create_user_with_no_password(self):
        """
        Test create a user with no password.
        This should fail.
        """
        payload = self.sample_user_info()
        payload['password'] = None

        # Because email is invalid, we expect this to raise an error
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(**payload)

    def test_create_user_with_empty_name(self):
        """
        Test create a user with empty name.
        This should fail
        """
        payload = self.sample_user_info()
        payload['name'] = ''

        # Because email is invalid, we expect this to raise an error
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(**payload)

    def test_create_user_with_no_name(self):
        """
        Test create a user with no name.
        This should fail
        """
        payload = self.sample_user_info()
        payload['name'] = None

        # Because email is invalid, we expect this to raise an error
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(**payload)

    def test_create_new_superuser_successful(self):
        """
        Test create a new superuser.
        """
        payload = self.sample_user_info()
        user = get_user_model().objects.create_superuser(**payload)

        # We expect this is staff and superuser
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
