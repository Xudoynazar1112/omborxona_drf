from django.core.management.base import BaseCommand
from warehouse.models import Product, Material, ProductMaterial, Warehouse


class Command(BaseCommand):
    help = "Vazifadagi boshlang'ich ma'lumotlarni (Product, Material, ProductMaterial, Warehouse) bazaga yuklaydi"

    def handle(self, *args, **options):
        self.stdout.write("Eski ma'lumotlar tozalanmoqda...")
        ProductMaterial.objects.all().delete()
        Warehouse.objects.all().delete()
        Product.objects.all().delete()
        Material.objects.all().delete()

        self.stdout.write("Xomashyolar (Material) yaratilmoqda...")
        mato = Material.objects.create(id=1, material_name="Mato")
        ip = Material.objects.create(id=2, material_name="Ip")
        tugma = Material.objects.create(id=3, material_name="Tugma")
        zamok = Material.objects.create(id=4, material_name="Zamok")

        self.stdout.write("Mahsulotlar (Product) yaratilmoqda...")
        koylak = Product.objects.create(id=1, product_name="Koylak", product_code=238923)
        shim = Product.objects.create(id=2, product_name="Shim", product_code=498723)

        self.stdout.write("Mahsulot xomashyolari (ProductMaterial) yaratilmoqda...")
        # Koylak uchun xomashyo normalari:
        # 1 ta koylak uchun: 0.8 mato, 5 tugma, 10 ip
        ProductMaterial.objects.create(product=koylak, material=mato, quantity=0.8)
        ProductMaterial.objects.create(product=koylak, material=tugma, quantity=5.0)
        ProductMaterial.objects.create(product=koylak, material=ip, quantity=10.0)

        # Shim uchun xomashyo normalari:
        # 1 ta shim uchun: 1.4 mato, 15 ip (20 ta shim uchun 300 ip), 1 zamok
        ProductMaterial.objects.create(product=shim, material=mato, quantity=1.4)
        ProductMaterial.objects.create(product=shim, material=ip, quantity=15.0)
        ProductMaterial.objects.create(product=shim, material=zamok, quantity=1.0)

        self.stdout.write("Omborxona partiyalari (Warehouse) yaratilmoqda...")
        # Vazifadagi rasm bo'yicha aniq partiyalar:
        # № 1: Mato, 12 qoldiq, narx 1500
        # № 2: Mato, 200 qoldiq, narx 1600
        # № 3: Ip, 40 qoldiq, narx 500
        # № 4: Ip, 300 qoldiq, narx 550
        # № 5: Tugma, 500 qoldiq, narx 300
        # № 6: Zamok, 1000 qoldiq, narx 2000
        Warehouse.objects.create(id=1, material=mato, remainder=12.0, price=1500.0)
        Warehouse.objects.create(id=2, material=mato, remainder=200.0, price=1600.0)
        Warehouse.objects.create(id=3, material=ip, remainder=40.0, price=500.0)
        Warehouse.objects.create(id=4, material=ip, remainder=300.0, price=550.0)
        Warehouse.objects.create(id=5, material=tugma, remainder=500.0, price=300.0)
        Warehouse.objects.create(id=6, material=zamok, remainder=1000.0, price=2000.0)

        self.stdout.write(self.style.SUCCESS("Barcha boshlang'ich ma'lumotlar muvaffaqiyatli yuklandi!"))
