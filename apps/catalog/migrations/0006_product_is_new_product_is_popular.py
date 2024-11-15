# Generated by Django 5.0.7 on 2024-11-13 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_product_min_total_amount'),
    ]

    operations = [
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
    ]
