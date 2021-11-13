import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
celery_app = Celery('config')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()


celery_app.conf.beat_schedule = {
    'cancel_registration': {
        'task': 'users.tasks.cancel_registration',
        'schedule': crontab(minute='*/1'),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
    },
}