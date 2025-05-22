import math
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from DjangoEmumbaTrainingApplication.models import OurUser, Task

class AverageTaskPerDayReportTestCase(APITestCase):
    def setUp(self):
        self.username = 'avguser'
        self.email = 'avg@example.com'
        self.password = 'testpass123'
        self.user = OurUser.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
            account_date_creation=timezone.now().date() - timedelta(days=4)
        )
        self.login_url = reverse('login_user')
        self.logout_url = reverse('logout_user')
        self.report_url = reverse('Report 2')

    def tearDown(self):
        Task.objects.all().delete()
        self.user.delete()

    def test_average_task_per_day_success(self):
        """
        Funtion Description: This is a POSITIVE test case. In this test case a logged in user will get the number of task
        he has completed on average.
        :return:
        """
        # Log in the user
        login_response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        # Create 4 completed tasks over 4 days
        for i in range(4):
            Task.objects.create(
                title=f'Task {i+1}',
                description='Test',
                due_date=timezone.now().date(),
                start_date=timezone.now().date() - timedelta(days=i),
                completion_status=True,
                completion_date=timezone.now().date() - timedelta(days=i),
                user_id=self.user
            )

        response = self.client.get(self.report_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Average task completed per day', response.data)
        # 4 tasks / 5 days (including today)
        self.assertTrue(math.isclose(response.data['Average task completed per day'], 0.8, rel_tol=1e-9))

    def test_average_task_per_day_zero_days(self):
        """
        Funtion Description: This is a CORNER test case. In this test case a logged in user having todays date as the creation date -
        - will try to get his average of task completed.
        Previously this test case failed because the number of days for a new user (a user having current date as the creation date) -
        - was being calculated to 0. Now we also include the current day in the days calculated.
        :return:
        """

        # Set account creation date to today
        self.user.account_date_creation = timezone.now().date()
        self.user.save()

        # Log in the user
        login_response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        # Create 2 completed tasks
        for i in range(2):
            Task.objects.create(
                title=f'Task {i+1}',
                description='Test',
                due_date=timezone.now().date(),
                start_date=timezone.now().date(),
                completion_status=True,
                completion_date=timezone.now().date(),
                user_id=self.user
            )

        response = self.client.get(self.report_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 2 tasks / 1 day
        self.assertIn('Average task completed per day', response.data)
        # Since our API returns a double value, we cannot just compare it with 2.0. So, rel_tol=1e-9 is used to defined -
        # - the relative tolerance for floating point comparisons.
        self.assertTrue(math.isclose(response.data['Average task completed per day'], 2.0, rel_tol=1e-9))

    def test_average_task_per_day_zero_days2(self):
        """
        Funtion Description: This is a NEGATIVE test case. In this test case a logged in user having tomorrows date as the
        - creation date will try to get his average of task completed. (Now, this case should not be possible, since -
        - our code does not allow a user to have a creation date in the future), but if someone manually added a user -
        - with a future date, this test case will check if the API handles it correctly. The API will not throw an exception -
        - but rather it will handle it and return an error response.
        :return:
        """

        # Set account creation date to tomorrow
        self.user.account_date_creation = timezone.now().date() + timedelta(days=1)
        self.user.save()

        # Log in the user
        login_response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        # Create 2 completed tasks
        for i in range(2):
            Task.objects.create(
                title=f'Task {i+1}',
                description='Test',
                due_date=timezone.now().date(),
                start_date=timezone.now().date(),
                completion_status=True,
                completion_date=timezone.now().date(),
                user_id=self.user
            )

        response = self.client.get(self.report_url)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


    def test_average_task_per_day_unauthenticated(self):
        """
        Function Description: This is a NEGATIVE testcase. In this test case a logged out user will try to access this API
        :return:
        """

        # Log out the user
        # Logging out, just in case we are not logged in
        logout_response = self.client.post(self.logout_url)
        # Session should be cleared
        self.assertNotIn('_auth_user_id', self.client.session,
                         msg="There should be no session")

        response = self.client.get(self.report_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)