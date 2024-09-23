from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from apps.catalog.models import Category
from .serializers import CategoryProductSerializer


class ProductListByCategorySlugView(ListAPIView):
    pass


class CategoryListView(ListAPIView):
    serializer_class = CategoryProductSerializer

    def get(self, request, *args, **kwargs):
        categories = Category.objects.prefetch_related('products').all()
        serializer = CategoryProductSerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)


class ProductSearchView(ListAPIView):
    pass


class ProductBonusView(ListAPIView):
    pass


class CategoryOnlyListView(ListAPIView):
    pass


class PopularProducts(ListAPIView):
    pass


class CheckProductSizes(ListAPIView):
    pass
