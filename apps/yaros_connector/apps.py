from django.apps import AppConfig

class YarosConnectorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.yaros_connector'

    def ready(self):
        from background_task.models import Task  # Переместите импорт сюда
        from .tasks import fetch_products, update_products  # Переместите импорт сюда
        
        # Проверяем, существует ли уже задача
        if not Task.objects.filter(task_name='apps.yaros_connector.tasks.fetch_products').exists():
            fetch_products(repeat=600)  # Запускаем каждые 10 минут

        if not Task.objects.filter(task_name='apps.yaros_connector.tasks.update_products').exists():
            update_products(repeat=300)  # Запускаем каждые 5 минут
