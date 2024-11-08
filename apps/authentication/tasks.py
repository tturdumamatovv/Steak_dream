from celery import shared_task
from .models import User


@shared_task
def check_birthdays_for_selected_users(user_ids):
    users = User.objects.filter(id__in=user_ids)
    for user in users:
        user.check_birthdays()
