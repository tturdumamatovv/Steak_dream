from colorfield.fields import ColorField
from django.db import models
from slugify import slugify

from apps.common.mixins import ImageProcessingMixin
from django.utils.translation import gettext_lazy as _

from apps.yaros_connector.models import Supplier


# Create your models here.


class Category(models.Model, ImageProcessingMixin):
    supplier_id = models.CharField(verbose_name=_('ID поставщика'), max_length=50, null=True, blank=True)
    title = models.CharField(verbose_name=_('Название'), max_length=255)
    parent = models.ForeignKey('self', verbose_name=_('Родительская категория'), on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    activity = models.BooleanField(verbose_name=_('Активный'), default=True)
    slug = models.CharField(verbose_name=_('Ссылка'), max_length=200, blank=True, null=True)
    image = models.FileField(verbose_name=_('Изображение'), upload_to='media/images/categories', null=True, blank=True)
    sort_priority = models.IntegerField(verbose_name=_('Приоритет сортировки'), default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.process_and_save_image('image')

        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model, ImageProcessingMixin):
    is_new = models.BooleanField(verbose_name=_('Новый'), default=False)
    is_popular = models.BooleanField(verbose_name=_('Популярный'), default=False)
    min_total_amount = models.IntegerField(verbose_name=_('Минимальная сумма заказа'), null=True, blank=True, default=1)
    supplier_integration = models.ForeignKey(Supplier, verbose_name=_('Поставщик'), on_delete=models.CASCADE, null=True, blank=True)
    supplier_id = models.CharField(verbose_name=_('ID поставщика'), max_length=50, null=True, blank=True, unique=True)
    category = models.ForeignKey(Category, verbose_name=_('Категория'), on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    title = models.CharField(verbose_name=_('Название'), max_length=255)
    price = models.DecimalField(verbose_name=_('Цена'), max_digits=12, decimal_places=6)
    discount_price = models.DecimalField(verbose_name=_('Цена со скидкой'), max_digits=12, decimal_places=6, null=True, blank=True)
    discount = models.DecimalField(verbose_name=_('Скидка'), max_digits=12, decimal_places=6, default=0)
    discount_type = models.CharField(verbose_name=_('Тип скидки'), max_length=255, null=True, blank=True, choices=[('percent', 'Процент'), ('amount', 'Сумма')])
    quantity = models.IntegerField(verbose_name=_('Количество'), default=0)
    image_url = models.URLField(verbose_name=_('Ссылка на изображение'), max_length=255, null=True, blank=True)
    image = models.FileField(verbose_name=_('Изображение'), upload_to='media/images/products', null=True, blank=True)
    description = models.TextField(verbose_name=_('Описание'), null=True, blank=True)
    measure = models.CharField(verbose_name=_('Единица измерения'), max_length=255, null=True, blank=True)
    sort_priority = models.IntegerField(verbose_name=_('Приоритет сортировки'), default=0)
    activity = models.BooleanField(verbose_name=_('Активный'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', related_name='products', verbose_name=_('Теги'), blank=True)

    def apply_discount(self):
        if self.discount_type == 'percent':
            self.discount_price = self.price * (1 - self.discount / 100)
        elif self.discount_type == 'amount':
            self.discount_price = self.price - self.discount
        else:
            self.discount_price = self.price


    def save(self, *args, **kwargs):
        self.process_and_save_image('image')
        self.apply_discount()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Название'))
    text_color = ColorField(default='#FF0000', format='hex', verbose_name=_('Цвет текста'))
    background_color = ColorField(default='#FF0000', format='hex', verbose_name=_('Цвет фона'))

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name
