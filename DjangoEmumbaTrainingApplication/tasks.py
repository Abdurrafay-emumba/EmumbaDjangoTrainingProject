# DjangoEmumbaTrainingApplication/tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def async_send_mail(subject, message, recipient_email):
    send_mail(subject, message, 'noreply@example.com', [recipient_email])
