from celery import shared_task
from .models import User
from ..yaros_connector.data_inserter import APIInserter


@shared_task
def check_birthdays_task():
    User.check_birthdays_for_all_users()

@shared_task
def fetch_products_from_api(supplier_id):
    inserter = APIInserter(supplier_id=supplier_id)
    error = inserter.create()
    return error
