from rest_framework import serializers
from .models import Product, ProductMaterial, Warehouse


class WarehouseSerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(source='material.name')

    class Meta:
        model = Warehouse
        fields = ['id', 'material_name', 'remainder', 'price']


class ProductMaterialSerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(source='material.name')
    warehouses = serializers.SerializerMethodField()

    class Meta:
        model = ProductMaterial
        fields = ['material_name', 'quantity', 'warehouses']

    def get_warehouses(self, obj):
        warehouses = Warehouse.objects.filter(material=obj.material)
        return WarehouseSerializer(warehouses, many=True).data


class ProductSerializer(serializers.ModelSerializer):
    product_materials = ProductMaterialSerializer('product_materials', many=True)

    class Meta:
        model = Product
        fields = ['name', 'code', 'product_materials']
