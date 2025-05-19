from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from DjangoEmumbaTrainingApplication.models import OurUser

class UserLoginTestCase(APITestCase):

    def setUp(self):

        """
        Function Description: In this setup function, we will first delete any user having the same username or email -
        - as our test username and email.
        We do this to ensure that there will be no clash when we try to save our test user.
        :return:
        """

        # This is the setup function, it will run each time before a test case
        self.url = reverse('login_user')
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

    def test_user_login_username_successfully_API_response_check(self):
        """
        Test Case Description: This test case is a POSITIVE test case. It will log the user using the username and password

        :return: This should pass, if it fails then debug and see why it failed
        """
        data = {
            'username': self.test_username,
            'password': self.test_password
        }

        response = self.client.post(self.url, data, format='json')

        # On Successful login, following message will be displayed
        # return Response({"message": "Login successful!", "username": user.username}, status=status.HTTP_200_OK)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         'Status should have been status.HTTP_200_OK')
        self.assertIn('_auth_user_id', self.client.session,
                      'Session should had been establish')
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)

    def test_user_login_username_unsuccessfully_API_response_check(self):
        """
        Test Case Description: This test case is a NEGATIVE test case. It will try to log the user using the username
        and a wrong password

        :return: This should pass, if it fails then debug and see why it failed
        """
        data = {
            'username': self.test_username,
            'password': self.test_password + "1234"
        }

        response = self.client.post(self.url, data, format='json')

        # On unsuccessful login, following message will be displayed
        # return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         'Status should have been status.HTTP_401_UNAUTHORIZED')
        self.assertNotIn('_auth_user_id', self.client.session,
                      'Session should not had been establish')

    def test_user_login_email_successfully_API_response_check(self):
        """
        Test Case Description: This test case is a POSITIVE test case. It will log the user using the email and password

        :return: This should pass, if it fails then debug and see why it failed
        """
        data = {
            'username': self.test_email,
            'password': self.test_password
        }

        response = self.client.post(self.url, data, format='json')

        # On Successful login, following message will be displayed
        # return Response({"message": "Login successful!", "username": user.username}, status=status.HTTP_200_OK)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         'Status should have been status.HTTP_200_OK')
        self.assertIn('_auth_user_id', self.client.session,
                      'Session should had been establish')
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)

    def test_user_login_email_unsuccessfully_API_response_check(self):
        """
        Test Case Description: This test case is a NEGATIVE test case. It will log the user using the email and a wrong -
        - password

        :return: This should pass, if it fails then debug and see why it failed
        """
        data = {
            'username': self.test_email,
            'password': self.test_password + "1234"
        }

        response = self.client.post(self.url, data, format='json')

        # On unsuccessful login, following message will be displayed
        # return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         'Status should have been status.HTTP_401_UNAUTHORIZED')
        self.assertNotIn('_auth_user_id', self.client.session,
                         'Session should not had been establish')

    def test_user_login_wrong_username_or_email_unsuccessfully_API_response_check(self):
        """
        Test Case Description: This test case is a NEGATIVE test case. It will try to log the user using a wrong email or password

        :return: This should pass, if it fails then debug and see why it failed
        """
        data = {
            'username': " ",
            'password': self.test_password
        }

        response = self.client.post(self.url, data, format='json')

        # On unsuccessful login, following message will be displayed
        # return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         'Status should have been status.HTTP_401_UNAUTHORIZED')
        self.assertNotIn('_auth_user_id', self.client.session,
                         'Session should not had been establish')

    def test_user_login_incomplete_data_API_response_check(self):
        """
        Test Case Description: This test case is a NEGATIVE test case. It will log the user using incomplete data

        :return: This should pass, if it fails then debug and see why it failed
        """
        data = {
            # 'username': self.test_email,
            'password': self.test_password
        }

        response = self.client.post(self.url, data, format='json')

        # On incomplete data received, following message will be displayed
        # return Response({"error": "Username (or Email) and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         'Status should have been status.HTTP_400_BAD_REQUEST')
        self.assertNotIn('_auth_user_id', self.client.session,
                         'Session should not had been establish')