import os
import uuid
from io import BytesIO

import qrcode
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.core.files.base import ContentFile
from django.db import models
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.catalog.models import Product


class CustomUserManager(BaseUserManager):
    @transaction.atomic
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError('Необходимо указать номер телефона')

        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)

        bonus_settings, created = BonusSystemSettings.objects.get_or_create(pk=1)

        user.add_bonus(bonus_settings.registration_bonus)

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
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    qr_code_data = models.CharField(max_length=255, blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)
    secret_key = models.UUIDField(default=uuid.uuid4, editable=False)
    favorite_products = models.ManyToManyField(Product, blank=True, verbose_name=_('Избранные товары'))

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _("Пользователи")

    def save(self, *args, **kwargs):
        self.generate_qr_code()
        super().save(*args, **kwargs)

    def generate_qr_code(self):
        if self.pk and self.qr_code:
            try:
                old_instance = User.objects.get(pk=self.pk)
                if old_instance.qr_code and os.path.isfile(old_instance.qr_code.path):
                    os.remove(old_instance.qr_code.path)
            except User.DoesNotExist:
                pass

        qr_data = f"{self.phone_number}%{self.secret_key}"
        qr_code_data = f"{self.phone_number}%{self.secret_key}"
        qr_img = qrcode.make(qr_data)
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        file_name = f"qr_code_{self.phone_number}.png"
        self.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)
        self.qr_code_data = qr_code_data

    def regenerate_secret_key(self):
        self.secret_key = uuid.uuid4()
        self.generate_qr_code()
        self.save()

    def get_admin_url(self):
        return f"/admin/authentication/user/{self.id}/change/"

    def __str__(self):
        return self.phone_number

    def add_bonus(self, amount):
        """Метод для начисления бонусов пользователю."""
        if amount > 0:
            translation = BonusTransaction.objects.create(user=self, bonus_spent=0, bonus_earned=amount)
            translation.save()
            print(translation)
            self.bonus += amount
            self.save(update_fields=['bonus'])

    def check_birthdays(self):
        """Проверяет дни рождения пользователя и его детей и начисляет бонусы."""
        if self.date_of_birth and self.date_of_birth.month == timezone.now().month and self.date_of_birth.day == timezone.now().day:
            bonus_settings = BonusSystemSettings.load()
            self.add_bonus(bonus_settings.birthday_bonus)

        for child in self.children.all():
            if child.date_of_birth and child.date_of_birth.month == timezone.now().month and child.date_of_birth.day == timezone.now().day:
                child.check_birthday_bonus()

    @classmethod
    def check_birthdays_for_all_users(cls):
        users = cls.objects.all()
        for user in users:
            user.check_birthdays()


class Child(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children', verbose_name=_("Пользователь"))
    name = models.CharField(max_length=255, verbose_name=_("Имя"))
    date_of_birth = models.DateField(verbose_name=_("Дата рождения"))

    class Meta:
        verbose_name = _("Ребенок")
        verbose_name_plural = _("Дети")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def check_birthday_bonus(self):
        if self.date_of_birth and self.date_of_birth.month == timezone.now().month and self.date_of_birth.day == timezone.now().day:
            bonus_settings = BonusSystemSettings.load()
            self.user.add_bonus(bonus_settings.child_birthday_bonus)


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name=_("Пользователь"))
    city = models.CharField(max_length=100, verbose_name=_("Адрес"), null=True, blank=True)
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
        result = self.city if self.city else ''
        return f'{result}'


class BonusSystemSettings(models.Model):
    registration_bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                             verbose_name=_('Бонус за регистрацию'))
    birthday_bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                         verbose_name=_('Бонус за день рождения'))
    child_birthday_bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                               verbose_name=_('Бонус за день рождения детей'))
    order_bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Бонус за заказ'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.registration_bonus}'

    class Meta:
        verbose_name = _("Настройки системы бонусов")

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class BonusTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False)
    bonus_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonus_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.transaction_id}'

    class Meta:
        verbose_name = _("Бонусная транзакция")
        verbose_name_plural = _("Бонусные транзакции")
        ordering = ['-created_at']


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name=_("Промокод"))
    is_personal = models.BooleanField(default=False, verbose_name=_("Именной"))
    usage_limit = models.PositiveIntegerField(default=1, verbose_name=_("Количество использований"))
    expiration_date = models.DateTimeField(null=True, blank=True, verbose_name=_("Дата окончания действия"))
    coins_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Количество койнов"))
    image = models.ImageField(upload_to='promo_images/', blank=True, null=True,
                              verbose_name=_("Изображение для попапа"))
    users = models.ManyToManyField(User, blank=True, related_name='promo_codes', verbose_name=_("Пользователи"))

    def is_valid(self):
        """Проверяет, действителен ли промокод."""
        if self.expiration_date and self.expiration_date < timezone.now():
            return False
        return True

    def apply_to_user(self, user):
        """Применяет промокод к пользователю."""
        if self.is_valid() and self.usage_limit > 0:
            if user not in self.users.all():
                user.add_bonus(self.coins_amount)
                self.usage_limit -= 1
                self.save()
                self.users.add(user)
                return True
        return False

    def __str__(self):
        return self.code
