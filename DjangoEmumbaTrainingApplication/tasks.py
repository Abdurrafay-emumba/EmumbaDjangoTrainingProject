# DjangoEmumbaTrainingApplication/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from DjangoEmumbaTrainingApplication.models import OurUser, Task

@shared_task
def async_send_mail(subject, message, recipient_email):
    send_mail(subject, message, 'noreply@example.com', [recipient_email])


@shared_task
def send_task_reminders():
    tomorrow = timezone.now().date() + timedelta(days=1)

    users = OurUser.objects.all()

    for user in users:
        tasks = Task.objects.filter(
            user_id=user,
            completion_status=False,
            due_date=tomorrow
        )

        if tasks.exists():
            task_list = '\n'.join([f"- {task.title}: {task.description}" for task in tasks])
            subject = "Task Reminder: Tasks Due Tomorrow"
            message = f"Hi {user.username},\n\nYou have the following tasks due tomorrow:\n\n{task_list}"
            send_mail(subject, message, 'noreply@example.com', [user.email])