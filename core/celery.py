import os

import environ
from celery import Celery

# Initialize environment variables
env = environ.Env()

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Initialize Celery
app = Celery("core")

# Broker and result backend configuration
app.conf.broker_url = env("CELERY_BROKER_URL")
app.conf.result_backend = env("CELERY_RESULT_BACKEND")

# Load settings from Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
