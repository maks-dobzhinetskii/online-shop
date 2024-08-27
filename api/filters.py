from django_filters import rest_framework as filters

from api.models import Product


class ProductFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category', lookup_expr='exact')
    subcategory = filters.CharFilter(field_name='subcategory', lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['category', 'subcategory']