import os
import uuid
from io import BytesIO
from urllib.parse import urlparse, parse_qs

import qrcode
from django.core.files.base import ContentFile
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError('Необходимо указать номер телефона')

        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None):
        user = self.create_user(phone_number, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=14, unique=True, verbose_name=_('Номер телефона'))
    code = models.CharField(max_length=4, blank=True, null=True, verbose_name=_('Код'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Работник'))
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, max_length=255,
                                        verbose_name=_('Изображение профиля'))
    full_name = models.CharField(max_length=255, blank=True, verbose_name=_('Полное имя'))
    date_of_birth = models.DateField(blank=True, null=True, verbose_name=_('Дата рождения'))
    email = models.EmailField(blank=True, verbose_name=_('Имейл'))
    first_visit = models.BooleanField(default=True, verbose_name=_('Дата первого визита'))
    fcm_token = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Токен'))
    receive_notifications = models.BooleanField(default=False, verbose_name=_('Получать уведомления'), null=True,
                                                blank=True)
    last_order = models.DateTimeField(null=True, blank=True, verbose_name=_("Последний заказ"))
    bonus = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_('Бонусы'), null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True, verbose_name=_('QR Код'))
    secret_key = models.CharField(max_length=255, default='', verbose_name=_('Секретный ключ'))

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="user_set_custom",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="user_set_custom",
        related_query_name="user",
    )

    def get_admin_url(self):
        return f"/admin/authentication/user/{self.id}/change/"

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _("Пользователи")

    def generate_qr_code(self):
        url = f"qr/check/qr/user/{self.id}/?secret_key={self.secret_key}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        filename = f'qr_code_{self.id}.png'
        self.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)

    def generate_new_secret_key(self):
        return str(uuid.uuid4())  # Генерация нового секретного ключа

    def get_and_update_qr(self):
        current_qr_code = self.qr_code

        # Удаляем старый QR-код из файловой системы, если он существует
        if current_qr_code:
            if os.path.isfile(current_qr_code.path):
                os.remove(current_qr_code.path)

        # Генерируем новый секретный ключ
        self.secret_key = self.generate_new_secret_key()
        self.generate_qr_code()  # Генерируем новый QR-код
        self.save()  # Сохраняем изменения

        return current_qr_code.url if current_qr_code else None

    def check_secret_key(self, qr_url):
        # Извлечение параметров из QR-кода
        parsed_url = urlparse(qr_url)
        query_params = parse_qs(parsed_url.query)

        # Извлечение ID пользователя и секретного ключа
        user_id = parsed_url.path.split('/')[-1]  # Предполагается, что ID - последний сегмент пути
        provided_secret_key = query_params.get('secret_key', [None])[0]

        # Проверка наличия пользователя
        user = get_object_or_404(User, id=user_id)

        # Сравнение секретного ключа
        if user.secret_key == provided_secret_key:
            return True  # Ключи совпадают
        else:
            return False  # Ключи не совпадают

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.qr_code:
            self.generate_qr_code()
            super().save(*args, **kwargs)


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name=_("Пользователь"))
    city = models.CharField(max_length=100, verbose_name=_("Адрес"), null=True, blank=True)
    # street = models.CharField(max_length=100, verbose_name=_("Улица"), null=True, blank=True)
    # house_number = models.CharField(max_length=10, verbose_name=_("Номер дома"), null=True, blank=True)
    apartment_number = models.CharField(max_length=10, verbose_name=_("Номер квартиры"), null=True, blank=True)
    entrance = models.CharField(max_length=10, verbose_name=_("Подъезд"), null=True, blank=True)
    floor = models.CharField(max_length=10, verbose_name=_("Этаж"), null=True, blank=True)
    intercom = models.CharField(max_length=10, verbose_name=_("Домофон"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    is_primary = models.BooleanField(default=False, verbose_name=_("Главный"))
    latitude = models.DecimalField(max_digits=200, decimal_places=6, verbose_name=_('Широта'), null=True, blank=True)
    longitude = models.DecimalField(max_digits=200, decimal_places=6, verbose_name=_('Долгота'), null=True, blank=True)
    comment = models.TextField(verbose_name=_("Комментарий"), null=True, blank=True)

    class Meta:
        verbose_name = _("Адрес пользователя")
        verbose_name_plural = _("Адреса пользователей")
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.city}'  # - {self.street} {self.house_number}'
