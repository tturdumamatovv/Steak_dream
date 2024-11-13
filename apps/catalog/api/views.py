from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView

from apps.catalog.models import Category, Product
from .filters import ProductFilter
from .serializers import CategoryProductSerializer, ProductSerializer, CategoryOnlySerializer


class ProductListByCategorySlugView(ListAPIView):
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        try:
            category = Category.objects.get(slug=slug, activity=True)
        except Category.DoesNotExist:
            raise NotFound("Активная категория не найдена")
        products = Product.objects.filter(category=category, activity=True).distinct()
        product_serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response({'products': product_serializer.data})


class CategoryListView(ListAPIView):
    serializer_class = CategoryProductSerializer

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().prefetch_related(
            'products'
        ).all()
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
        categories = Category.objects.filter(activity=True)
        serializer = CategoryOnlySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)


class PopularProductsView(ListAPIView):
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(is_popular=True)
        product_serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response({'products': product_serializer.data})


class NewProductsView(ListAPIView):
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(is_new=True)
        product_serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response({'products': product_serializer.data})


class AddFavoriteView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        user = request.user

        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        if product in user.favorite_products.all():
            user.favorite_products.remove(product)
            message = 'Product removed from favorites'
        else:
            user.favorite_products.add(product)
            message = 'Product added to favorites'

        return Response({'message': message}, status=status.HTTP_200_OK)


class FavoriteProductsView(ListAPIView):
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        favorite_products = user.favorite_products.all()
        product_serializer = ProductSerializer(favorite_products, many=True, context={'request': request})
        return Response({'products': product_serializer.data})
