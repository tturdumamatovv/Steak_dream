from django.db import transaction
from rest_framework import serializers
from apps.orders.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'amount']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['type', 'infosystem', 'status', 'pay_method', 'change', 'total', 'addresses', 'comment', 'order_items', 'user']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            for item_data in order_items_data:
                OrderItem.objects.create(order=order, **item_data)
        return order
