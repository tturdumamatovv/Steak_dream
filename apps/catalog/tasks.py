from celery import shared_task

from ..yaros_connector.models import Supplier
from ..yaros_connector.product_updater import ProductUpdater


@shared_task
def update_product_task(supplier_id, product_id):
    supplier = Supplier.objects.get(id=supplier_id)
    inserter = ProductUpdater(supplier=supplier)
    return inserter.update_product_data([product_id])


