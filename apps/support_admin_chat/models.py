from django.db import models
from django.conf import settings

from django.contrib.auth import get_user_model

User = get_user_model()

class ChatRoom(models.Model):
    user = models.OneToOneField(User, related_name='chat_room', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Чат-комната для {self.user.phone_number} (Активна: {self.active})"
    
    class Meta:
        verbose_name = 'Чат-комната'
        verbose_name_plural = 'Чат-комнаты'


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Сообщение от {self.sender.phone_number} в комнате {self.room.id}"
    
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'