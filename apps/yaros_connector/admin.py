from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib import messages

from .data_inserter import APIInserter
from .models import Supplier
from apps.authentication.tasks import fetch_products_from_api


# Register your models here.


@admin.register(Supplier)
class SupplierAdmin(ModelAdmin):
    def run_api_insert(self, request, queryset):
        for supplier in queryset:
            inserter = APIInserter(supplier=supplier)
            error = inserter.create()
            if error:
                self.message_user(
                    request, 
                    f"Ошибка при загрузке данных для {supplier.name}: {error}\n"
                    f"Пожалуйста, проверьте поля 'Ссылка' и 'Публикация' на наличие недостающих слешей ('/').",
                    level=messages.ERROR
                )
            else:
                self.message_user(request, f"Данные для {supplier.name} успешно загружены", level=messages.SUCCESS)

    def update_products_from_api(self, request, queryset):
        for supplier in queryset:
            fetch_products_from_api.delay(supplier.id)
            self.message_user(request, f"Запрос на обновление продуктов для {supplier.name} отправлен.", level=messages.SUCCESS)

    actions = [run_api_insert, update_products_from_api]
    run_api_insert.short_description = 'Загрузить данные для выбранных поставщиков'
    update_products_from_api.short_description = "Обновить данные для выбранных поставщиков"
