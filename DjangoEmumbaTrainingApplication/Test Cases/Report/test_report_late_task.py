from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from DjangoEmumbaTrainingApplication.models import OurUser, Task

class LateTaskReportTestCase(APITestCase):
    def setUp(self):
        self.username = 'lateuser'
        self.email = 'late@example.com'
        self.password = 'testpass123'
        self.user = OurUser.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
            account_date_creation=timezone.now().date() - timedelta(days=10)
        )
        self.login_url = reverse('login_user')
        self.logout_url = reverse('logout_user')
        self.report_url = reverse('Report 3')

    def tearDown(self):
        Task.objects.all().delete()
        self.user.delete()

    def test_late_task_report_with_late_tasks(self):
        # Log in the user
        login_response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        today = timezone.now().date()

        # Task completed after due date (late)
        Task.objects.create(
            title='Late Completed',
            description='Completed late',
            start_date=today - timedelta(days=5),
            due_date=today - timedelta(days=3),
            completion_status=True,
            completion_date=today - timedelta(days=1),
            user_id=self.user
        )
        # Task not completed and overdue (late)
        Task.objects.create(
            title='Overdue Incomplete',
            description='Still not done',
            start_date=today - timedelta(days=7),
            due_date=today - timedelta(days=2),
            completion_status=False,
            completion_date=None,
            user_id=self.user
        )
        # Task completed on time (not late)
        Task.objects.create(
            title='On Time',
            description='Done on time',
            start_date=today - timedelta(days=4),
            due_date=today - timedelta(days=2),
            completion_status=True,
            completion_date=today - timedelta(days=2),
            user_id=self.user
        )

        response = self.client.get(self.report_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_late_task_report_with_no_late_tasks(self):
        # Log in the user
        login_response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        today = timezone.now().date()

        # All tasks completed on time
        Task.objects.create(
            title='On Time 1',
            description='Done on time',
            start_date=today - timedelta(days=3),
            due_date=today - timedelta(days=2),
            completion_status=True,
            completion_date=today - timedelta(days=2),
            user_id=self.user
        )
        Task.objects.create(
            title='On Time 2',
            description='Done on time',
            start_date=today - timedelta(days=2),
            due_date=today - timedelta(days=1),
            completion_status=True,
            completion_date=today - timedelta(days=1),
            user_id=self.user
        )

        response = self.client.get(self.report_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_late_task_report_unauthenticated(self):
        # Log out the user
        # Logging out, just in case we are not logged in
        logout_response = self.client.post(self.logout_url)
        # Session should be cleared
        self.assertNotIn('_auth_user_id', self.client.session,
                         msg="There should be no session")

        response = self.client.get(self.report_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)