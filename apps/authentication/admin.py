from django.contrib import admin

from django.utils.translation import gettext_lazy as _
from unfold.admin import TabularInline, ModelAdmin, StackedInline

from .models import User, UserAddress



@admin.register(UserAddress)
class UserAddressAdmin(ModelAdmin):
    pass


class UserAddressInline(StackedInline):
    model = UserAddress
    extra = 0
    classes = ['collapse']


@admin.register(User)
class UserAdmin(ModelAdmin):
    inlines = [UserAddressInline]
