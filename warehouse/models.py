from django.db import models


class Product(models.Model):
    product_name = models.CharField(max_length=255, verbose_name="Mahsulot nomi")
    product_code = models.IntegerField(unique=True, verbose_name="Mahsulot kodi")

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ['id']

    def __str__(self):
        return f"{self.product_name} ({self.product_code})"


class Material(models.Model):
    material_name = models.CharField(max_length=255, verbose_name="Xomashyo nomi")

    class Meta:
        verbose_name = "Xomashyo"
        verbose_name_plural = "Xomashyolar"
        ordering = ['id']

    def __str__(self):
        return self.material_name


class ProductMaterial(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_materials',
        verbose_name="Mahsulot"
    )
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name='product_materials',
        verbose_name="Xomashyo"
    )
    quantity = models.FloatField(verbose_name="1 dona mahsulot uchun miqdor")

    class Meta:
        verbose_name = "Mahsulot xomashyosi"
        verbose_name_plural = "Mahsulot xomashyolari"
        ordering = ['id']

    def __str__(self):
        return f"{self.product.product_name} -> {self.material.material_name}: {self.quantity}"


class Warehouse(models.Model):
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name='warehouses',
        verbose_name="Xomashyo"
    )
    remainder = models.FloatField(verbose_name="Partiyadagi qoldiq")
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Partiya narxi"
    )

    class Meta:
        verbose_name = "Omborxona partiyasi"
        verbose_name_plural = "Omborxona partiyalari"
        ordering = ['id']

    def __str__(self):
        return f"Partiya #{self.id}: {self.material.material_name} - Qoldiq: {self.remainder}, Narx: {self.price}"
