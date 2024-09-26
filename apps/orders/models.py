from django.db import models


# Create your models here.


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
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    addresses = models.ForeignKey('authentication.UserAddress', on_delete=models.CASCADE)
    comment = models.TextField()


class OrderItem(models.Model):
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE)
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
    quantity = models.FloatField()
    amount = models.FloatField()
