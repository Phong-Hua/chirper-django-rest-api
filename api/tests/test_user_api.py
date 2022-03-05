from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


CREATE_USER_URL = reverse('api:user-create')
LOGIN_URL = reverse('api:login')
LIST_USER_URL = reverse('api:user-list')


def user_detail_url(user_id):
    """
    Return user detail url of a specific user
    """
    return reverse('api:user-details/', args=[user_id])


def user_update_url(user_id):
    """
    Return user update url of a specific user
    """
    return reverse('api:user-update/', args=[user_id])


def user_delete_url(user_id):
    """
    Return user delete user of a specific user
    """
    return reverse('api:user-delete/', args=[user_id])


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

    def test_create_user_no_avatarURL(self):
        """
        Test create user with no avatar.
        Since avatar is not requried.
        This should success
        """
        payload = self.sample_payload()
        payload.pop('avatarURL', None)
        # Make post request
        res = self.create_user_request(payload)
        # Expect 201 status
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        # Expect other info match
        self.assertEqual(user.email, payload['email'])
        self.assertEqual(user.name, payload['name'])
        self.assertTrue(user.check_password(payload['password']))
        # Expect the avatarURL is an empty string
        self.assertEqual(user.avatarURL, '')

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

    def test_update_user_without_authentication(self):
        """
        Test update a user without authentication.
        This should fail
        """
        payload = self.sample_payload()
        # Create user
        user = get_user_model().objects.create_user(**payload)
        # Edit the payload
        payload['email'] = 'user1edit@test.com'
        payload['name'] = payload['name'] + 'edit'
        # Make put request
        res = self.client.put(user_update_url(user.id), payload)
        # Expect status 401
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_without_authentication(self):
        """
        Test partial update a user without authentication.
        This should fail
        """
        payload = self.sample_payload()
        # Create user
        user = get_user_model().objects.create_user(**payload)
        # Make patch request
        res = self.client.patch(user_update_url(user.id),
                                {'email': 'newEmail@test.com'})
        # Expect status 401
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user_without_authentication(self):
        """
        Test delete a user without authentication.
        This should fail
        """
        payload = self.sample_payload()
        # Create user
        user = get_user_model().objects.create_user(**payload)
        # Make delete request
        res = self.client.delete(user_delete_url(user.id))
        # Expect status 401
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


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
                           password='testpass123', name='user1',
                           **extra_params):
        """
        Create and return sample user
        """
        return get_user_model().objects.create_user(
            email=email, password=password, name=name, **extra_params
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

    def test_update_own_user_with_authentication(self):
        """
        Test the login user update their own info.
        This should pass
        """
        payload = {
            'email': 'newuser1@test.com',
            'password': 'newuser1',
            'name': 'newuser1',
            'avatarURL': 'newuser1Avatar'
        }
        # user_url
        user_url = user_update_url(self.user.id)
        # Make put request
        res = self.client.put(user_url, payload)
        # Expect status 200
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Update user with the latest value from db
        self.user.refresh_from_db()

        # Expect other info match
        self.assertEqual(self.user.email, payload['email'])
        self.assertEqual(self.user.name, payload['name'])
        self.assertEqual(self.user.avatarURL, payload['avatarURL'])
        self.assertTrue(self.user.check_password(payload['password']))

    def test_update_second_user_with_authentication(self):
        """
        Test the login user update info of another user.
        This should fail.
        """
        payload = {
            'email': 'user2@test.com',
            'name': 'user2',
            'password': 'user2pass',
            'avatarURL': 'user2Avatar'
        }
        # Create another user
        another_user = self.create_sample_user(**payload)
        # Create another payload from payload
        another_payload = {x: 'edit'+payload[x] for x in payload.keys()}
        # Create user url
        user_url = user_update_url(another_user.id)
        # Make put request
        res = self.client.put(user_url, another_payload)
        # Expect status 403
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        # Refresh another_user
        another_user.refresh_from_db()
        # Expect info of another_user is the same as before
        self.assertEqual(another_user.email, payload['email'])
        self.assertEqual(another_user.name, payload['name'])
        self.assertEqual(another_user.avatarURL, payload['avatarURL'])
        self.assertTrue(another_user.check_password(payload['password']))

    def test_partial_update_email_own_user_with_authentication(self):
        """
        Test the login user partial update email their own info.
        This should pass
        """
        # Create user url
        user_url = user_update_url(self.user.id)
        email = 'user1newemail@test.com'
        # Make patch request
        res = self.client.patch(user_url, {'email': email})
        # Expect status 200
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Refresh user
        self.user.refresh_from_db()
        # Expect email change
        self.assertEqual(self.user.email, email)

    def test_partial_update_email_second_user_with_authentication(self):
        """
        Test the login user partial update email of another user.
        This should fail.
        """
        payload = {
            'email': 'user2@test.com',
            'name': 'user2',
            'password': 'user2pass',
            'avatarURL': 'user2Avatar'
        }
        # Create another user
        another_user = self.create_sample_user(**payload)
        new_email = 'user2newemail@test.com'
        # Make patch request
        res = self.client.patch(user_update_url(another_user.id),
                                {'email': new_email})
        # Refresh another_user
        another_user.refresh_from_db()
        # Expect status 403
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        # Expect email do not change
        self.assertEqual(another_user.email, payload['email'])

    def test_partial_update_name_own_user_with_authentication(self):
        """
        Test the login user partial update name their own info.
        This should pass
        """
        # Create user url
        user_url = user_update_url(self.user.id)
        name = 'user1newname'
        # Make patch request
        res = self.client.patch(user_url, {'name': name})
        # Expect status 200
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Refresh user
        self.user.refresh_from_db()
        # Expect name change
        self.assertEqual(self.user.name, name)

    def test_partial_update_name_second_user_with_authentication(self):
        """
        Test the login user partial update name of another user.
        This should fail.
        """
        payload = {
            'email': 'user2@test.com',
            'name': 'user2',
            'password': 'user2pass',
            'avatarURL': 'user2Avatar'
        }
        # Create another user
        another_user = self.create_sample_user(**payload)
        new_name = 'user2newname'
        # Make patch request
        res = self.client.patch(user_update_url(another_user.id),
                                {'name': new_name})
        # Refresh another_user
        another_user.refresh_from_db()
        # Expect status 403
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        # Expect name do not change
        self.assertEqual(another_user.name, payload['name'])

    def test_partial_update_password_own_user_with_authentication(self):
        """
        Test the login user partial update email their own info.
        This should pass
        """
        # Create user url
        user_url = user_update_url(self.user.id)
        password = 'user1newpassword'
        # Make patch request
        res = self.client.patch(user_url, {'password': password})
        # Expect status 200
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Refresh user
        self.user.refresh_from_db()
        # Expect password change
        self.assertTrue(self.user.check_password(password))

    def test_partial_update_password_second_user_with_authentication(self):
        """
        Test the login user partial update email of another user.
        This should fail.
        """
        payload = {
            'email': 'user2@test.com',
            'name': 'user2',
            'password': 'user2pass',
            'avatarURL': 'user2Avatar'
        }
        # Create another user
        another_user = self.create_sample_user(**payload)
        new_password = 'user2newpassword'
        # Make patch request
        res = self.client.patch(user_update_url(another_user.id),
                                {'password': new_password})
        # Refresh another_user
        another_user.refresh_from_db()
        # Expect status 403
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        # Expect password do not change
        self.assertTrue(another_user.check_password(payload['password']))

    def test_partial_update_avatar_own_user_with_authentication(self):
        """
        Test the login user partial update email their own info.
        This should pass
        """
        # Create user url
        user_url = user_update_url(self.user.id)
        avatar = 'user1newavatar'
        # Make patch request
        res = self.client.patch(user_url, {'avatarURL': avatar})
        # Expect status 200
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Refresh user
        self.user.refresh_from_db()
        # Expect avatar change
        self.assertEqual(self.user.avatarURL, avatar)

    def test_partial_update_avatar_second_user_with_authentication(self):
        """
        Test the login user partial update email of another user.
        This should fail.
        """
        payload = {
            'email': 'user2@test.com',
            'name': 'user2',
            'password': 'user2pass',
            'avatarURL': 'user2Avatar'
        }
        # Create another user
        another_user = self.create_sample_user(**payload)
        new_avatar = 'user2newavatar'
        # Make patch request
        res = self.client.patch(user_update_url(another_user.id),
                                {'avatarURL': new_avatar})
        # Refresh another_user
        another_user.refresh_from_db()
        # Expect status 403
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        # Expect avatar do not change
        self.assertEqual(another_user.avatarURL, payload['avatarURL'])

    def test_delete_own_user_with_authentication(self):
        """
        Test the login user delete their own info.
        This should pass
        """
        # Make delete request
        res = self.client.delete(user_delete_url(self.user.id))
        # Expect response is 204
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        # Expect the user do not exist
        user_exist = get_user_model().objects.filter(id=self.user.id).exists()
        self.assertFalse(user_exist)

    def test_delete_second_user_with_authentication(self):
        """
        Test the login user delete info of another user.
        This should fail.
        """
        payload = {
            'email': 'user2@test.com',
            'name': 'user2',
            'password': 'user2pass',
            'avatarURL': 'user2Avatar'
        }
        # Create another user
        another_user = self.create_sample_user(**payload)
        # Make delete request
        res = self.client.delete(user_delete_url(another_user.id))
        # Expect status 403
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        # Expect another_user still exist
        user_exist = get_user_model().objects.\
            filter(id=another_user.id).exists()
        self.assertTrue(user_exist)
