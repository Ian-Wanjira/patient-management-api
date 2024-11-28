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

# SSL settings for Redis
if app.conf.broker_url.startswith("rediss://"):
    app.conf.broker_use_ssl = {"ssl_cert_reqs": "CERT_NONE"}
if app.conf.result_backend.startswith("rediss://"):
    app.conf.redis_backend_use_ssl = {"ssl_cert_reqs": "CERT_NONE"}

# Load settings from Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
