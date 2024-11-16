from django.urls import path
from .views import UserOrderListView, UserOrderDetailView, OrderCreateView, RestaurantListView

urlpatterns = [
    path('orders/', UserOrderListView.as_view(), name='user-order-list'),
    path('orders/<int:pk>/', UserOrderDetailView.as_view(), name='user-order-detail'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path('order/cancel/<int:pk>/', OrderCancelView.as_view(), name='order-cancel'),
    path('restaurants/', RestaurantListView.as_view(), name='restaurant-list'),
]
