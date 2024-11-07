from django.contrib import admin

from django.utils.translation import gettext_lazy as _
from unfold.admin import TabularInline, ModelAdmin, StackedInline

from .models import User, UserAddress, BonusTransaction, Child
from .tasks import test_task

@admin.register(UserAddress)
class UserAddressAdmin(ModelAdmin):
    pass


class UserAddressInline(StackedInline):
    model = UserAddress
    extra = 0
    classes = ['collapse']


class ChildInline(StackedInline):
    model = Child
    extra = 0
    classes = ['collapse']


@admin.register(User)
class UserAdmin(ModelAdmin):
    inlines = [UserAddressInline, ChildInline]
    actions = ['run_test_task']

    def run_test_task(self, request, queryset):
        for user in queryset:
            test_task.delay(user.id)
        self.message_user(request, "Тестовая задача запущена для выбранных пользователей")

    run_test_task.short_description = "Запустить тестовую задачу для выбранных пользователей"


@admin.register(BonusTransaction)
class BonusTransactionAdmin(ModelAdmin):
    list_display = ('user', 'bonus_spent', 'bonus_earned', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__phone_number',)
