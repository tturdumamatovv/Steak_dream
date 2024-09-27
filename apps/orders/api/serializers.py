from rest_framework import serializers
from apps.orders.models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'amount']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)  # Изменено на order_items

    class Meta:
        model = Order
        fields = ['type', 'infosystem', 'status', 'pay_method', 'change', 'total', 'addresses', 'comment', 'order_items']  # Добавлено order_items
