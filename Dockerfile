# Use a lightweight Python base image
FROM python:3.11-slim

# Prevent Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y libpq-dev gcc --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . /app

# Ensure settings module is visible to Django
ENV DJANGO_SETTINGS_MODULE=core.settings

# Collect static files and apply migrations
RUN python manage.py collectstatic --no-input && \
    python manage.py migrate

# Start the application
CMD ["daphne", "core.asgi:application", "-b", "0.0.0.0", "-p", "8001"]
