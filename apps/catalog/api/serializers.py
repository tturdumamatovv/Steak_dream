from django.core import serializers

from apps.catalog.models import Product, Category




class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'text_color', 'background_color']



class ProductSerializer(serializers.ModelSerializer):
    # ingredients = IngredientSerializer(many=True)
    tags = TagSerializer(many=True)
    category_slug = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'image', 'tags', 'measure', 'sort_priority', 'bonuses',
                  'product_sizes', 'category_slug', 'category_name']

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

    def get_category_slug(self, obj):
        if obj.category:
            return obj.category.slug
        return None

    def get_category_name(self, obj):
        # Проверяем, существует ли категория у продукта
        if obj.category:
            return obj.category.name
        return None


class CategoryProductSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    # sets = SetSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'parent', 'slug', 'image', 'products', ]  # 'sets']
