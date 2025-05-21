from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from DjangoEmumbaTrainingApplication.models import OurUser, Task

class SimilarTaskTestCase(APITestCase):
    def setUp(self):
        self.username = 'similaruser'
        self.email = 'similar@example.com'
        self.password = 'pass1234'

        self.user = OurUser.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

        self.login_url = reverse('login_user')
        self.logout_url = reverse('logout_user')
        self.similar_task_url = reverse('similar_tasks')

    def tearDown(self):
        Task.objects.all().delete()
        self.user.delete()

    def test_similar_tasks_found(self):
        """
        Function Description: This is a POSITIVE Test Case Where a logged in user similar tasks are identified correctly"
        :return:
        """

        # Log in the user
        login_response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK,
                         msg="The user should have been logged in")

        Task.objects.create(
            title='Task A',
            description='Fix bugs in code',
            due_date=timezone.now().date(),
            start_date=timezone.now().date(),
            user_id=self.user
        )
        Task.objects.create(
            title='Task B',
            description='Fix bugs',
            due_date=timezone.now().date(),
            start_date=timezone.now().date(),
            user_id=self.user
        )

        response = self.client.get(self.similar_task_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertIn('task_1', response.data['results'][0])
        self.assertIn('task_2', response.data['results'][0])

    def test_no_similar_tasks(self):
        """
        Function Description: This is a POSITIVE Test Case Where a logged in user's no tasks are similar"
        :return:
        """

        # Log in the user
        login_response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK,
                         msg="The user should have been logged in")

        Task.objects.create(
            title='Task A',
            description='Write documentation',
            due_date=timezone.now().date(),
            start_date=timezone.now().date(),
            user_id=self.user
        )
        Task.objects.create(
            title='Task B',
            description='Fix bugs in backend',
            due_date=timezone.now().date(),
            start_date=timezone.now().date(),
            user_id=self.user
        )

        response = self.client.get(self.similar_task_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])

    def test_one_task_only(self):
        """
        Function Description: This is a POSITIVE Test Case Where a logged in user's only one task exists (no pair possible)"
        :return:
        """

        # Log in the user
        login_response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK,
                         msg="The user should have been logged in")

        Task.objects.create(
            title='Task A',
            description='Write docs',
            due_date=timezone.now().date(),
            start_date=timezone.now().date(),
            user_id=self.user
        )

        response = self.client.get(self.similar_task_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])

    def test_unauthenticated_user(self):
        """
        Function Description: This is a NEGATIVE Test Case Where a logged out user is rejected"
        :return:
        """
        # Logging out, just in case we are not logged in
        logout_response = self.client.post(self.logout_url)
        # Session should be cleared
        self.assertNotIn('_auth_user_id', self.client.session,
                         msg="There should be no session")


        response = self.client.get(self.similar_task_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
