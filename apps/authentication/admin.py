from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline

from .models import User, UserAddress, Child, BonusSystemSettings, BonusTransaction, PromoCode
from .tasks import check_birthdays_for_selected_users


@admin.register(UserAddress)
class UserAddressAdmin(ModelAdmin):
    pass


class UserAddressInline(StackedInline):
    model = UserAddress
    extra = 0
    classes = ['collapse']


class ChildInline(StackedInline):
    model = Child
    extra = 1




@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ['phone_number', 'date_of_birth']  # Добавьте нужные поля
    search_fields = ['phone_number', 'date_of_birth']
    readonly_fields = ['qr_code_data']
    exclude = ['favorite_products']
    inlines = [UserAddressInline, ChildInline]

    def check_birthdays(self, request, queryset):
        user_ids = list(queryset.values_list('id', flat=True))  # Получаем список ID выбранных пользователей
        self.message_user(request, f"Запрос на проверку дней рождения для выбранных пользователей отправлен.")

    actions = [check_birthdays]
    check_birthdays.short_description = "Проверить дни рождения для выбранных пользователей и их детей"


@admin.register(BonusSystemSettings)
class BonusSystemSettingsAdmin(ModelAdmin):
    pass


@admin.register(BonusTransaction)
class BonusTransactionAdmin(ModelAdmin):
    list_display = ['user', 'bonus_spent', 'bonus_earned', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__phone_number']


@admin.register(PromoCode)
class PromoCodeAdmin(ModelAdmin):
    list_display = ['code', 'is_personal', 'usage_limit', 'expiration_date', 'coins_amount']
    search_fields = ['code']
    list_filter = ['is_personal', 'expiration_date']
