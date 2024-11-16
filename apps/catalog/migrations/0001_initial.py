# Generated by Django 5.1.1 on 2024-11-15 11:29

import apps.common.mixins
import colorfield.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('yaros_connector', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('text_color', colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=25, samples=None, verbose_name='Цвет текста')),
                ('background_color', colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=25, samples=None, verbose_name='Цвет фона')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier_id', models.CharField(blank=True, max_length=50, null=True, verbose_name='ID поставщика')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('activity', models.BooleanField(default=True, verbose_name='Активный')),
                ('slug', models.CharField(blank=True, max_length=200, null=True, verbose_name='Ссылка')),
                ('image', models.FileField(blank=True, null=True, upload_to='media/images/categories', verbose_name='Изображение')),
                ('sort_priority', models.IntegerField(default=0, verbose_name='Приоритет сортировки')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='catalog.category', verbose_name='Родительская категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
            bases=(models.Model, apps.common.mixins.ImageProcessingMixin),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_new', models.BooleanField(default=False, verbose_name='Новый')),
                ('is_popular', models.BooleanField(default=False, verbose_name='Популярный')),
                ('min_total_amount', models.IntegerField(blank=True, default=1, null=True, verbose_name='Минимальная сумма заказа')),
                ('supplier_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='ID поставщика')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('price', models.DecimalField(decimal_places=6, max_digits=12, verbose_name='Цена')),
                ('discount_price', models.DecimalField(blank=True, decimal_places=6, max_digits=12, null=True, verbose_name='Цена со скидкой')),
                ('discount', models.DecimalField(decimal_places=6, default=0, max_digits=12, verbose_name='Скидка')),
                ('discount_type', models.CharField(blank=True, choices=[('percent', 'Процент'), ('amount', 'Сумма')], max_length=255, null=True, verbose_name='Тип скидки')),
                ('quantity', models.IntegerField(default=0, verbose_name='Количество')),
                ('image_url', models.URLField(blank=True, max_length=255, null=True, verbose_name='Ссылка на изображение')),
                ('image', models.FileField(blank=True, null=True, upload_to='media/images/products', verbose_name='Изображение')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('measure', models.CharField(blank=True, max_length=255, null=True, verbose_name='Единица измерения')),
                ('sort_priority', models.IntegerField(default=0, verbose_name='Приоритет сортировки')),
                ('activity', models.BooleanField(default=True, verbose_name='Активный')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='catalog.category', verbose_name='Категория')),
                ('supplier_integration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='yaros_connector.supplier', verbose_name='Поставщик')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
            bases=(models.Model, apps.common.mixins.ImageProcessingMixin),
        ),
        migrations.CreateModel(
            name='PromotionalProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='Время начала акции')),
                ('end_time', models.DateTimeField(verbose_name='Время окончания акции')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание акции')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/images/promotions')),
                ('required_quantity', models.PositiveIntegerField(default=1, verbose_name='Количество для подарка')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promotions', to='catalog.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Акционный продукт',
                'verbose_name_plural': 'Акционные продукты',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='promotional_products',
            field=models.ManyToManyField(blank=True, related_name='products', to='catalog.promotionalproduct', verbose_name='Акционные продукты'),
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='products', to='catalog.tag', verbose_name='Теги'),
        ),
    ]
