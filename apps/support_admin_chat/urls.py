# urls.py
from django.urls import path
from .views import admin_chat, user_chat, admin_chat_list

urlpatterns = [
    path('admin/chat/<int:pk>/', admin_chat, name='admin-chat'),
    path('admin/chat/list', admin_chat_list, name='admin-chat-list'),

    path('chat/', user_chat, name='user-chat'),

]
