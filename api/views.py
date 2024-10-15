from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer


class ProductDetailAPIView(APIView):
    def post(self, request):
        product_code = request.data.get('product_code')
        quantity = request.data.get('quantity')
        print(request.data)

        try:
            product = Product.objects.get(code=product_code)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        product_data = ProductSerializer(product).data

        # Include the requested quantity in the response
        product_data['requested_quantity'] = quantity

        return Response({"result": [product_data]}, status=status.HTTP_200_OK)
