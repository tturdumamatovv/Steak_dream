from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Category, Product
from .tasks import update_product_task


# Register your models here.
@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    # fields = ['title', 'parent', 'activity', 'image', 'sort_priority', 'supplier_id', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title']
    list_display = ['title', 'parent', 'supplier_id', 'activity']
    list_display_links = ['title', 'parent']
    list_filter = ['activity']

    list_editable = ['activity']
    list_per_page = 10


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['title', 'category', 'price', 'quantity', 'created_at', 'is_new', 'is_popular']
    search_fields = ['title', 'supplier_id',]
    list_filter = ['category', 'created_at']
    list_per_page = 15
    list_editable = ['is_new', 'is_popular']

    def update_selected_products(self, request, queryset):
        for product in queryset:
            update_product_task.delay(product.supplier_integration.id, product.supplier_id)  # Асинхронный вызов
            self.message_user(request, f"Запрос на обновление товара {product.title} отправлен.")

    # Link the action to the admin
    actions = [update_selected_products]
    update_selected_products.short_description = "Обновить данные для выбранных товаров"
