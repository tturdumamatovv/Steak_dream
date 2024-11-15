# Generated by Django 5.0.7 on 2024-11-15 10:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_product_activity_alter_product_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=12, verbose_name='Скидка'),
        ),
        migrations.AddField(
            model_name='product',
            name='discount_price',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=12, null=True, verbose_name='Цена со скидкой'),
        ),
        migrations.AddField(
            model_name='product',
            name='discount_type',
            field=models.CharField(blank=True, choices=[('percent', 'Процент'), ('amount', 'Сумма')], max_length=255, null=True, verbose_name='Тип скидки'),
        ),
        migrations.AddField(
            model_name='product',
            name='is_new',
            field=models.BooleanField(default=False, verbose_name='Новый'),
        ),
        migrations.AddField(
            model_name='product',
            name='is_popular',
            field=models.BooleanField(default=False, verbose_name='Популярный'),
        ),
        migrations.AddField(
            model_name='product',
            name='min_total_amount',
            field=models.IntegerField(blank=True, default=1, null=True, verbose_name='Минимальная сумма заказа'),
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
    ]
