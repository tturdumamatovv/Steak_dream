from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.orders.models import Order, OrderItem, Restaurant
from .serializers import OrderSerializer, OrderItemSerializer, RestaurantSerializer
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
        request.data['user'] = request.user.id  # Устанавливаем пользователя
        order_serializer = OrderSerializer(data=request.data)
        if order_serializer.is_valid():
            order = order_serializer.save()  # Теперь пользователь будет сохранен

            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderCancelView(APIView):
    def post(self, request, pk):
        order = Order.objects.get(id=pk)
        if order.user != request.user:
            return Response({'error': 'You are not authorized to cancel this order.'}, status=status.HTTP_403_FORBIDDEN)
        order.status = 'cancelled'
        order.save()
        return Response({'message': 'Order canceled successfully.'}, status=status.HTTP_200_OK)


class RestaurantListView(generics.ListAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Restaurant.objects.all()
