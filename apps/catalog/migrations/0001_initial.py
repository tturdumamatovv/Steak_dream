# Generated by Django 5.1.1 on 2024-10-16 09:30

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
                ('supplier_id', models.CharField(blank=True, max_length=50, null=True)),
                ('title', models.CharField(max_length=255)),
                ('activity', models.BooleanField(default=True)),
                ('slug', models.CharField(blank=True, max_length=200, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='media/images/categories')),
                ('sort_priority', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='catalog.category')),
            ],
            bases=(models.Model, apps.common.mixins.ImageProcessingMixin),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier_id', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=6, max_digits=12)),
                ('quantity', models.FloatField(default=0.0)),
                ('image_url', models.URLField(blank=True, max_length=255, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='media/images/products')),
                ('description', models.TextField(blank=True, null=True)),
                ('measure', models.CharField(blank=True, max_length=255, null=True)),
                ('sort_priority', models.IntegerField(default=0)),
                ('activity', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='catalog.category')),
                ('supplier_integration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='yaros_connector.supplier')),
                ('tags', models.ManyToManyField(blank=True, related_name='products', to='catalog.tag', verbose_name='Теги')),
            ],
            bases=(models.Model, apps.common.mixins.ImageProcessingMixin),
        ),
    ]
