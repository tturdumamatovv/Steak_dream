from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.orders.models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from drf_spectacular.utils import extend_schema


class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(self.request.user)
        return Order.objects.filter(user=self.request.user)


class UserOrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreateView(APIView):
    @extend_schema(
        request=OrderSerializer,
        responses={
            201: OrderSerializer,
            400: 'Bad Request'
        },
        description="Создание нового заказа с предметами."
    )
    def post(self, request):
        # Устанавливаем пользователя в данные запроса
        request.data['user'] = request.user.id  # Устанавливаем пользователя
        order_serializer = OrderSerializer(data=request.data)
        if order_serializer.is_valid():
            order = order_serializer.save()  # Теперь пользователь будет сохранен

            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
