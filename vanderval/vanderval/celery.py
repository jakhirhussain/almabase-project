import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vanderval.settings')

app = Celery('vanderval')

app.conf.task_queues = {
    'high_priority': {
        'exchange': 'default',
        'routing_key': 'high_priority',
    },
    'medium_priority': {
        'exchange': 'default',
        'routing_key': 'medium_priority',
    },
    'low_priority': {
        'exchange': 'default',
        'routing_key': 'low_priority',
    },
}

app.conf.task_default_queue = 'low_priority'
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
