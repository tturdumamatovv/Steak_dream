from django.contrib import admin
from unfold.admin import TabularInline, ModelAdmin

from .models import Order, OrderItem
from ..yaros_connector.models import Supplier
from ..yaros_connector.order_sender import APIOrderSender


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    inlines = [OrderItemInline]


    actions = ['send_order_to_yaros']

    def send_order_to_yaros(self, request, queryset):
        for instance in queryset:
            supplier = Supplier.objects.first()
            order_sender = APIOrderSender(order=instance, supplier=supplier)
            response = order_sender.prepare_order(instance)  # Отправляем заказ
            print("Ответ от Ярос:", response)  # Логируем ответ от Ярос