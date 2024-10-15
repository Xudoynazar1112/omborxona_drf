from django.urls import path
from .views import ProductDetailAPIView

urlpatterns = [
    path('', ProductDetailAPIView.as_view(), name='product')
]
