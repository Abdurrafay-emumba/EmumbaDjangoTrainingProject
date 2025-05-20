from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from DjangoEmumbaTrainingApplication.models import OurUser

class UserLogOutTestCase(APITestCase):

    def setUp(self):

        """
        Function Description: In this setup function, we will first delete any user having the same username or email -
        - as our test username and email.
        We do this to ensure that there will be no clash when we try to save our test user and then use these credentials -
        - to login
        :return:
        """

        # This is the setup function, it will run each time before a test case
        self.login_url = reverse('login_user')
        self.logout_url = reverse('logout_user')

        self.test_email = 'abdurrafay0610@gmail.com'
        self.test_username = 'testuser645363452542'
        self.test_password = 'secure@1234'
        self.test_first_name = 'first'
        self.test_last_name = 'last'

        try:
            # Checking to see if a user is not already registered by this email
            temp_user = OurUser.objects.get(email=self.test_email)
            # If a user having our test email exist, then delete it, as we will be registering a user with this email
            temp_user.delete()
        except Exception as e:
            # If there is no user with that email then good
            pass

        try:
            # Checking to see if a user is not already registered by this username
            temp_user = OurUser.objects.get(username=self.test_username)
            # If a user having our username exist, then delete it, as we will be registering a user with this username
            temp_user.delete()
        except Exception as e:
            # If there is no user with that username then good
            pass

        # Creating the user, so that we can use these credentials to login
        self.user = OurUser.objects.create_user(
            username=self.test_username ,
            email=self.test_email,
            password=self.test_password,
            first_name=self.test_first_name,
            last_name=self.test_last_name
        )

    def tearDown(self):
        # This function will run each time after a test case is executed
        # Clean up: Delete the user after each test
        try:
            # Checking to see if a user is already registered by this email
            temp_user = OurUser.objects.get(email=self.test_email)
            # If a user having our test email exist, then delete it
            temp_user.delete()
        except Exception as e:
            # If there is no user with that email then good
            pass

        try:
            # Checking to see if a user is not already registered by this username
            temp_user = OurUser.objects.get(username=self.test_username)
            # If a user having our username exist, then delete it
            temp_user.delete()
        except Exception as e:
            # If there is no user with that username then good
            pass

    def test_logout_clears_session(self):

        """
        Function Description: This is a POSITIVE test case. It will first login our client and then log it out
        :return:
        """

        # Log in the user first using the login endpoint
        login_response = self.client.post(self.login_url, {
            'username': self.test_username,
            'password': self.test_password
        }, format='json')

        # Ensure login worked
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('_auth_user_id', self.client.session)

        # Now call logout
        logout_response = self.client.post(self.logout_url)

        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        self.assertIn('Logout successful', logout_response.json()['message'])

        # Session should be cleared
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_logout_requires_authentication(self):
        """
        Function Description: This is a NEGATIVE test case. We are calling the logout function, without any session being logged in
        :return:
        """
        # Fresh client without login
        new_client = self.client_class()
        response = new_client.post(self.logout_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Because IsAuthenticated is required