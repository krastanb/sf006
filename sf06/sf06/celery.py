import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sf06.settings')

app = Celery('sf06')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'weekly_subs': {
        'task': 'news.tasks.every_week_mails', # название таска
        'schedule': crontab(), # период в секундах
    },
}