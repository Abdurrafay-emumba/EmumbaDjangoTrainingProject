from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from DjangoEmumbaTrainingApplication.models import OurUser, Task

class TaskOpenedEveryDayReportTestCase(APITestCase):
    def setUp(self):
        self.username = 'weekdayuser'
        self.email = 'weekday@example.com'
        self.password = 'testpass123'
        self.user = OurUser.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )
        self.login_url = reverse('login_user')
        self.logout_url = reverse('logout_user')
        self.report_url = reverse('Report 5')

    def tearDown(self):
        Task.objects.all().delete()
        self.user.delete()

    def test_task_opened_every_day_success(self):
        # Log in the user
        login_response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        today = timezone.now().date()
        # Create tasks on different days
        Task.objects.create(
            title='Task Mon',
            description='Monday task',
            start_date=today - timedelta(days=today.weekday()),  # Monday
            due_date=today,
            user_id=self.user
        )
        Task.objects.create(
            title='Task Tue',
            description='Tuesday task',
            start_date=today - timedelta(days=today.weekday() - 1),  # Tuesday
            due_date=today,
            user_id=self.user
        )
        Task.objects.create(
            title='Task Mon 2',
            description='Another Monday task',
            start_date=today - timedelta(days=today.weekday()),  # Monday
            due_date=today,
            user_id=self.user
        )

        response = self.client.get(self.report_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return a list of dicts with weekday and task_count
        weekdays = {item['weekday']: item['task_count'] for item in response.data}
        self.assertIn(2, weekdays.values())  # Monday has 2 tasks
        self.assertIn(1, weekdays.values())  # Tuesday has 1 task

    def test_task_opened_every_day_empty(self):
        # Log in the user
        login_response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        # No tasks created
        response = self.client.get(self.report_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data), [])

    def test_task_opened_every_day_unauthenticated(self):
        # Ensure logged out
        self.client.post(self.logout_url)
        response = self.client.get(self.report_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)