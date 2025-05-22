import io
import csv
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from DjangoEmumbaTrainingApplication.models import OurUser, Task

class TaskStatusReportTestCase(APITestCase):
    def setUp(self):
        self.username = 'reportuser'
        self.email = 'report@example.com'
        self.password = 'testpass123'
        self.user = OurUser.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )
        self.login_url = reverse('login_user')
        self.logout_url = reverse('logout_user')
        self.report_url = reverse('Report 1')

    def tearDown(self):
        Task.objects.all().delete()
        self.user.delete()

    def test_get_task_status_report(self):
        """
        Function Description: This is a POSITIVE test case. In this test case a logged in user will get his task status report.
        We will add a few tasks to the database and then check if the report is generated correctly.
        :return:
        """
        # Log in the user
        login_response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        # Create tasks: 2 completed, 1 incomplete
        Task.objects.create(
            title='Task 1',
            description='Desc 1',
            due_date=timezone.now().date(),
            start_date=timezone.now().date(),
            completion_status=True,
            completion_date=timezone.now().date(),
            user_id=self.user
        )
        Task.objects.create(
            title='Task 2',
            description='Desc 2',
            due_date=timezone.now().date(),
            start_date=timezone.now().date(),
            completion_status=True,
            completion_date=timezone.now().date(),
            user_id=self.user
        )
        Task.objects.create(
            title='Task 3',
            description='Desc 3',
            due_date=timezone.now().date(),
            start_date=timezone.now().date(),
            completion_status=False,
            user_id=self.user
        )

        response = self.client.get(self.report_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'text/csv')

        # Parse CSV content
        content = response.content.decode('utf-8')
        csv_reader = csv.reader(io.StringIO(content))
        rows = list(csv_reader)
        self.assertEqual(rows[0], ['Total tasks', 'Completed Task', 'Incompleted Task'])
        self.assertEqual(rows[1], ['3', '2', '1'])

    def test_get_task_status_report_unsuccessful(self):
        """
        Function Description: This is a NEGATIVE test case. In this test case a logged out user will try to get his task status report.
        :return:
        """

        # Logging out, just in case we are not logged in
        logout_response = self.client.post(self.logout_url)
        # Session should be cleared
        self.assertNotIn('_auth_user_id', self.client.session,
                         msg="There should be no session")

        # Create tasks: 2 completed, 1 incomplete
        Task.objects.create(
            title='Task 1',
            description='Desc 1',
            due_date=timezone.now().date(),
            start_date=timezone.now().date(),
            completion_status=True,
            completion_date=timezone.now().date(),
            user_id=self.user
        )
        Task.objects.create(
            title='Task 2',
            description='Desc 2',
            due_date=timezone.now().date(),
            start_date=timezone.now().date(),
            completion_status=True,
            completion_date=timezone.now().date(),
            user_id=self.user
        )
        Task.objects.create(
            title='Task 3',
            description='Desc 3',
            due_date=timezone.now().date(),
            start_date=timezone.now().date(),
            completion_status=False,
            user_id=self.user
        )

        response = self.client.get(self.report_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)