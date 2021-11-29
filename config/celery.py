import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
celery_app = Celery('config')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

celery_app.conf.task_routes = {
    'users.tasks.send_email': {'queue': 'emails'}
}

celery_app.conf.timezone = 'Europe/Moscow'

celery_app.conf.beat_schedule = {
    'process_initial_notifications_about_new_users': {
        'task': 'users.tasks.process_initial_notifications_about_new_users',
        'schedule': crontab(minute='*/2'),
    },
}
