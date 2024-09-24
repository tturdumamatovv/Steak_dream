from colorfield.fields import ColorField
from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

from apps.common.mixins import ImageProcessingMixin
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Category(models.Model, ImageProcessingMixin):
    supplier_id = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    activity = models.BooleanField(default=True)
    slug = models.CharField(max_length=200, blank=True, null=True)
    image = models.FileField(upload_to='media/images/categories', null=True, blank=True)
    sort_priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.process_and_save_image('image')

        if not self.slug:
            self.slug = slugify(unidecode(self.title))

        super().save(*args, **kwargs)


class Product(models.Model, ImageProcessingMixin):
    supplier_id = models.CharField(max_length=50, null=True, blank=True, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=6)
    quantity = models.FloatField(default=0.0)
    image_url = models.URLField(max_length=255, null=True, blank=True)
    image = models.FileField(upload_to='media/images/products', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    measure = models.CharField(max_length=255, null=True, blank=True)
    sort_priority = models.IntegerField(default=0)
    activity = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', related_name='products', verbose_name=_('Теги'), blank=True)

    def save(self, *args, **kwargs):
        self.process_and_save_image('image')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Название'))
    text_color = ColorField(default='#FF0000', format='hex', verbose_name=_('Цвет текста'))
    background_color = ColorField(default='#FF0000', format='hex', verbose_name=_('Цвет фона'))

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name
