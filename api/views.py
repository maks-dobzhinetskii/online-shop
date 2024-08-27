from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from django.db.models import Sum, F

from api.filters import ProductFilter
from api.models import Category, Product, Subcategory
from api.serializers import CategorySerializer, ProductSerializer, SubcategorySerializer


class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(stock__gt=models.F('reserved'))
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    pagination_class = ProductPagination

    @action(detail=True, methods=['patch'])
    def change_price(self, request, pk=None):
        product = self.get_object()
        new_price = request.data.get('price')
        product.price = new_price
        product.save()
        return Response({'status': 'price set'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def start_discount(self, request, pk=None):
        product = self.get_object()
        discount = request.data.get('discount')
        product.discount_percentage = discount
        product.save()
        return Response({'status': 'discount set'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reserve(self, request, pk=None):
        product = self.get_object()
        quantity = int(request.data.get('quantity', 1))
        if product.stock - product.reserved >= quantity:
            product.reserved += quantity
            product.save()
            return Response({'status': 'reserved'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'not enough stock'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def cancel_reserve(self, request, pk=None):
        product = self.get_object()
        quantity = int(request.data.get('quantity', 1))
        if product.reserved >= quantity:
            product.reserved -= quantity
            product.save()
            return Response({'status': 'reservation canceled'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'not enough reserved'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def sell(self, request, pk=None):
        product = self.get_object()
        quantity = int(request.data.get('quantity', 1))
        if product.reserved >= quantity:
            product.reserved -= quantity
            product.stock -= quantity
            product.sold += quantity
            product.save()
            return Response({'status': 'sold'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'not enough reserved'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def sales_report(self, request):
        category = request.query_params.get('category')
        subcategory = request.query_params.get('subcategory')

        products = Product.objects.all()

        if category:
            products = products.filter(category=category)
        if subcategory:
            products = products.filter(subcategory=subcategory)

        sales_data = products.aggregate(
            total_sold=Sum('sold'),
            total_revenue=Sum(F('price') * F('sold'))
        )

        return Response(sales_data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['patch'])
    def update_category(self, request, pk=None):
        product = self.get_object()
        category_id = request.data.get('category')
        try:
            category = Category.objects.get(id=category_id)
            product.category = category
            product.save()
            return Response({'status': 'category updated'}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({'status': 'category not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['patch'])
    def update_subcategory(self, request, pk=None):
        product = self.get_object()
        subcategory_id = request.data.get('subcategory')
        try:
            subcategory = Subcategory.objects.get(id=subcategory_id)
            product.subcategory = subcategory
            product.save()
            return Response({'status': 'subcategory updated'}, status=status.HTTP_200_OK)
        except Subcategory.DoesNotExist:
            return Response({'status': 'subcategory not found'}, status=status.HTTP_404_NOT_FOUND)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer