from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from DjangoEmumbaTrainingApplication.models import OurUser, Task

class MarkTaskCompleteTestCase(APITestCase):
    def setUp(self):
        self.login_url = reverse('login_user')
        self.logout_url = reverse('logout_user')
        self.mark_task_complete_url = reverse('mark_task_complete')

        self.user = OurUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='securepass123'
        )

        self.task = Task.objects.create(
            user_id=self.user,
            title='Sample Task',
            description='A test task',
            due_date=timezone.now().date() + timezone.timedelta(days=5),
            start_date=timezone.now().date()
        )

    def tearDown(self):
        Task.objects.all().delete()
        OurUser.objects.all().delete()


    def test_mark_task_complete_success(self):
        """
        Function Description: This is a POSITIVE test case. In this our logged in user will mark one of his task complete
        :return:
        """

        # Login first
        login_response = self.client.post(self.login_url, {
            'username': self.user.username,
            'password': 'securepass123'
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK,
                         msg="The user should have been logged in")


        # Before sending the request, make sure the task is not completed
        self.assertFalse(self.task.completion_status,
                         msg="Task should not be completed right now. We are yet to invoke the API")


        # Send PATCH request
        response = self.client.patch(self.mark_task_complete_url, {
            'id': self.task.id
        }, format='json')

        # On success API returns
        # return Response({"message": "Task marked as complete"}, status=status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK, "The API should have given HTTP_200_OK")
        self.assertEqual(response.data['message'], 'Task marked as complete', "")

        # Checking to see if the completion_status changed in the database
        self.task.refresh_from_db()
        self.assertTrue(self.task.completion_status)
        self.assertIsNotNone(self.task.completion_date)

    def test_mark_task_complete_logout_unsuccess(self):
        """
        Function Description: This is a NEGATIVE test case. In this our logged out user will try to mark one of his task complete
        :return:
        """

        # Logging out, just in case we are not logged in
        logout_response = self.client.post(self.logout_url)
        # Session should be cleared
        self.assertNotIn('_auth_user_id', self.client.session,
                         msg="There should be no session")

        # Before sending the request, make sure the task is not completed
        self.assertFalse(self.task.completion_status,
                         msg="Task should not be completed right now. We are yet to invoke the API")


        # Send PATCH request
        response = self.client.patch(self.mark_task_complete_url, {
            'id': self.task.id
        }, format='json')

        # Since we are logged out, it should give us unauthorized msg
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         "The API should have given HTTP_403_FORBIDDEN, because authentication is required")

        # Checking to see if the completion_status changed in the database
        self.task.refresh_from_db()
        self.assertFalse(self.task.completion_status)

    def test_mark_task_complete_invalid_task_id(self):
        """
        Function Description: This is a NEGATIVE test case. In this our logged in user will mark one of his invalid task complete
        :return:
        """

        # Login first
        login_response = self.client.post(self.login_url, {
            'username': self.user.username,
            'password': 'securepass123'
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK,
                         msg="The user should have been logged in")


        # Before sending the request, make sure the task is not completed
        self.assertFalse(self.task.completion_status,
                         msg="Task should not be completed right now. We are yet to invoke the API")

        # Use non-existing task ID
        response = self.client.patch(self.mark_task_complete_url, {
            'id': 9999
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

