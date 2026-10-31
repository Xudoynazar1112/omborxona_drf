from rest_framework import serializers
from warehouse.models import Product, Material, ProductMaterial, Warehouse


class OrderItemRequestSerializer(serializers.Serializer):
    product_code = serializers.IntegerField(
        required=True,
        help_text="Mahsulot kodi (masalan: 238923)"
    )
    quantity = serializers.FloatField(
        required=True,
        min_value=0.0001,
        help_text="Ishlab chiqarilishi kerak bo'lgan mahsulot soni"
    )


class ProductMaterialResponseSerializer(serializers.Serializer):
    warehouse_id = serializers.IntegerField(
        allow_null=True,
        help_text="Ombor partiyasi ID raqami. Agar partiya yetmay qolsa null."
    )
    material_name = serializers.CharField(help_text="Xomashyo nomi")
    qty = serializers.FloatField(help_text="Olingan yoki yetishmayotgan miqdor")
    price = serializers.FloatField(
        allow_null=True,
        help_text="Partiyadagi narx. Agar yetishmayotgan xomashyo bo'lsa null."
    )


class ProductCalculationResultSerializer(serializers.Serializer):
    product_name = serializers.CharField(help_text="Mahsulot nomi")
    product_qty = serializers.FloatField(help_text="Mahsulot miqdori")
    product_materials = ProductMaterialResponseSerializer(many=True)


class CalculationResponseSerializer(serializers.Serializer):
    result = ProductCalculationResultSerializer(many=True)


# Model Serializers for standard CRUD / inspection
class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'material_name']


class ProductMaterialSerializer(serializers.ModelSerializer):
    material_name = serializers.ReadOnlyField(source='material.material_name')

    class Meta:
        model = ProductMaterial
        fields = ['id', 'product', 'material', 'material_name', 'quantity']


class ProductSerializer(serializers.ModelSerializer):
    product_materials = ProductMaterialSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_code', 'product_materials']


class WarehouseSerializer(serializers.ModelSerializer):
    material_name = serializers.ReadOnlyField(source='material.material_name')

    class Meta:
        model = Warehouse
        fields = ['id', 'material', 'material_name', 'remainder', 'price']
