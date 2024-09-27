from background_task import background
from background_task.models import Task
import logging

logger = logging.getLogger(__name__)

from apps.yaros_connector.data_inserter import APIInserter
from apps.yaros_connector.models import Supplier


@background(schedule=600)  # Задача будет запускаться каждые 10 минут
def fetch_products():
    # Проверяем, существует ли уже задача
    if Task.objects.filter(task_name='fetch_products').exists():
        logger.info("Fetch products task already exists, skipping.")
        return  # Если задача уже существует, выходим

    logger.info("Fetching products...")
    suppliers = Supplier.objects.all()
    for supplier in suppliers:
        inserter = APIInserter(supplier=supplier)
        inserter.create()  # Получение и создание продуктов

@background(schedule=300)  # Задача будет запускаться каждые 5 минут
def update_products():
    # Проверяем, существует ли уже задача
    if Task.objects.filter(task_name='update_products').exists():
        logger.info("Update products task already exists, skipping.")
        return  # Если задача уже существует, выходим

    logger.info("Updating products...")
    suppliers = Supplier.objects.all()
    for supplier in suppliers:
        inserter = APIInserter(supplier=supplier)
        inserter.update_all_products()  # Обновление продуктов