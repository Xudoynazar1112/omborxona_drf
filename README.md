# Omborxona Tizimi (Warehouse Material Allocation REST API)

Ushbu loyiha **Mohirdev** platformasining **“Omborxona tizimi – Mock Task”** amaliy topshirig'i uchun ishlab chiqilgan.

Loyiha ishlab chiqarish korxonasida berilgan mahsulotlarni ishlab chiqarish uchun kerak bo‘ladigan xomashyolarni omborxonadagi partiyalar (FIFO) bo‘yicha hisoblab, qaysi partiyadan qancha olinishini aniqlab beruvchi **REST API** xizmatini taqdim etadi.

---

## 🚀 Texnologiyalar
* **Python**: 3.11+
* **Django**: 5.x
* **Django REST Framework (DRF)**: 3.15+
* **drf-spectacular**: OpenAPI 3.0 & Swagger UI hujjatlashtirish
* **SQLite3**: Ma'lumotlar bazasi

---

## 📌 Asosiy Xususiyatlar va Algoritm Qoidalari
1. **FIFO (First In, First Out) partiya taqsimoti**:
   Xomashyolar partiyalar bo'yicha ketma-ket (boshlang'ich partiyalardan boshlab) olinadi.
2. **Bazadagi ma'lumotlar daxlsizligi**:
   Hisoblash jarayonida `Warehouse` jadvalidagi `remainder` qiymati bazadan kamaytirilmaydi. Barcha hisob-kitoblar virtual (xotirada) olib boriladi.
3. **Ketma-ket virtual hisob-kitob**:
   Oldingi mahsulotlar (masalan: Ko‘ylak) olgan xomashyolar miqdori keyingi mahsulotlar (masalan: Shim) uchun hisobga olinadi.
4. **Yetishmayotgan xomashyolar**:
   Agar omborda xomashyo partiyalari tugasa yoki yetarli bo‘lmasa, yetishmayotgan miqdor quyidagicha qaytariladi:
   * `"warehouse_id": null`
   * `"price": null`
   * `"qty": <yetishmayotgan_miqdor>`

---

## 🛠 O'rnatish va Ishga Tushirish

### 1. Virtual muhitni faollashtirish
```bash
# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 2. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 3. Migratsiyalarni qo'llash
```bash
python manage.py migrate
```

### 4. Boshlang'ich test ma'lumotlarini yuklash
Vazifadagi barcha xomashyolar, mahsulotlar, ularning normalari va omborxona partiyalari jadvalini bir buyruq bilan bazaga yuklash:
```bash
python manage.py seed_data
```

### 5. Serverni ishga tushirish
```bash
python manage.py runserver
```

Server ishga tushgach, brauzerda quyidagi manzillarga kirish mumkin:
* **Swagger UI (Interaktiv API)**: [http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/) yoki [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **Redoc**: [http://127.0.0.1:8000/api/schema/redoc/](http://127.0.0.1:8000/api/schema/redoc/)
* **Admin panel**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🧪 Avtomatlashtirilgan Testlarni Ishga Tushirish
Barcha biznes-mantiq va API endpointlar 100% testlar bilan qoplangan:
```bash
python manage.py test
```

---

## 📡 API Qo'llanmasi

### Endpoint:
`POST /api/v1/warehouse/calculate/` (yoki `/api/calculate/`)

#### Kiruvchi so'rov (Request Body):
```json
[
  {
    "product_code": 238923,
    "quantity": 30
  },
  {
    "product_code": 498723,
    "quantity": 20
  }
]
```

#### Kutilayotgan javob (Response 200 OK):
```json
{
  "result": [
    {
      "product_name": "Koylak",
      "product_qty": 30,
      "product_materials": [
        {
          "warehouse_id": 1,
          "material_name": "Mato",
          "qty": 12,
          "price": 1500
        },
        {
          "warehouse_id": 2,
          "material_name": "Mato",
          "qty": 12,
          "price": 1600
        },
        {
          "warehouse_id": 5,
          "material_name": "Tugma",
          "qty": 150,
          "price": 300
        },
        {
          "warehouse_id": 3,
          "material_name": "Ip",
          "qty": 40,
          "price": 500
        },
        {
          "warehouse_id": 4,
          "material_name": "Ip",
          "qty": 260,
          "price": 550
        }
      ]
    },
    {
      "product_name": "Shim",
      "product_qty": 20,
      "product_materials": [
        {
          "warehouse_id": 2,
          "material_name": "Mato",
          "qty": 28,
          "price": 1600
        },
        {
          "warehouse_id": 4,
          "material_name": "Ip",
          "qty": 40,
          "price": 550
        },
        {
          "warehouse_id": null,
          "material_name": "Ip",
          "qty": 260,
          "price": null
        },
        {
          "warehouse_id": 6,
          "material_name": "Zamok",
          "qty": 20,
          "price": 2000
        }
      ]
    }
  ]
}
```

---

## 📊 Ma'lumotlar Bazasi Tuzilishi
1. **`Product`**: Ishlab chiqariladigan mahsulotlar (`product_name`, `product_code`).
2. **`Material`**: Xomashyolar (`material_name`).
3. **`ProductMaterial`**: 1 dona mahsulot uchun sarflanadigan norma (`product`, `material`, `quantity`).
4. **`Warehouse`**: Ombordagi partiyalar jamlanmasi (`material`, `remainder`, `price`).
