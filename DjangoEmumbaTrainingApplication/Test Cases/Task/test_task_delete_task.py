from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from DjangoEmumbaTrainingApplication.models import OurUser, Task

class MarkTaskCompleteTestCase(APITestCase):
    def setUp(self):
        self.login_url = reverse('login_user')
        self.logout_url = reverse('logout_user')

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

        self.delete_task_url = reverse('delete_task', args=[self.task.id])

    def tearDown(self):
        Task.objects.all().delete()
        OurUser.objects.all().delete()

    def test_delete_task_successfully(self):

        """
        Function Description: This is a POSITIVE test case. In this a logged in user will delete his task
        :return:
        """

        # Login first
        login_response = self.client.post(self.login_url, {
            'username': self.user.username,
            'password': 'securepass123'
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK,
                         msg="The user should have been logged in")

        response = self.client.delete(self.delete_task_url)

        # This is the API response on successful deletion
        # return Response({"message": "Task deleted successfully."}, status=status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Task deleted successfully.")

        # Checking the database
        self.assertEqual(Task.objects.count(), 0)

    def test_delete_nonexistent_task(self):

        """
        Function Description: This is a NEGATIVE test case. In this a logged in user will delete his non existent task
        :return:
        """

        # Login first
        login_response = self.client.post(self.login_url, {
            'username': self.user.username,
            'password': 'securepass123'
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK,
                         msg="The user should have been logged in")

        invalid_url = reverse('delete_task', args=[self.task.id+1])  # Since we only have 1 task, task.id+1 should not exist
        response = self.client.delete(invalid_url)
        # This is the API unsuccessful deletion
        # return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "Task not found.")

    def test_delete_task_unauthenticated(self):

        """
        Function Description: This is a NEGATIVE test case. In this a logged out user will try to delete his task
        :return:
        """

        # Logging out, just in case we are not logged in
        logout_response = self.client.post(self.logout_url)
        # Session should be cleared
        self.assertNotIn('_auth_user_id', self.client.session,
                         msg="There should be no session")

        response = self.client.delete(self.delete_task_url)

        response = self.client.delete(self.delete_task_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)