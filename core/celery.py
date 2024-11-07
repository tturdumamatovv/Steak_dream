from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.conf.update(
    worker_pool='solo'
)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Настройка периодического выполнения задач
app.conf.beat_schedule = {
    'check-birthdays-every-day': {
        'task': 'apps.authentication.tasks.check_birthdays_task',
        'schedule': crontab(hour=0, minute=0),  # Каждый день в полночь
    },
    'fetch-products-every-15-minutes': {
        'task': 'apps.authentication.tasks.fetch_products_from_api',
        'schedule': crontab(minute='*/15'),  # Каждые 15 минут
    },
}
