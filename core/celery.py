from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Задайте настройки Django для использования в Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Создайте приложение Celery
app = Celery('core')
app.conf.update(
    worker_pool='solo'
)

# Загрузите настройки из конфигурации Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживайте задачи в установленных приложениях
app.autodiscover_tasks()

