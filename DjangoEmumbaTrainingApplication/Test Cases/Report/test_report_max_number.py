from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from DjangoEmumbaTrainingApplication.models import OurUser, Task

class MaxTaskCompletedDayReportTestCase(APITestCase):
    def setUp(self):
        self.username = 'maxuser'
        self.email = 'max@example.com'
        self.password = 'testpass123'
        self.user = OurUser.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
            account_date_creation=timezone.now().date() - timedelta(days=10)
        )
        self.login_url = reverse('login_user')
        self.logout_url = reverse('logout_user')
        self.report_url = reverse('Report 4')

    def tearDown(self):
        Task.objects.all().delete()
        self.user.delete()

    def test_max_task_completed_day_success(self):
        # Log in the user
        login_response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        today = timezone.now().date()
        # 2 tasks completed on the same day, 1 on another day
        Task.objects.create(
            title='Task 1',
            description='Desc 1',
            start_date=today - timedelta(days=3),
            due_date=today - timedelta(days=2),
            completion_status=True,
            completion_date=today - timedelta(days=1),
            user_id=self.user
        )
        Task.objects.create(
            title='Task 2',
            description='Desc 2',
            start_date=today - timedelta(days=4),
            due_date=today - timedelta(days=2),
            completion_status=True,
            completion_date=today - timedelta(days=1),
            user_id=self.user
        )
        Task.objects.create(
            title='Task 3',
            description='Desc 3',
            start_date=today - timedelta(days=5),
            due_date=today - timedelta(days=2),
            completion_status=True,
            completion_date=today - timedelta(days=2),
            user_id=self.user
        )

        response = self.client.get(self.report_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The day with 2 completions should be returned
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data['completion_date'], (today - timedelta(days=1)))
        self.assertEqual(response.data['task_count'], 2)

    def test_max_task_completed_day_zero_completed(self):
        """
        Function Description: This is a CORNER test case. In this test case a logged in user having 0 completed task -
        - will access this API and get an empty response.
        :return:
        """
        # Log in the user
        login_response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        today = timezone.now().date()
        # All tasks are incomplete
        Task.objects.create(
            title='Task 1',
            description='Desc 1',
            start_date=today - timedelta(days=3),
            due_date=today - timedelta(days=2),
            completion_status=False,
            user_id=self.user
        )
        Task.objects.create(
            title='Task 2',
            description='Desc 2',
            start_date=today - timedelta(days=4),
            due_date=today - timedelta(days=2),
            completion_status=False,
            user_id=self.user
        )

        response = self.client.get(self.report_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return None (no completed tasks)
        self.assertIsNone(response.data)

    def test_max_task_completed_day_zero_tasks(self):
        """
        Function Description: This is a CORNER test case. In this test case a logged in user having 0 task, will access this API -
        - and get an empty response.
        :return:
        """
        # Log in the user
        login_response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        # No tasks created
        response = self.client.get(self.report_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data)

    """
    def test_max_task_completed_day_user_deleted(self):
        """"""
        Function Description: This is a NEGATIVE test case. To throw the exception we will login the user and then delete him -
        - before calling the API. Such a behaviour should not be possible, but on the off-chance it does happen, then -
        - we are catering it.

        Django will lets the user login, but when we try to access the API, it searches for the user in the database -
        - does not find the user and does not let us use the API. Test case aborted.

        :return:
        """"""
        # Log in the user
        login_response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        # Delete the user after login
        self.user.delete()

        # Now call the API, which should raise an exception and return 500
        response = self.client.get(self.report_url)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('Exception occurred', response.data)
    """

    def test_max_task_completed_day_unauthenticated(self):
        # Log out the user
        # Logging out, just in case we are not logged in
        logout_response = self.client.post(self.logout_url)
        # Session should be cleared
        self.assertNotIn('_auth_user_id', self.client.session,
                         msg="There should be no session")

        response = self.client.get(self.report_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)