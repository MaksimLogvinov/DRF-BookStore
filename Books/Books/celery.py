import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Books.settings')

app = Celery('Books', include=['apps.orders.tasks'])
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
