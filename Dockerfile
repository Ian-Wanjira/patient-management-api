# Base Python image with dependencies for the build stages
FROM python:3.12-slim AS base

# Set up environment and working directory
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/local/app

# Install system dependencies and Python dependencies early for caching
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Build dependencies separately for caching
FROM base AS dependencies

# Copy the requirements file to install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN gunicorn --version

# Final stage for Django application image
FROM base AS django

# Copy the dependencies from the previous stage
COPY --from=dependencies /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=dependencies /usr/local/bin/gunicorn /usr/local/bin/gunicorn

# Copy the application source code
COPY . .

# Set permissions and create non-root user
RUN useradd -m app && chown -R app /usr/local/app
USER app

# Expose the application port
EXPOSE 8000

# Command to run the Django server with Gunicorn
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Final stage for Celery worker image
FROM base AS celery

# Copy the dependencies from the previous stage
COPY --from=dependencies /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=dependencies /usr/local/bin/celery /usr/local/bin/celery

# Copy the application source code
COPY . .

# Set permissions and create non-root user
RUN useradd -m app && chown -R app /usr/local/app
USER app

# Command to run the Celery worker
CMD ["celery", "-A", "core", "worker", "-l", "info"]
