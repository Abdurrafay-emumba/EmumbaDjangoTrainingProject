from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from DjangoEmumbaTrainingApplication.models import OurUser, Task
from unittest.mock import patch

class TaskOpenedEveryDay2ReportTestCase(APITestCase):
    def setUp(self):
        self.username = 'user2'
        self.email = 'user2@example.com'
        self.password = 'testpass123'
        self.user = OurUser.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )
        self.login_url = reverse('login_user')
        self.logout_url = reverse('logout_user')
        self.report_url = reverse('Report 6')

    def tearDown(self):
        Task.objects.all().delete()
        self.user.delete()

    def test_task_opened_every_day2_success(self):
        self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        }, format='json')

        today = timezone.now().date()
        Task.objects.create(
            title='Task 1',
            description='Task 1',
            start_date=today - timedelta(days=2),
            due_date=today,
            user_id=self.user
        )
        Task.objects.create(
            title='Task 2',
            description='Task 2',
            start_date=today - timedelta(days=2),
            due_date=today,
            user_id=self.user
        )
        Task.objects.create(
            title='Task 3',
            description='Task 3',
            start_date=today - timedelta(days=1),
            due_date=today,
            user_id=self.user
        )

        response = self.client.get(self.report_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return a list of dicts with start_date and task_count
        dates = {item['start_date']: item['task_count'] for item in response.data}
        self.assertIn((today - timedelta(days=2)), dates)
        self.assertEqual(dates[(today - timedelta(days=2))], 2)
        self.assertIn((today - timedelta(days=1)), dates)
        self.assertEqual(dates[(today - timedelta(days=1))], 1)

    def test_task_opened_every_day2_empty(self):
        self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        }, format='json')

        response = self.client.get(self.report_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data), [])

    def test_task_opened_every_day2_unauthenticated(self):
        self.client.post(self.logout_url)
        response = self.client.get(self.report_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_task_opened_every_day2_exception(self):
        self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        }, format='json')
        with patch('DjangoEmumbaTrainingApplication.views.Task.objects') as mock_tasks:
            mock_tasks.filter.side_effect = Exception('Test exception')
            response = self.client.get(self.report_url)
            self.assertIn('Exception occurred', response.data)