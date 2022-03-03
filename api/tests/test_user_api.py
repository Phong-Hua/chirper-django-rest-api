from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

# Build url for Create user: user:userprofile-list
# user is app name in urls.py
# userprofile: is the custom model for our database. Since we use ModelViewSet, we dont
# specify basename, so we will use custom model name
# list: method for post, get
CREATE_USER_URL = reverse('user:userprofile-list')


class PublicApiTests(TestCase):
    """
    Test api that do not require authentication
    """
    
    def setUp(self) -> None:
        self.client = APIClient()

    def sample_payload(self, email='user1@test.com',
        password='testpass123', name='user1', avatarURL='user1avatar'):
        return {
            'email': email,
            'password': password,
            'name': name,
            'avatarURL': avatarURL
        }

    def create_user_request(self, payload):
        """
        Make post request to create user in json format.
        Return the response
        """
        return self.client.post(CREATE_USER_URL, payload, format='json')


    def test_create_valid_user_success(self):
        """
        Test create user with valid success.
        This should pass
        """

        payload = self.sample_payload()

        # Make post request
        res = self.create_user_request(payload)

        # Expect status 201
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Serializer user
        user = get_user_model().objects.get(**res.data)

        # Expect email, name, avatarURL, password match
        self.assertEqual(user.email, payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertEqual(user.name, payload['name'])
        self.assertEqual(user.avatarURL, payload['avatarURL'])
        # Check the password do not return in data
        self.assertNotIn('password', res.data)

    def test_create_existing_user(self):
        """
        Test create a user with email of an existing user.
        This should fail
        """

        payload_1 = self.sample_payload()
        # Create user
        get_user_model().objects.create_user(**payload_1)

        # Make post request
        res = self.create_user_request(payload_1)
        # Expect Bad request status
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_invalid_email(self):
        """
        Test create a user with invalid email.
        This should fail
        """
        payload = self.sample_payload(email='invalidemail')
        # Make post request
        res = self.create_user_request(payload)
        # Expect Bad request status
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_empty_email(self):
        """
        Test create a user with empty email.
        This should fail
        """
        payload = self.sample_payload(email='')
        # Make post request
        res = self.create_user_request(payload)
        # Expect Bad request status
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_none_email(self):
        """
        Test create user with none email.
        This should fail
        """
        payload = self.sample_payload(email=None)
        # Make post request
        res = self.create_user_request(payload)
        # Expect Bad request status
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_no_email(self):
        """
        Test create user with email is missing in payload.
        This should fail
        """
        payload = self.sample_payload()
        payload.pop('email', None)
        # Make post request
        res = self.create_user_request(payload)
        # Expect Bad request status
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_empty_name(self):
        """
        Test create user with empty name.
        This should fail
        """
        payload = self.sample_payload(name='')
        # Make post request
        res = self.create_user_request(payload)
        # Expect Bad request status
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_none_name(self):
        """
        Test create user with none name.
        This should fail
        """
        payload = self.sample_payload(name=None)
        # Make post request
        res = self.create_user_request(payload)
        # Expect Bad request status
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_no_name(self):
        """
        Test create user with name is not in payload.
        This should fail
        """
        payload = self.sample_payload()
        payload.pop('name', None)
        # Make post request
        res = self.create_user_request(payload)
        # Expect Bad request status
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_short_password(self):
        """
        Test create user with short password (less than 5 characters).
        This should fail
        """
        payload = self.sample_payload(password='pass')
        # Make post request
        res = self.create_user_request(payload)
        # Expect bad request status
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_empty_password(self):
        """
        Test create user with empty password.
        This should fail
        """
        payload = self.sample_payload(password='')
        # Make post request
        res = self.create_user_request(payload)
        # Expect bad request status
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_none_password(self):
        """
        Test create user with password is none.
        This should fail
        """
        payload = self.sample_payload(password=None)
        # Make post request
        res = self.create_user_request(payload)
        # Expect bad request status
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_no_password(self):
        """
        Test create user with password is missing from payload.
        This should fail
        """
        payload = self.sample_payload()
        payload.pop('password', None)
        # Make post request
        res = self.create_user_request(payload)
        # Expect bad request status
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

