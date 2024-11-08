from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib import messages

from .data_inserter import APIInserter
from .models import Supplier
from .tasks import fetch_products_from_api, update_products_task


# Register your models here.


@admin.register(Supplier)
class SupplierAdmin(ModelAdmin):
    def run_api_insert(self, request, queryset):
        for supplier in queryset:
            fetch_products_from_api.delay(supplier.id)
            self.message_user(request, f"Запрос на загрузку данных для {supplier.name} отправлен.", level=messages.SUCCESS)

    def update_products_from_api(self, request, queryset):
        for supplier in queryset:
            update_products_task.delay(supplier.id)
            self.message_user(request, f"Запрос на обновление продуктов для {supplier.name} отправлен.", level=messages.SUCCESS)

    actions = [run_api_insert, update_products_from_api]
    run_api_insert.short_description = 'Загрузить данные для выбранных поставщиков'
    update_products_from_api.short_description = "Обновить данные для выбранных поставщиков"
