import random
import string

from django.contrib.auth import get_user_model
from django.db import models
from geopy.distance import geodesic
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
from apps.pages.models import SingletonModel

# Create your models here.
User = get_user_model()



class Restaurant(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Название'))
    address = models.CharField(max_length=255, verbose_name=_('Адрес'))
    phone_number = models.CharField(max_length=15, verbose_name=_('Телефонный номер'), blank=True, null=True)
    email = models.EmailField(verbose_name=_('Электронная почта'), blank=True, null=True)
    opening_hours = models.TimeField(verbose_name=_('Время открытия'), blank=True, null=True)
    closing_hours = models.TimeField(verbose_name=_('Время закрытия'), blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_('Широта'), blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_('Долгота'), blank=True, null=True)
    telegram_chat_ids = models.TextField(verbose_name=_('Telegram Chat IDs'), validators=[MinLengthValidator(1)],
                                         help_text=_('Введите чат-айди через запятую'), blank=True, null=True)
    self_pickup_available = models.BooleanField(default=True, verbose_name=_('Самовывоз доступен'))

    class Meta:
        verbose_name = _("Ресторан")
        verbose_name_plural = _("Рестораны")

    def __str__(self):
        return self.name

    def get_telegram_chat_ids(self):
        if self.telegram_chat_ids:
            return [chat_id.strip() for chat_id in self.telegram_chat_ids.split(',') if chat_id.strip()]
        return []

    def distance_to(self, user_lat, user_lon):
        restaurant_location = (self.latitude, self.longitude)
        user_location = (user_lat, user_lon)
        return geodesic(restaurant_location, user_location).kilometers


class Order(models.Model):
    type = models.CharField(max_length=255, choices=[('delivery', 'Доставка'), ('pickup', 'Самовывоз')])
    infosystem = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255,
                              choices=[('created', 'Создан'), ('paid', 'Оплачен'), ('delivered', 'Доставлен')])
    pay_method = models.CharField(max_length=255, choices=[
        ('cash', 'Наличные'),
        ('visa', 'Виза'),
        ('elcart', 'Эльекарт'),
        ('elsom', 'Элсом'),
        ('o_money', 'О деньги')
    ])
    change = models.FloatField()
    total = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    addresses = models.ForeignKey('authentication.UserAddress', on_delete=models.CASCADE)
    comment = models.TextField()


class OrderItem(models.Model):
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
    quantity = models.FloatField()
    amount = models.FloatField()




class PercentCashback(SingletonModel):
    mobile_percent = models.IntegerField(verbose_name="Процент за мобильное приложение")
    web_percent = models.IntegerField(verbose_name="Процент за веб-сайт")
    magazine_percent = models.IntegerField(verbose_name="Процент за магазин")

    def __str__(self):
        return f"Процент кэшбека № {self.id}"

    class Meta:
        verbose_name = "Процент кэшбэка"
        verbose_name_plural = "Проценты кэшбэка"


class Report(models.Model):
    image = models.ImageField(upload_to='reports/', blank=True, null=True, verbose_name="Картинка")
    description = models.TextField(verbose_name="Описание")
    contact_number = models.CharField(max_length=15, verbose_name="Контактный номер")

    def __str__(self):
        return f"Отчет № {self.id}"

    class Meta:
        verbose_name = "Отчет"
        verbose_name_plural = "Отчеты"
