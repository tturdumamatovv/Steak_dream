from django.apps import AppConfig


class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.catalog'

    verbose_name = 'Каталог'
    verbose_name_plural = 'Каталоги'