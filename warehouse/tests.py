from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from warehouse.models import Product, Material, ProductMaterial, Warehouse
from warehouse.services import calculate_product_materials


class WarehouseAllocationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Xomashyolar
        self.mato = Material.objects.create(id=1, material_name="Mato")
        self.ip = Material.objects.create(id=2, material_name="Ip")
        self.tugma = Material.objects.create(id=3, material_name="Tugma")
        self.zamok = Material.objects.create(id=4, material_name="Zamok")

        # Mahsulotlar
        self.koylak = Product.objects.create(id=1, product_name="Koylak", product_code=238923)
        self.shim = Product.objects.create(id=2, product_name="Shim", product_code=498723)

        # Mahsulot retseptlari (normalari)
        ProductMaterial.objects.create(product=self.koylak, material=self.mato, quantity=0.8)
        ProductMaterial.objects.create(product=self.koylak, material=self.tugma, quantity=5.0)
        ProductMaterial.objects.create(product=self.koylak, material=self.ip, quantity=10.0)

        ProductMaterial.objects.create(product=self.shim, material=self.mato, quantity=1.4)
        ProductMaterial.objects.create(product=self.shim, material=self.ip, quantity=15.0)
        ProductMaterial.objects.create(product=self.shim, material=self.zamok, quantity=1.0)

        # Omborxona partiyalari (vazifadagi rasm bo'yicha)
        Warehouse.objects.create(id=1, material=self.mato, remainder=12.0, price=1500.0)
        Warehouse.objects.create(id=2, material=self.mato, remainder=200.0, price=1600.0)
        Warehouse.objects.create(id=3, material=self.ip, remainder=40.0, price=500.0)
        Warehouse.objects.create(id=4, material=self.ip, remainder=300.0, price=550.0)
        Warehouse.objects.create(id=5, material=self.tugma, remainder=500.0, price=300.0)
        Warehouse.objects.create(id=6, material=self.zamok, remainder=1000.0, price=2000.0)

    def test_mohirdev_example_calculation(self):
        """Vazifadagi misol so'rov bo'yicha to'liq hisoblash testi"""
        orders = [
            {"product_code": 238923, "quantity": 30},
            {"product_code": 498723, "quantity": 20}
        ]
        response_data = calculate_product_materials(orders)
        result = response_data["result"]

        self.assertEqual(len(result), 2)

        # 1. Koylak tekshiruvi
        koylak_res = result[0]
        self.assertEqual(koylak_res["product_name"], "Koylak")
        self.assertEqual(koylak_res["product_qty"], 30)
        self.assertEqual(koylak_res["product_materials"], [
            {"warehouse_id": 1, "material_name": "Mato", "qty": 12, "price": 1500},
            {"warehouse_id": 2, "material_name": "Mato", "qty": 12, "price": 1600},
            {"warehouse_id": 5, "material_name": "Tugma", "qty": 150, "price": 300},
            {"warehouse_id": 3, "material_name": "Ip", "qty": 40, "price": 500},
            {"warehouse_id": 4, "material_name": "Ip", "qty": 260, "price": 550}
        ])

        # 2. Shim tekshiruvi
        shim_res = result[1]
        self.assertEqual(shim_res["product_name"], "Shim")
        self.assertEqual(shim_res["product_qty"], 20)
        self.assertEqual(shim_res["product_materials"], [
            {"warehouse_id": 2, "material_name": "Mato", "qty": 28, "price": 1600},
            {"warehouse_id": 4, "material_name": "Ip", "qty": 40, "price": 550},
            {"warehouse_id": None, "material_name": "Ip", "qty": 260, "price": None},
            {"warehouse_id": 6, "material_name": "Zamok", "qty": 20, "price": 2000}
        ])

        # 3. Bazadagi ombor qoldiqlari o'zgarmaganligini tekshirish
        self.assertEqual(Warehouse.objects.get(id=1).remainder, 12.0)
        self.assertEqual(Warehouse.objects.get(id=2).remainder, 200.0)
        self.assertEqual(Warehouse.objects.get(id=3).remainder, 40.0)
        self.assertEqual(Warehouse.objects.get(id=4).remainder, 300.0)
        self.assertEqual(Warehouse.objects.get(id=5).remainder, 500.0)
        self.assertEqual(Warehouse.objects.get(id=6).remainder, 1000.0)

    def test_api_endpoint(self):
        """REST API endpoint orqali POST so'rovini tekshirish"""
        url = reverse('calculate-materials')
        payload = [
            {"product_code": 238923, "quantity": 30},
            {"product_code": 498723, "quantity": 20}
        ]
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("result", response.data)
        self.assertEqual(len(response.data["result"]), 2)
