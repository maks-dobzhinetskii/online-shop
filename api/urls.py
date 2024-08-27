from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet, ProductViewSet, SubcategoryViewSet


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'subcategories', SubcategoryViewSet, basename='subcategory')


urlpatterns = [
    path('', include(router.urls)),
    # path('products/sales_report/', sales_report, name='sales_report'),
]

