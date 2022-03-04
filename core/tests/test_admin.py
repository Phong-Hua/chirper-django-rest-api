from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    # Setup before test
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@test.com',
            password='password123',
            name='admin',
        )

        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user1@test.com',
            password='password123',
            name='user1',
            avatarURL='user1_avatar'
        )

    def test_users_listed(self):
        """
        Test that users are listed on user page.
        """
        # Refer to this document
        # https://docs.djangoproject.com/en/2.1/ref/contrib/admin/#reversing-admin-urls
        # for reverse admin
        # core is the app name, userprofile is UserProfile model
        url = reverse('admin:core_userprofile_changelist')
        res = self.client.get(url)
        # Check the http response 200
        # And response contains certain items: name, email, avatarURL
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.avatarURL)

    def test_user_change_page(self):
        """
        Test that user edit page works
        """

        url = reverse('admin:core_userprofile_change', args=[self.user.id])
        res = self.client.get(url)

        # Test status code
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """
        Test that create user page works
        """
        url = reverse('admin:core_userprofile_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
