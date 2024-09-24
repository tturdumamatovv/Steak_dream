from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from apps.catalog.models import Category, Product
from .filters import ProductFilter
from .serializers import CategoryProductSerializer, ProductSerializer, CategoryOnlySerializer


class ProductListByCategorySlugView(ListAPIView):
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            raise NotFound("Категория не найдена")
        products = Product.objects.filter(category=category).distinct()
        product_serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response({'products': product_serializer.data, })


class CategoryListView(ListAPIView):
    serializer_class = CategoryProductSerializer

    def get(self, request, *args, **kwargs):
        categories = Category.objects.prefetch_related('products').all()
        serializer = CategoryProductSerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)


class ProductSearchView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter


class CategoryOnlyListView(ListAPIView):
    serializer_class = CategoryOnlySerializer

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategoryOnlySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)


# class PopularProducts(ListAPIView):
#     pass
#
#
# class CheckProductSizes(ListAPIView):
#     pass
