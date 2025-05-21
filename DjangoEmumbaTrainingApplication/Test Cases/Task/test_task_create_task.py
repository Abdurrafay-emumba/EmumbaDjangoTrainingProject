from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from DjangoEmumbaTrainingApplication.models import OurUser
from DjangoEmumbaTrainingApplication.models import Task

# TODO_DONE :: Why are these test not being registered?
# You need to keep the following things in mind for the test case to run
#   1) The directory in which you have the test case files must also have a __init__.py
#   2) The name of the file must be test_*.py or *_test.py
#   3) The test class name must be Test*
#   4) The test functions must start with test_*

class TestCreateTask(APITestCase):
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
        self.create_task_url = reverse('create_task')

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
        Task.objects.all().delete()

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

    def test_create_task_successful(self):
        """
        Function Description: This is a POSITIVE test case. In this function a logged in user, will create -
        - a task by providing all the relevant info
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

        # Create a task
        data = {
            "title": "Test Task",
            "description": "This is a test task.",
            "due_date": (timezone.now().date() + timezone.timedelta(days=7)).isoformat()
        }

        response = self.client.post(self.create_task_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Task created successfully")
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        self.assertEqual(task.title, data["title"])
        self.assertEqual(task.description, data["description"])
        self.assertEqual(task.user_id, self.user)

    def test_create_task_missing_field(self):
        """
        Function Description: This is a NEGATIVE test case. In this function a logged in user, will try to create -
        - a task with incomplete data
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

        data = {
            "description": "This task has no title.",
            "due_date": (timezone.now().date() + timezone.timedelta(days=7)).isoformat()
        }

        response = self.client.post(self.create_task_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_create_unauthorized_user(self):
        """
        Function Description: This is a NEGATIVE test case. In this function a logged out user, will try to create -
        - a task by providing all the relevant info
        :return:
        """

        # Calling logout (in case there was a user logged in)
        logout_response = self.client.post(self.logout_url)
        # Session should be cleared
        self.assertNotIn('_auth_user_id', self.client.session)

        # Create a task
        data = {
            "title": "Test Task",
            "description": "This is a test task.",
            "due_date": (timezone.now().date() + timezone.timedelta(days=7)).isoformat()
        }

        response = self.client.post(self.create_task_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



