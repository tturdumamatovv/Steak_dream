# Generated by Django 5.0.7 on 2024-11-12 08:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_bonussystemsettings_child'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Промокод')),
                ('is_personal', models.BooleanField(default=False, verbose_name='Именной')),
                ('usage_limit', models.PositiveIntegerField(default=1, verbose_name='Количество использований')),
                ('expiration_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания действия')),
                ('coins_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Количество койнов')),
                ('image', models.ImageField(blank=True, null=True, upload_to='promo_images/', verbose_name='Изображение для попапа')),
                ('users', models.ManyToManyField(blank=True, related_name='promo_codes', to=settings.AUTH_USER_MODEL, verbose_name='Пользователи')),
            ],
        ),
    ]
