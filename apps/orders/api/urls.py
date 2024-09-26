from django.urls import path
from .views import UserOrderListView, UserOrderDetailView

urlpatterns = [
    path('orders/', UserOrderListView.as_view(), name='user-order-list'),
    path('orders/<int:pk>/', UserOrderDetailView.as_view(), name='user-order-detail'),
]
