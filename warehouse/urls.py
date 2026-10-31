from django.urls import path, include
from rest_framework.routers import DefaultRouter
from warehouse.views import (
    ProductMaterialCalculationAPIView,
    ProductViewSet,
    MaterialViewSet,
    WarehouseViewSet,
)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'materials', MaterialViewSet, basename='material')
router.register(r'warehouses', WarehouseViewSet, basename='warehouse')

urlpatterns = [
    # Asosiy hisoblash API'si
    path('calculate/', ProductMaterialCalculationAPIView.as_view(), name='calculate-materials'),
    # Qo'shimcha ma'lumotlar API'si
    path('', include(router.urls)),
]
