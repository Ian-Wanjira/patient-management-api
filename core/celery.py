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

# Explicit SSL configuration for Redis
app.conf.broker_transport_options = {
    "ssl": {
        "ssl_cert_reqs": None  # Use None for no validation or replace with "required" for CERT_REQUIRED
    }
}
app.conf.redis_backend_transport_options = {"ssl": {"ssl_cert_reqs": None}}

# Load settings from Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
