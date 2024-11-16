from django.db import transaction
from rest_framework import serializers

from apps.catalog.api.serializers import ProductSerializer
from apps.orders.models import Order, OrderItem, Restaurant


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'amount']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['type', 'infosystem', 'status', 'pay_method', 'change', 'total', 'addresses', 'comment',
                  'order_items', 'user', 'created_at']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            for item_data in order_items_data:
                OrderItem.objects.create(order=order, **item_data)
        return order


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'phone_number', 'email', 'opening_hours', 'closing_hours']
