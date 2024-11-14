from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from apps.catalog.api.views import (
    ProductListByCategorySlugView,
    CategoryListView,
    ProductSearchView,
    CategoryOnlyListView,
    PopularProductsView,
    NewProductsView, AddFavoriteView, FavoriteProductsView,
    PromotionalProductListView, UpdateUserPromotionalProductView
)

urlpatterns = [
    path('product/search/', ProductSearchView.as_view(), name='product-search'),
    path('category/<slug:slug>/', ProductListByCategorySlugView.as_view(), name='category'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/only/', CategoryOnlyListView.as_view(), name='category-only-list'),
    path('popular-products/', PopularProductsView.as_view(), name='popular-products'),
    path('new-products/', NewProductsView.as_view(), name='new-products'),
    path('add-favorite/<int:product_id>/', AddFavoriteView.as_view(), name='add_favorite'),
    path('favorite/products/', FavoriteProductsView.as_view(), name='favorite_products'),
    path('promotional-products/', PromotionalProductListView.as_view(), name='promotional_products'),
    path('update-promotional-product/', UpdateUserPromotionalProductView.as_view(), name='update_user_promotional_product'),

]
