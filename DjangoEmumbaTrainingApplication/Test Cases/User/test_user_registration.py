from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from DjangoEmumbaTrainingApplication.models import OurUser

class UserRegistrationTestCase(APITestCase):
    """
    IMPORTANT: Django by default surpresses email sending during unit testing, so verification emails will not -
    - be sent during unit testing.
    """

    def setUp(self):
        # This is the setup function, it will run each time before a test case
        self.url = reverse('register_user')
        self.test_email = 'abdurrafay0610@gmail.com'
        self.test_username = 'testuser645363452542'

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

    def test_register_user_successfully_API_response_check(self):
        """
        Test Case Description: This test case is a POSITIVE test case. It will register a new user, using the register
        - API. It will only check for the positive response from API

        :return: This should pass, if it fails then debug and see why it failed
        """
        data = {
            'username': self.test_username,
            'email': self.test_email,
            'password': 'StrongPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post(self.url, data, format='json')

        # This is the response of our API on successful user registration
        # return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         msg = "Status should have been status.HTTP_201_CREATED")
        self.assertEqual(response.data['message'], 'User registered successfully',
                         msg = "The message should have been User registered successfully")

    def test_register_user_successfully_database_check(self):
        """
        Test Case Description: This test case is a POSITIVE test case. It will register a new user, using the register
        - API. It will only check for the data integrity in the database

        :return: This should pass, if it fails then debug and see why it failed
        """
        data = {
            'username': self.test_username,
            'email': self.test_email,
            'password': 'StrongPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }

        # Calling the API registering the user
        response = self.client.post(self.url, data, format='json')

        try:
            #  Check user in DB
            user = OurUser.objects.get(email=self.test_email)
            # The username should match with the one we registered with
            self.assertEqual(user.username, self.test_username,
                             msg = "The username should match with the one we registered with")
            # The email should not be verified on registration, it should be false
            self.assertFalse(user.is_email_verified,
                             msg = "The email should not be verified on registration, it should be false")
            # THe account creation date should be same as today
            self.assertEqual(user.account_date_creation, timezone.now().date(),
                             msg = "The account creation date should be same as today")
        except Exception as e:
            # If an exception was thrown, it means that django was not able to find the newly created user
            # So, writing an assert that will always throw
            self.assertEqual(True,False,
                             msg = "Exception was thrown, it means that user was not created successfully: " + str(e))

    def test_register_user_incomplete_data_API_response_check1(self):
        """
        Test Case Description: This test case is a NEGATIVE test case. It will send incomplete data to try and register a new user,
        - using the register API. It will only check for the negative response from API

        :return: This should pass, if it fails then debug and see why it failed
        """

        # Removing a major required field (username) from our data
        data = {
            # 'username': self.test_username,
            'email': self.test_email,
            'password': 'StrongPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post(self.url, data, format='json')

        # This is the response of our API on unsuccessful user registration
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         msg = "Username was not provided. Status should have been status.HTTP_400_BAD_REQUEST")

    def test_register_user_incomplete_data_response_check2(self):
        """
        Test Case Description: This test case is a NEGATIVE test case. It will send incomplete data to try and register a new user,
        - using the register API. It will only check for the negative response from API

        :return: This should pass, if it fails then debug and see why it failed
        """

        # Removing a major required field (email) from our data
        data = {
            'username': self.test_username,
            # 'email': self.test_email,
            'password': 'StrongPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post(self.url, data, format='json')

        # This is the response of our API on unsuccessful user registration
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         msg = "Email was not provided. Status should have been status.HTTP_400_BAD_REQUEST")

    def test_register_user_incomplete_data_response_check3(self):
        """
        Test Case Description: This test case is a NEGATIVE test case. It will send incomplete data to try and register a new user,
        - using the register API. It will only check for the negative response from API

        :return: This should pass, if it fails then debug and see why it failed
        """

        # Removing a major required field (password) from our data
        data = {
            'username': self.test_username,
            'email': self.test_email,
            # 'password': 'StrongPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post(self.url, data, format='json')

        # This is the response of our API on unsuccessful user registration
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         msg = "password was not provided. Status should have been status.HTTP_400_BAD_REQUEST")

    def test_register_user_incomplete_data_response_check4(self):
        """
        Test Case Description: This test case is a POSITIVE test case. It will send incomplete data to try and register a new user,
        - using the register API. It will only check for the negative response from API. It will exclude the minor fields:
            1) first_name
            2) last_name

            Which are not required

        :return: This should pass, if it fails then debug and see why it failed
        """

        # Removing the minor fields first_name and last_name from our data
        data = {
            'username': self.test_username,
            'email': self.test_email,
            'password': 'StrongPass123!',
            # 'first_name': 'Test',
            # 'last_name': 'User'
        }

        response = self.client.post(self.url, data, format='json')

        # This is the response of our API on successful user registration
        # return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         msg = "first_name and last_name was not provided. Status should have been status.HTTP_201_CREATED, as they are not required fields")


    def test_register_duplicate_email_API_response_check(self):
        """
        Test Case Description: This test case is a NEGATIVE test case. It will register a new user, and then -
        - register another user with the same email.

        :return: This should pass, if it fails then debug and see why it failed
        """
        data = {
            'username': self.test_username,
            'email': self.test_email,
            'password': 'StrongPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post(self.url, data, format='json')

        # This is the response of our API on successful user registration
        # return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         msg = "Status should have been status.HTTP_201_CREATED")
        self.assertEqual(response.data['message'], 'User registered successfully',
                         msg = "The message should have been User registered successfully")

        # Re-again registering the user, with the same email. But everything else is different
        data = {
            'username': 'Random user name59307847q',
            'email': self.test_email,
            'password': 'Random password 5809374903 74',
            'first_name': 'random first name 58q0375809q87',
            'last_name': 'random last anem 5iq-95-q909'
        }

        response = self.client.post(self.url, data, format='json')

        # This is the response of our API on unsuccessful user registration
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         msg="password was not provided. Status should have been status.HTTP_400_BAD_REQUEST")

    def test_register_duplicate_username_API_response_check(self):
        """
        Test Case Description: This test case is a NEGATIVE test case. It will register a new user, and then -
        - register another user with the same username.

        :return: This should pass, if it fails then debug and see why it failed
        """
        data = {
            'username': self.test_username,
            'email': self.test_email,
            'password': 'StrongPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post(self.url, data, format='json')

        # This is the response of our API on successful user registration
        # return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         msg = "Status should have been status.HTTP_201_CREATED")
        self.assertEqual(response.data['message'], 'User registered successfully',
                         msg = "The message should have been User registered successfully")

        # Re-again registering the user, with the same email. But everything else is different
        data = {
            'username': self.test_username,
            'email': 'RandomEmail59q375908@gmail.com',
            'password': 'Random password 5809374903 74',
            'first_name': 'random first name 58q0375809q87',
            'last_name': 'random last anem 5iq-95-q909'
        }

        response = self.client.post(self.url, data, format='json')

        # This is the response of our API on unsuccessful user registration
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         msg="password was not provided. Status should have been status.HTTP_400_BAD_REQUEST")

# TODO :: Add more test cases, for example, if the API does indeed return HTTP_400_BAD_REQUEST, make sure that the data was not saved in the database