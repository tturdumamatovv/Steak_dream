from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(verbose_name=_('Название'), max_length=255)
    url = models.CharField(verbose_name=_('Ссылка'), max_length=255)
    publication = models.CharField(verbose_name=_('Публикация'), max_length=255)
    username = models.CharField(verbose_name=_('Имя пользователя'), max_length=255)
    password = models.CharField(verbose_name=_('Пароль'), max_length=255)
    infosystem = models.CharField(verbose_name=_('Инфосистема'), max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

