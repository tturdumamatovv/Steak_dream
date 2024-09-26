from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Category, Product


# Register your models here.
@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['title', 'category', 'price', 'quantity', 'created_at']
    search_fields = ['title', 'supplier_id',]
    list_filter = ['category', 'created_at']
