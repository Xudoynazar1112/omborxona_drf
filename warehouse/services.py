from typing import List, Dict, Any, Union
from collections import defaultdict
from warehouse.models import Product, Warehouse


def clean_number(value: Union[float, int, None]) -> Union[int, float, None]:
    """
    Agar son butun bo'lsa (masalan 12.0), int sifatida (12),
    kasr bo'lsa float sifatida qaytaradi.
    """
    if value is None:
        return None
    if isinstance(value, (int, float)):
        if float(value).is_integer():
            return int(value)
        return round(float(value), 4)
    return value


def calculate_product_materials(orders: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Mahsulotlar va ularning miqdorlari ro'yxatini qabul qilib,
    har bir mahsulot uchun omborxona partiyalaridan xomashyolarni
    FIFO asosida hisoblab beruvchi asosiy servis funksiyasi.

    MUHIM:
    - Bazadagi Warehouse.remainder o'zgarmaydi.
    - Hisoblash faqat xotirada (in-memory) virtual qoldiqlar orqali olib boriladi.
    - Avvalgi mahsulotlar olgan qoldiqlar keyingi mahsulotlar uchun hisobga olinadi.
    - Yetmay qolgan xomashyo warehouse_id: null, price: null bilan ko'rsatiladi.
    """
    # Ombordagi barcha partiyalarning virtual qoldiqlarini xotirada saqlash
    # FIFO tartibida (id bo'yicha o'sish tartibida)
    warehouses = Warehouse.objects.select_related('material').order_by('id')
    
    # Har bir material bo'yicha partiyalar ro'yxati va ularning virtual qoldiqlari
    warehouse_batches_by_material = defaultdict(list)
    for wh in warehouses:
        warehouse_batches_by_material[wh.material_id].append({
            'id': wh.id,
            'material_name': wh.material.material_name,
            'virtual_remainder': float(wh.remainder),
            'price': float(wh.price),
        })

    result = []

    for order in orders:
        product_code = order.get('product_code')
        order_qty = order.get('quantity', 0)

        try:
            product = Product.objects.prefetch_related(
                'product_materials__material'
            ).get(product_code=product_code)
        except Product.DoesNotExist:
            raise ValueError(f"product_code={product_code} bo'lgan mahsulot topilmadi!")

        product_result = {
            "product_name": product.product_name,
            "product_qty": clean_number(order_qty),
            "product_materials": []
        }

        # Mahsulot uchun kerakli har bir xomashyoni hisoblash
        for pm in product.product_materials.all():
            material_id = pm.material_id
            material_name = pm.material.material_name
            total_needed = float(pm.quantity) * float(order_qty)
            remaining_needed = total_needed

            # Ushbu material uchun mavjud partiyalarni ko'rib chiqamiz
            batches = warehouse_batches_by_material.get(material_id, [])

            for batch in batches:
                if remaining_needed <= 0:
                    break

                if batch['virtual_remainder'] > 0:
                    if batch['virtual_remainder'] >= remaining_needed:
                        # Ushbu partiya yetarli
                        allocated_qty = remaining_needed
                        batch['virtual_remainder'] -= allocated_qty
                        remaining_needed = 0.0

                        product_result["product_materials"].append({
                            "warehouse_id": batch['id'],
                            "material_name": material_name,
                            "qty": clean_number(allocated_qty),
                            "price": clean_number(batch['price'])
                        })
                    else:
                        # Ushbu partiyadagi borini olib, qolganini keyingi partiyadan qidiramiz
                        allocated_qty = batch['virtual_remainder']
                        remaining_needed -= allocated_qty
                        batch['virtual_remainder'] = 0.0

                        product_result["product_materials"].append({
                            "warehouse_id": batch['id'],
                            "material_name": material_name,
                            "qty": clean_number(allocated_qty),
                            "price": clean_number(batch['price'])
                        })

            # Agar partiyalar tugasa-yu, xomashyo hali ham yetmay qolsa
            if remaining_needed > 0:
                product_result["product_materials"].append({
                    "warehouse_id": None,
                    "material_name": material_name,
                    "qty": clean_number(remaining_needed),
                    "price": None
                })

        result.append(product_result)

    return {"result": result}
