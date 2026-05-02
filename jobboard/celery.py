import os
from celery import Celery

# Tell Celery which Django settings to use
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobboard.settings')

app = Celery('jobboard')

# Read Celery config from Django settings
# namespace='CELERY' means all Celery settings in settings.py
# must start with CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto discover tasks from all installed apps
# So we don't need to manually import tasks
app.autodiscover_tasks()