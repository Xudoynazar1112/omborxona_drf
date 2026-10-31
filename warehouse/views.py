from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from drf_spectacular.utils import extend_schema, OpenApiExample

from warehouse.models import Product, Material, Warehouse
from warehouse.serializers import (
    OrderItemRequestSerializer,
    CalculationResponseSerializer,
    ProductSerializer,
    MaterialSerializer,
    WarehouseSerializer,
)
from warehouse.services import calculate_product_materials


class ProductMaterialCalculationAPIView(APIView):
    """
    Ishlab chiqarish korxonasida mahsulot ishlab chiqarish uchun kerak bo'lgan
    xomashyolarni hisoblash va ombor ma'lumotidan javob olish uchun REST API.
    """

    @extend_schema(
        summary="Mahsulotlar uchun xomashyolarni ombor partiyalari bo'yicha hisoblash",
        description=(
            "Mahsulotlar kodi va ularning miqdorlari ro'yxatini qabul qiladi. "
            "Ombordagi partiyalardan FIFO asosida xomashyolarni taqsimlaydi. "
            "Agar xomashyo yetmay qolsa, qolgan qismi warehouse_id: null va price: null bilan qaytariladi. "
            "DIQQAT: Bazadagi ombor ma'lumotlariga (remainder) o'zgartirish kiritilmaydi."
        ),
        request=OrderItemRequestSerializer(many=True),
        responses={
            status.HTTP_200_OK: CalculationResponseSerializer,
            status.HTTP_400_BAD_REQUEST: dict,
        },
        examples=[
            OpenApiExample(
                name="Ko'ylak va Shim uchun so'rov",
                description="30 ta Ko'ylak va 20 ta Shim uchun xomashyolarni hisoblash so'rovi",
                value=[
                    {"product_code": 238923, "quantity": 30},
                    {"product_code": 498723, "quantity": 20}
                ],
                request_only=True,
            ),
            OpenApiExample(
                name="Bitta mahsulot uchun so'rov",
                description="10 dona mahsulot uchun so'rov",
                value={"product_code": 238923, "quantity": 10},
                request_only=True,
            ),
            OpenApiExample(
                name="Kutilgan natija javobi",
                description="Ombordagi partiyalar bo'yicha taqsimlangan xomashyolar javobi",
                value={
                    "result": [
                        {
                            "product_name": "Koylak",
                            "product_qty": 30,
                            "product_materials": [
                                {"warehouse_id": 1, "material_name": "Mato", "qty": 12, "price": 1500},
                                {"warehouse_id": 2, "material_name": "Mato", "qty": 12, "price": 1600},
                                {"warehouse_id": 5, "material_name": "Tugma", "qty": 150, "price": 300},
                                {"warehouse_id": 3, "material_name": "Ip", "qty": 40, "price": 500},
                                {"warehouse_id": 4, "material_name": "Ip", "qty": 260, "price": 550}
                            ]
                        },
                        {
                            "product_name": "Shim",
                            "product_qty": 20,
                            "product_materials": [
                                {"warehouse_id": 2, "material_name": "Mato", "qty": 28, "price": 1600},
                                {"warehouse_id": 4, "material_name": "Ip", "qty": 40, "price": 550},
                                {"warehouse_id": None, "material_name": "Ip", "qty": 260, "price": None},
                                {"warehouse_id": 6, "material_name": "Zamok", "qty": 20, "price": 2000}
                            ]
                        }
                    ]
                },
                response_only=True,
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        data = request.data

        # Agar bitta dict kelgan bo'lsa, uni ro'yxatga o'giramiz
        if isinstance(data, dict):
            # Ehtimol data ichida 'products' yoki 'orders' kaliti bo'lishi mumkin
            if 'products' in data and isinstance(data['products'], list):
                orders_data = data['products']
            else:
                orders_data = [data]
        elif isinstance(data, list):
            orders_data = data
        else:
            return Response(
                {"error": "Yuborilgan ma'lumot ro'yxat (list) yoki obyekt (dict) bo'lishi shart!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = OrderItemRequestSerializer(data=orders_data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = calculate_product_materials(serializer.validated_data)
            return Response(result, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Kutilmagan xatolik yuz berdi: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Mahsulotlar ro'yxati va tafsilotlari"""
    queryset = Product.objects.all().prefetch_related('product_materials__material')
    serializer_class = ProductSerializer


class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    """Xomashyolar ro'yxati"""
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class WarehouseViewSet(viewsets.ReadOnlyModelViewSet):
    """Omborxona partiyalari ro'yxati"""
    queryset = Warehouse.objects.all().select_related('material')
    serializer_class = WarehouseSerializer
