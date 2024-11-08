from celery import shared_task

from apps.yaros_connector.data_inserter import APIInserter
from apps.yaros_connector.models import Supplier


@shared_task
def fetch_products_from_api(supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)
    inserter = APIInserter(supplier=supplier)
    error = inserter.create()
    return error

@shared_task
def update_products_task(supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)
    inserter = APIInserter(supplier=supplier)
    error = inserter.update_all_products()
    return error
