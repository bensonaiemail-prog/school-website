import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_system.settings')

app = Celery('school_system')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Celery Beat Schedule
app.conf.beat_schedule = {
    'send-fee-reminders-daily': {
        'task': 'results.tasks.send_fee_reminders',
        'schedule': crontab(hour=9, minute=0),  # Every day at 9 AM
    },
    'send-overdue-fee-alerts': {
        'task': 'results.tasks.send_overdue_fee_alerts',
        'schedule': crontab(hour=10, minute=0, day_of_week='monday'),  # Every Monday at 10 AM
    },
}