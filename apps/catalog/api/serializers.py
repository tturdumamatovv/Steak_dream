from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.authentication.models import UserPromotionalProduct
from apps.catalog.models import Product, Category, Tag, PromotionalProduct


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
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'discount_price', 'discount', 'discount_type', 'quantity',
                  'image', 'tags', 'measure', 'sort_priority', 'category_slug',
                  'category_name', 'min_total_amount', 'is_favorite']

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

    def get_is_favorite(self, obj):
        """Проверка, находится ли продукт в избранном у текущего пользователя."""
        user = self.context.get('request').user  # Получаем пользователя из контекста
        if user.is_authenticated:
            return obj in user.favorite_products.all()
        return False

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


class PromotionalProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)
    class Meta:
        model = PromotionalProduct
        fields = ['id', 'product', 'start_time', 'end_time', 'description', 'image', 'required_quantity']


class UserPromotionalProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(source='promotional_product.product', many=False)
    required_quantity = serializers.IntegerField(source='promotional_product.required_quantity', read_only=True)


    class Meta:
        model = UserPromotionalProduct
        fields = ['product', 'purchased_quantity', 'required_quantity']
