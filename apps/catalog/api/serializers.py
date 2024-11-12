from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.catalog.models import Product, Category, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'text_color', 'background_color']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['slug', 'title', 'image']


class ProductSerializer(serializers.ModelSerializer):
    # ingredients = IngredientSerializer(many=True)
    tags = TagSerializer(many=True)
    category_slug = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    price = serializers.FloatField()
    discount = serializers.FloatField()
    discount_price = serializers.FloatField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'discount_price', 'discount', 'discount_type',  'quantity', 'image', 'tags', 'measure', 'sort_priority', 'category_slug',
                  'category_name']


    def get_min_price(self, obj):
        return obj.get_min_price()

    def get_bonus_price(self, obj):
        # Логика для вычисления bonus_price
        # Предположим, что bonus_price - это минимальная бонусная цена среди всех размеров продукта
        min_bonus_price = None
        for size in obj.product_sizes.all():
            if min_bonus_price is None or size.bonus_price < min_bonus_price:
                min_bonus_price = size.bonus_price
        return min_bonus_price

    @extend_schema_field(serializers.CharField)
    def get_category_slug(self, obj):
        if obj.category:
            return obj.category.slug
        return None

    @extend_schema_field(serializers.CharField)
    def get_category_name(self, obj):
        # Проверяем, существует ли категория у продукта
        if obj.category:
            return obj.category.title
        return None

class CategoryProductSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'parent', 'slug', 'image', 'products', ]


class CategoryOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'image', ]
