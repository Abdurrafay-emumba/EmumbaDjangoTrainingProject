from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from DjangoEmumbaTrainingApplication.models import OurUser

User = get_user_model()

class GetUsersAPITestCase(APITestCase):
    def setUp(self):

        # Deleting users if already exist ( we will create them anew for the unit test)
        for i in range(20):
            try:
                # Checking to see if a user is not already registered by this email
                temp_user = OurUser.objects.get(email=f'test_user{i}@test_example.com')
                # If a user having our test email exist, then delete it, as we will be registering a user with this email
                temp_user.delete()
            except Exception as e:
                # If there is no user with that email then good
                pass

            try:
                # Checking to see if a user is not already registered by this username
                temp_user = OurUser.objects.get(username=f'test_user{i}')
                # If a user having our username exist, then delete it, as we will be registering a user with this username
                temp_user.delete()
            except Exception as e:
                # If there is no user with that username then good
                pass

        # Creating some test users
        for i in range(20):
            self.user = OurUser.objects.create_user(
                username=f'test_user{i}',
                email=f'test_user{i}@test_example.com',
                password='pass1234',
                first_name='0',
                last_name='9'
            )

        self.url = reverse('get_users')
        self.login_url = reverse('login_user')
        self.logout_url = reverse('logout_user')

    def test_get_users_authenticated(self):
        """
        Function Description: This is a POSITIVE test case. We will login a user and call the API. It should return us the results
        """

        # Log in the user first using the login endpoint
        login_response = self.client.post(self.login_url, {
            'username': 'test_user0',
            'password': 'pass1234'
        }, format='json')

        # Ensure login worked
        self.assertEqual(login_response.status_code, 200,
                         msg='Login Should have worked')
        self.assertIn('_auth_user_id', self.client.session,
                      msg = 'Session should have been established')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_get_users_unauthenticated(self):
        """
        Function Description: This is a NEGATIVE test case. Since this API requires user login, it should not work.
        The unauthenticated users should receive 401.
        """

        # Calling logout (in case there was a user logged in)
        logout_response = self.client.post(self.logout_url)
        # Session should be cleared
        self.assertNotIn('_auth_user_id', self.client.session)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_pagination_limit(self):
        """
        Function Description: This is a POSITIVE test case, here we will check if the page pagination limit of 10 is being respected -
        - or not
        """

        # Log in the user first using the login endpoint
        login_response = self.client.post(self.login_url, {
            'username': 'test_user0',
            'password': 'pass1234'
        }, format='json')

        # Ensure login worked
        self.assertEqual(login_response.status_code, 200)
        self.assertIn('_auth_user_id', self.client.session)

        # First page
        response = self.client.get(self.url)
        # Check if pagination limit is applied (e.g., 10 per page)
        self.assertLessEqual(len(response.data['results']), 10)

        # We have enough created users in the setup to trigger pagination (2nd Page)
        response = self.client.get(f"{self.url}?page=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
