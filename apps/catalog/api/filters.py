import django_filters

from apps.catalog.models import Product


class ProductFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(field_name='id')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['id', 'title']
