from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

# Build url for Create user: api:userprofile-list
# api is app name in urls.py
# userprofile: is the custom model for our database.
# Since we use ModelViewSet, we dont
# specify basename, so we will use custom model name
# list: method for post, get
CREATE_USER_URL = reverse('api:user-create')
LOGIN_URL = reverse('api:login')
LIST_USER_URL = reverse('api:user-list')


def user_detail_url(user_id):
    """
    Return user detail url of a specific user
    """
    return reverse('api:user-details/', args=[user_id])

# def user_manage_url(user_id):
#     """
#     Return user manage url of a specific user
#     """
#     return reverse('api:user/manage/', args=[user_id])


class PublicApiTests(TestCase):
    """
    Test api that do not require authentication
    """

    def setUp(self) -> None:
        self.client = APIClient()

    def sample_payload(self, email='user1@test.com',
                       password='testpass123', name='user1',
                       avatarURL='user1avatar'):
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

    def create_login_request(self, email, password):
        """
        Make the post request to login in json format.
        Return the response
        """
        return self.client.post(LOGIN_URL,
                                {'email': email, 'password': password},
                                format='json')

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

    def test_login_with_valid_credential(self):
        """
        Test user can login succesfully.
        """
        payload = self.sample_payload()
        # Create user
        get_user_model().objects.create_user(**payload)
        # Login using the payload
        res = self.create_login_request(payload['email'], payload['password'])
        # Expect status 200
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Expect return the token
        self.assertIn('token', res.data)

    def test_login_with_wrong_email(self):
        """
        Test login with email of non existing user.
        This should fail.
        """
        payload = self.sample_payload()
        # Create user
        get_user_model().objects.create_user(**payload)
        # Modify the email to be different to the one in payload
        payload['email'] = 'notexistinguser@gmail.com'
        # Login using the payload
        res = self.create_login_request(payload['email'], payload['password'])
        # Assert status 401
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_wrong_password(self):
        """
        Test login with wrong password of existing user.
        This should fail
        """
        payload = self.sample_payload()
        # Create user
        get_user_model().objects.create_user(**payload)
        # Modify the password to be different to the one in payload
        payload['password'] = 'wrongpass123'
        # Login using the payload
        res = self.create_login_request(payload['email'], payload['password'])
        # Assert status 401
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_none_email(self):
        """
        Test login with email is none.
        This should fail
        """
        payload = self.sample_payload()
        # Create user
        get_user_model().objects.create_user(**payload)
        # Login using the payload
        res = self.create_login_request(None, payload['password'])
        # Assert status 400
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_none_password(self):
        """
        Test login with wrong password of existing user.
        This should fail
        """
        payload = self.sample_payload()
        # Create user
        get_user_model().objects.create_user(**payload)
        # Login using the payload
        res = self.create_login_request(payload['email'], None)
        # Assert status 400
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_not_allow_get_method(self):
        """
        Test login does not allow get method
        """
        res = self.client.get(LOGIN_URL)
        # Expect status 405
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_list_all_users_without_authentication(self):
        """
        Test list all users without authentication.
        This should fail
        """
        res = self.client.get(LIST_USER_URL)
        # Expect status unauthorized
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_user_without_authentication(self):
        """
        Test retrieve a user without authentication.
        This should fail
        """
        payload = self.sample_payload()
        # Create user
        user = get_user_model().objects.create_user(**payload)
        # Create user detail url of this user
        user_url = user_detail_url(user.id)
        # Make get request
        res = self.client.get(user_url)
        # Expect status 401
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_update_user_without_authentication(self):
    #     """
    #     Test update a user without authentication.
    #     This should fail
    #     """

    # def test_partial_update_without_authentication(self):
    #     """
    #     Test partial update a user without authentication.
    #     This should fail
    #     """

    # def test_delete_user_without_authentication(self):
    #     """
    #     Test delete a user without authentication.
    #     This should fail
    #     """


class PrivateApiTests(TestCase):
    """
    Test require authentication
    """

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = self.create_sample_user()
        # Force the user authenticated
        self.client.force_authenticate(user=self.user)

    def create_sample_user(self, email='user1@test.com',
                           password='testpass123', name='user1'):
        """
        Create and return sample user
        """
        return get_user_model().objects.create_user(
            email=email, password=password, name=name
        )

    def test_list_all_users_with_authentication(self):
        """
        Test list all users with authentication.
        This should success
        """
        # Make get request
        res = self.client.get(LIST_USER_URL)
        # Expect status 200
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_user_with_authentication(self):
        """
        Test retrieve a user with authentication
        """
        # Create user url
        user_url = user_detail_url(self.user.id)
        # Make get request
        res = self.client.get(user_url)
        # Expect status 200
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        user = get_user_model().objects.get(**res.data)

        # Expect the user is the same as self.user
        self.assertEqual(self.user.email, user.email)
        self.assertEqual(self.user.name, user.name)
        # Expect the password is not return
        self.assertNotIn('password', res.data)
