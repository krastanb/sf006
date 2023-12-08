import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sf06.settings')

app = Celery('sf06')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()