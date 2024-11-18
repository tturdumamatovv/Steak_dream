from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from django.utils import timezone

from apps.catalog.models import Category, Product, PromotionalProduct
from .filters import ProductFilter
from .serializers import CategoryProductSerializer, ProductSerializer, CategoryOnlySerializer, PromotionalProductSerializer, UserPromotionalProductSerializer
from ...authentication.models import UserPromotionalProduct
from django.db.models import Q
import random


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
    def post(self, request, product_id):
        # Get the user from the request
        if not request.user.is_authenticated:
            return Response({"error": "Пользователь не авторизован"}, status=status.HTTP_401_UNAUTHORIZED)
        user = request.user

        try:
            # Get the product using the product_id from the URL
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # Toggle the product in the user's favorite products
        if product in user.favorite_products.all():
            user.favorite_products.remove(product)
            message = 'Продукт был удален из избранных'
        else:
            user.favorite_products.add(product)
            message = 'Продукт был добавлен в избранное'

        # Return the response with a success message
        return Response({'message': message}, status=status.HTTP_200_OK)


class FavoriteProductsView(ListAPIView):
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "Пользователь не авторизован"}, status=status.HTTP_401_UNAUTHORIZED)

        user = request.user
        favorite_products = user.favorite_products.all()
        product_serializer = ProductSerializer(favorite_products, many=True, context={'request': request})
        return Response({'products': product_serializer.data})


class PromotionalProductListView(ListAPIView):
    queryset = PromotionalProduct.objects.all()
    serializer_class = PromotionalProductSerializer

    def get_queryset(self):
        return super().get_queryset().filter(start_time__lte=timezone.now(), end_time__gte=timezone.now())


class UpdateUserPromotionalProductView(APIView):

    serializer_class = UserPromotionalProductSerializer
    def post(self, request, *args, **kwargs):
        product_id = request.data.get('promotional_product')
        quantity = request.data.get('purchased_quantity', 1)

        try:
            promotional_product = PromotionalProduct.objects.get(product_id=product_id)
        except PromotionalProduct.DoesNotExist:
            return Response({'error': 'Акционный продукт не найден'}, status=status.HTTP_404_NOT_FOUND)

        user_promotion, created = UserPromotionalProduct.objects.get_or_create(
            user=request.user,
            promotional_product=promotional_product
        )

        user_promotion.purchased_quantity += quantity
        user_promotion.save()

        return Response({'message': 'Счетчик обновлен', 'purchased_quantity': user_promotion.purchased_quantity}, status=status.HTTP_200_OK)


class UserPromotionalProductView(ListAPIView):
    serializer_class = UserPromotionalProductSerializer

    def get_queryset(self):
        return UserPromotionalProduct.objects.filter(user=self.request.user)


class SimilarProductsView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        product_id = self.kwargs['id']
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Product.objects.none()

        similar_products = product.similar_products.all()

        if similar_products.count() < 10:
            additional_products = Product.objects.filter(category=product.category).exclude(id=product.id)
            similar_products = similar_products | additional_products

        if similar_products.count() < 10:
            random_products = Product.objects.exclude(id__in=similar_products.values_list('id', flat=True))
            similar_products = similar_products | random_products

        return similar_products.distinct()[:10]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)