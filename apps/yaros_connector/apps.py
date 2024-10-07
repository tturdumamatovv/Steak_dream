from django.apps import AppConfig
from django.db import ProgrammingError



class YarosConnectorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.yaros_connector'

    def ready(self):
        from background_task.models import Task
        from .tasks import fetch_products, update_products, test_task

        try:
            if not Task.objects.filter(task_name='apps.yaros_connector.tasks.fetch_products').exists():
                fetch_products(repeat=600)  # Запускаем каждые 10 минут

            if not Task.objects.filter(task_name='apps.yaros_connector.tasks.update_products').exists():
                update_products(repeat=300)  # Запускаем каждые 5 минут
        except ProgrammingError:
                pass