# Generated by Django 5.1.1 on 2024-11-15 11:29

import colorfield.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('content', models.TextField(verbose_name='Содержание')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
                ('image', models.ImageField(blank=True, null=True, upload_to='advertisements/', verbose_name='Изображение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Реклама',
                'verbose_name_plural': 'Рекламные объявления',
            },
        ),
        migrations.CreateModel(
            name='BonusPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_app_image', models.FileField(blank=True, null=True, upload_to='bonus_pages', verbose_name='Мобильное приложение')),
                ('mobile_app_text', models.TextField(blank=True, null=True, verbose_name='Текст приложения')),
                ('mobile_app_color', colorfield.fields.ColorField(blank=True, default='#000000', image_field=None, max_length=25, null=True, samples=None, verbose_name='Цвет карточки приложения')),
                ('bonus_image', models.FileField(blank=True, null=True, upload_to='bonus_pages', verbose_name='Картинка карточки бонусов')),
                ('bonus_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Заголовок карточки бонусов')),
                ('bonus_text', models.TextField(blank=True, null=True, verbose_name='Текст карточки бонусов')),
                ('bonus_color', colorfield.fields.ColorField(blank=True, default='#000000', image_field=None, max_length=25, null=True, samples=None, verbose_name='Цвет карточки бонусов')),
                ('bottom_card_text', models.TextField(blank=True, null=True, verbose_name='Нижняя часть карточки')),
                ('bottom_cart_color', colorfield.fields.ColorField(blank=True, default='#000000', image_field=None, max_length=25, null=True, samples=None, verbose_name='Цвет нижней части карточки')),
            ],
            options={
                'verbose_name': 'Бонусная страница',
                'verbose_name_plural': 'Бонусная страница',
            },
        ),
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Контакты',
                'verbose_name_plural': 'Контакты',
            },
        ),
        migrations.CreateModel(
            name='MainPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.ImageField(help_text='Иконка для главной страницы.', upload_to='images/icons', verbose_name='Иконка')),
                ('phone', models.CharField(help_text='Контактный телефон для главной страницы.', max_length=20, verbose_name='Телефон')),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Мета заголовок')),
                ('meta_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Мета описание')),
                ('meta_image', models.ImageField(blank=True, null=True, upload_to='images/meta', verbose_name='Мета изображение')),
            ],
            options={
                'verbose_name': 'Главная страница',
                'verbose_name_plural': 'Главная страница',
            },
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=255, verbose_name='Название сайта')),
                ('site_description', models.TextField(verbose_name='Описание сайта')),
                ('site_logo', models.FileField(blank=True, null=True, upload_to='site_logos', verbose_name='Логотип сайта')),
                ('site_bottom_logo', models.FileField(blank=True, null=True, upload_to='site_logos', verbose_name='Логотип нижней части сайта')),
                ('site_favicon', models.FileField(blank=True, null=True, upload_to='site_favicons', verbose_name='Иконка сайта')),
            ],
            options={
                'verbose_name': 'Настройки сайта',
                'verbose_name_plural': 'Настройки сайта',
            },
        ),
        migrations.CreateModel(
            name='StaticPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('slug', models.SlugField(blank=True, null=True, unique=True, verbose_name='Слаг')),
                ('image', models.FileField(blank=True, null=True, upload_to='images/static', verbose_name='Изображение')),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Мета заголовок')),
                ('meta_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Мета описание')),
                ('meta_image', models.FileField(blank=True, null=True, upload_to='images/meta', verbose_name='Мета изображение')),
            ],
            options={
                'verbose_name': 'Статическая страница',
                'verbose_name_plural': 'Статические страницы',
            },
        ),
        migrations.CreateModel(
            name='Stories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=123, null=True, verbose_name='Заголовок')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/stories', verbose_name='Изображение')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Группа историй',
                'verbose_name_plural': 'Группы историй',
            },
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('category', 'Категория'), ('product', 'Продукт'), ('link', 'Отдельная ссылка')], default='product', max_length=10, verbose_name='Тип баннера')),
                ('link', models.URLField(blank=True, null=True, verbose_name='Ссылка')),
                ('title', models.CharField(blank=True, max_length=123, null=True, verbose_name='Заголовок')),
                ('image_desktop', models.ImageField(upload_to='images/banners/desktop/%Y/%m/', verbose_name='Картинка крупная')),
                ('image_mobile', models.ImageField(upload_to='images/banners/mobile/%Y/%m/', verbose_name='Картинка мобильная')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name='Категория')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Баннер',
                'verbose_name_plural': 'Баннеры',
                'ordering': ['is_active', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('contacts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.contacts')),
            ],
            options={
                'verbose_name': 'Адрес',
                'verbose_name_plural': 'Адреса',
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255, verbose_name='Имейл')),
                ('contacts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.contacts')),
            ],
            options={
                'verbose_name': 'Имейл',
                'verbose_name_plural': 'Имейлы',
            },
        ),
        migrations.CreateModel(
            name='DeliveryConditions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Изображение')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_conditions', to='pages.mainpage')),
            ],
            options={
                'verbose_name': 'Условия доставки',
                'verbose_name_plural': 'Условия доставки',
            },
        ),
        migrations.CreateModel(
            name='MethodsOfPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Изображение')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='methods_of_payment', to='pages.mainpage')),
            ],
            options={
                'verbose_name': 'Способ оплаты',
                'verbose_name_plural': 'Способы оплаты',
            },
        ),
        migrations.CreateModel(
            name='OrderTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Изображение')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_types', to='pages.mainpage')),
            ],
            options={
                'verbose_name': 'Тип заказа',
                'verbose_name_plural': 'Типы заказа',
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=100, verbose_name='Ссылка')),
                ('icon', models.FileField(upload_to='payment_icons', verbose_name='Иконка')),
                ('contacts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.contacts')),
            ],
            options={
                'verbose_name': 'Ссылка для оплаты',
                'verbose_name_plural': 'Ссылки для оплаты',
            },
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=100, verbose_name='Телефон')),
                ('contacts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.contacts')),
            ],
            options={
                'verbose_name': 'Телефон',
                'verbose_name_plural': 'Телефоны',
            },
        ),
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=100, verbose_name='Ссылка')),
                ('icon', models.FileField(upload_to='social_icons', verbose_name='Иконка')),
                ('contacts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.contacts')),
            ],
            options={
                'verbose_name': 'Ссылка соцсети',
                'verbose_name_plural': 'Ссылки соцсетей',
            },
        ),
        migrations.CreateModel(
            name='StoriesUserCheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('stories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stories_user_check', to='pages.stories')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stories_user_check', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/stories', verbose_name='Изображение')),
                ('type', models.CharField(choices=[('category', 'Категория'), ('product', 'Продукт'), ('link', 'Отдельная ссылка')], default='product', max_length=10, verbose_name='Тип баннера')),
                ('link', models.URLField(blank=True, null=True, verbose_name='ссылка')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name='Категория')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='Продукт')),
                ('stories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stories', to='pages.stories')),
            ],
            options={
                'verbose_name': 'История',
                'verbose_name_plural': 'Истории',
            },
        ),
    ]
