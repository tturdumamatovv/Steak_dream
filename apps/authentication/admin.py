from django.contrib import admin

from django.utils.translation import gettext_lazy as _
from unfold.admin import TabularInline, ModelAdmin, StackedInline

from .models import User, UserAddress, BonusTransaction, Child

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


@admin.register(BonusTransaction)
class BonusTransactionAdmin(ModelAdmin):
    list_display = ('user', 'bonus_spent', 'bonus_earned', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__phone_number',)
