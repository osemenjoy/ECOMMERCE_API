import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

# Create an instance of the Celery class with the name 'main'.
celery_app = Celery("main")

# Load task modules from all registered Django app configs.
celery_app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from installed apps.
celery_app.autodiscover_tasks()
