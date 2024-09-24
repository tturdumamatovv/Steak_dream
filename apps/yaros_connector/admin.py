from django.contrib import admin
from unfold.admin import ModelAdmin

from .data_inserter import APIInserter
from .models import Supplier


# Register your models here.


@admin.register(Supplier)
class SupplierAdmin(ModelAdmin):
    pass

    def run_api_insert(self, request, queryset):
        from .tasks import demo_task
        demo_task("Hello, Background Tasks!", repeat=5)
        for supplier in queryset:
            inserter = APIInserter(supplier=supplier)
            inserter.create()
            self.message_user(request, f"Data insertion complete for supplier: {supplier.name}")

    def update_products_from_api(self, request, queryset):
        for supplier in queryset:
            inserter = APIInserter(supplier=supplier)
            inserter.update_all_products()
            self.message_user(request, f"Products updated for supplier: {supplier.name}")

    # Link the action to the admin
    actions = [run_api_insert, update_products_from_api]
    run_api_insert.short_description = 'Run API Insert for selected Suppliers'

    update_products_from_api.short_description = "Update products from API for selected suppliers"

