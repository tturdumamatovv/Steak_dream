# Generated by Django 5.1.1 on 2024-11-16 06:25

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        ('catalog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_map_api_key', models.CharField(blank=True, max_length=250, null=True, verbose_name='Ключ для карты')),
            ],
            options={
                'verbose_name': 'Google Карта',
                'verbose_name_plural': 'Google Карты',
            },
        ),
        migrations.CreateModel(
            name='PercentCashback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_percent', models.IntegerField(verbose_name='Процент за мобильное приложение')),
                ('web_percent', models.IntegerField(verbose_name='Процент за веб-сайт')),
                ('magazine_percent', models.IntegerField(verbose_name='Процент за магазин')),
            ],
            options={
                'verbose_name': 'Процент кэшбэка',
                'verbose_name_plural': 'Проценты кэшбэка',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='reports/', verbose_name='Картинка')),
                ('description', models.TextField(verbose_name='Описание')),
                ('contact_number', models.CharField(max_length=15, verbose_name='Контактный номер')),
            ],
            options={
                'verbose_name': 'Отчет',
                'verbose_name_plural': 'Отчеты',
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, verbose_name='Телефонный номер')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Электронная почта')),
                ('opening_hours', models.TimeField(blank=True, null=True, verbose_name='Время открытия')),
                ('closing_hours', models.TimeField(blank=True, null=True, verbose_name='Время закрытия')),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Широта')),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Долгота')),
                ('telegram_chat_ids', models.TextField(blank=True, help_text='Введите чат-айди через запятую', null=True, validators=[django.core.validators.MinLengthValidator(1)], verbose_name='Telegram Chat IDs')),
                ('self_pickup_available', models.BooleanField(default=True, verbose_name='Самовывоз доступен')),
            ],
            options={
                'verbose_name': 'Ресторан',
                'verbose_name_plural': 'Рестораны',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('delivery', 'Доставка'), ('pickup', 'Самовывоз')], default='pickup', max_length=255, verbose_name='Способ получения')),
                ('infosystem', models.CharField(blank=True, max_length=255, null=True, verbose_name='Инфосистема')),
                ('status', models.CharField(choices=[('pending', 'В ожидании'), ('in_progress', 'В процессе'), ('delivery', 'Доставка'), ('completed', 'Завершено'), ('cancelled', 'Отменено')], default='pending', max_length=255, verbose_name='Статус')),
                ('pay_method', models.CharField(choices=[('cash', 'Наличные'), ('visa', 'Виза'), ('elcart', 'Эльекарт'), ('elsom', 'Элсом'), ('o_money', 'О деньги')], default='cash', max_length=255, verbose_name='Способ оплаты')),
                ('change', models.FloatField(default=0, verbose_name='Сдача')),
                ('bonus_spent', models.FloatField(default=0, verbose_name='Использованные бонусы')),
                ('bonus_earned', models.FloatField(default=0, verbose_name='Заработанные бонусы')),
                ('total', models.FloatField(default=0, verbose_name='Итого')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('addresses', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.useraddress', verbose_name='Адрес доставки')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(verbose_name='Количество')),
                ('amount', models.FloatField(verbose_name='Сумма')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='orders.order', verbose_name='Заказы')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Товар в заказ',
                'verbose_name_plural': 'Товары в заказе',
            },
        ),
    ]
