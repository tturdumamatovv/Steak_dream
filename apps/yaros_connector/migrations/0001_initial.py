# Generated by Django 5.1.1 on 2024-11-15 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('url', models.CharField(max_length=255, verbose_name='Ссылка')),
                ('publication', models.CharField(max_length=255, verbose_name='Публикация')),
                ('username', models.CharField(max_length=255, verbose_name='Имя пользователя')),
                ('password', models.CharField(max_length=255, verbose_name='Пароль')),
                ('infosystem', models.CharField(max_length=255, verbose_name='Инфосистема')),
            ],
            options={
                'verbose_name': 'Поставщик',
                'verbose_name_plural': 'Поставщики',
            },
        ),
    ]
