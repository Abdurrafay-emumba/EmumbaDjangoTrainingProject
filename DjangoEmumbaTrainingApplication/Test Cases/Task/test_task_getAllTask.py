from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from DjangoEmumbaTrainingApplication.models import OurUser, Task

class GetAllTasksTestCase(APITestCase):
    def setUp(self):
        self.username = 'taskuser'
        self.email = 'taskuser@example.com'
        self.password = 'testpass123'

        self.user = OurUser.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

        self.login_url = reverse('login_user')
        self.logout_url = reverse('logout_user')
        self.get_all_tasks_url = reverse('getAllTask')

    def tearDown(self):
        Task.objects.all().delete()
        self.user.delete()

    def test_get_all_tasks_successfully(self):
        """
        Function Description: This is a POSITIVE test case. In this test case a logged in user, having task will get his -
        - paginated task
        :return:
        """

        # Log in the user
        login_response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK,
                         msg="The user should have been logged in")

        # Create 2 tasks for the user
        Task.objects.create(
            title='Task 1',
            description='Description 1',
            due_date=timezone.now().date(),
            start_date=timezone.now().date(),
            user_id=self.user
        )
        Task.objects.create(
            title='Task 2',
            description='Description 2',
            due_date=timezone.now().date(),
            start_date=timezone.now().date(),
            user_id=self.user
        )

        response = self.client.get(self.get_all_tasks_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['title'], 'Task 1')
        self.assertEqual(response.data['results'][1]['title'], 'Task 2')

    def test_get_all_tasks_empty(self):
        """
        Function Description: This is a POSITIVE test case. In this test case a logged in user, having task will get his -
        - paginated task (zero task)
        :return:
        """

        # Log in the user
        login_response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK,
                         msg="The user should have been logged in")

        response = self.client.get(self.get_all_tasks_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])

    def test_get_all_tasks_unauthenticated(self):
        """
       Function Description: This is a NEGATIVE test case. In this test case a logged out user will try having his task
       :return:
       """

        # Logging out, just in case we are not logged in
        logout_response = self.client.post(self.logout_url)
        # Session should be cleared
        self.assertNotIn('_auth_user_id', self.client.session,
                         msg="There should be no session")

        response = self.client.get(self.get_all_tasks_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)