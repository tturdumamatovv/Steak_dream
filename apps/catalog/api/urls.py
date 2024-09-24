from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from apps.catalog.api.views import (
    ProductListByCategorySlugView,
    CategoryListView,
    ProductSearchView,
    CategoryOnlyListView,
    # PopularProducts,
    # CheckProductSizes
)

urlpatterns = [
          path('product/search/', ProductSearchView.as_view(), name='product-search'),
          path('category/<slug:slug>/', ProductListByCategorySlugView.as_view(), name='category'),
          path('categories/', CategoryListView.as_view(), name='category-list'),
          path('categories/only/', CategoryOnlyListView.as_view(), name='category-only-list'),
          # path('popular/products/', PopularProducts.as_view(), name='popular-products'),
          # path('check/products/', CheckProductSizes.as_view(), name='check-products'),

]
