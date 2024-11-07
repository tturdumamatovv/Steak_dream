from celery import shared_task


@shared_task
def test_task(user_id):
    # Логика задачи, например, вывод в консоль
    print(f"Задача для пользователя с ID {user_id} выполнена")