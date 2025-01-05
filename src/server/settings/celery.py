from __future__ import absolute_import, unicode_literals
import os
import sys

from .base import CELERY_DISCOVER_TASKS

from celery import Celery
from celery.schedules import timedelta


sys.path.append('/app/src')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings.base')

app = Celery('bank-parser')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(CELERY_DISCOVER_TASKS)

app.conf.beat_schedule = {
    'change_account_status': {
        'task': 'server.tasks.account_tasks.change_account_status_task',
        'schedule': timedelta(minutes=1),
    },
    'delete_account_status': {
        'task': 'server.tasks.account_tasks.delete_account_task',
        'schedule': timedelta(minutes=10),
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
