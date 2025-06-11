# DjangoEmumbaTrainingApplication/celery.py
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoEmumbaTrainingProject.settings')

app = Celery('DjangoEmumbaTrainingProject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-task-reminders-every-day-8am': {
        'task': 'DjangoEmumbaTrainingApplication.tasks.send_task_reminders',
        'schedule': crontab(hour=13, minute=30),
    },
}