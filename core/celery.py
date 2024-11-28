import os

import environ
from celery import Celery

env = environ.Env()

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

app.conf.broker_url = env("CELERY_BROKER_URL")
app.conf.result_backend = env("CELERY_RESULT_BACKEND")

app.conf.broker_use_ssl = {"ssl_cert_reqs": "CERT_NONE"}
app.conf.redis_backend_use_ssl = {"ssl_cert_reqs": "CERT_NONE"}

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
