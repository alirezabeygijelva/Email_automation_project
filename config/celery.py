from django.conf import settings
import os
import django
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'write_in_file': {
        'task': 'EmailAutomationBot.tasks.get_emails',
        'schedule': 300,
        'options': {
            'expires': 10,
        }
    }

}


