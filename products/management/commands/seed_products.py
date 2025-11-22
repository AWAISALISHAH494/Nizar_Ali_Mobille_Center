from django.core.management.base import BaseCommand
from django.utils import timezone

from products.models import Category, Brand, Product


class Command(BaseCommand):
    help = "Seed database with sample mobile accessories products, categories, and brands"

    def handle(self, *args, **options):
        categories_data = [
            ("Chargers", "Fast wall chargers and adapters"),
            ("Cables", "USB-C, Lightning, and Micro-USB cables"),
            ("Power Banks", "Portable power banks for all devices"),
            ("Earphones", "Wired and wireless earphones / earbuds"),
            ("Phone Cases", "Protective and stylish phone cases"),
            ("Screen Protectors", "Tempered glass and film protectors"),
        ]

        brands_data = [
            ("Anker", "Charging and mobile accessories"),
            ("Baseus", "Innovative mobile accessories"),
            ("Aukey", "Value tech accessories"),
            ("Samsung", "Genuine Samsung accessories"),
        ]

        category_objs = {}
        for name, desc in categories_data:
            cat, _ = Category.objects.get_or_create(name=name, defaults={"description": desc, "is_active": True})
            category_objs[name] = cat
        # Deactivate any legacy categories not in our target list
        Category.objects.exclude(name__in=[name for name, _ in categories_data]).update(is_active=False)

        brand_objs = {}
        for name, desc in brands_data:
            br, _ = Brand.objects.get_or_create(name=name, defaults={"description": desc, "is_active": True})
            brand_objs[name] = br
        # Ensure only these demo brands are active (optional)
        Brand.objects.exclude(name__in=[name for name, _ in brands_data]).update(is_active=False)

        products = [
            {
                "name": "Anker 20W USB-C Fast Charger",
                "short_description": "Compact PD wall adapter for iPhone/Android",
                "description": "Fast-charging 20W USB-C adapter with Power Delivery for modern phones.",
                "category": category_objs["Chargers"],
                "brand": brand_objs["Anker"],
                "sku": "CHG-ANKER-20W-001",
                "price": 19.99,
                "compare_price": 24.99,
                "cost_price": 9.00,
                "weight": 0.18,
                "dimensions": "1.7x1.7x1.1 in",
                "is_featured": True,
            },
            {
                "name": "Baseus 65W GaN Charger",
                "short_description": "Multi-port fast charger (USB-C + USB-A)",
                "description": "GaN technology charger with high efficiency and low heat output.",
                "category": category_objs["Chargers"],
                "brand": brand_objs["Baseus"],
                "sku": "CHG-BASEUS-65W-002",
                "price": 39.99,
                "compare_price": 49.99,
                "cost_price": 24.00,
                "weight": 0.35,
                "dimensions": "2.2x1.9x1.1 in",
                "is_featured": True,
            },
            {
                "name": "USB-C to USB-C Cable (1m)",
                "short_description": "Durable braided PD cable",
                "description": "Supports up to 60W charging with reinforced strain relief.",
                "category": category_objs["Cables"],
                "brand": brand_objs["Aukey"],
                "sku": "CBL-USBC-1M-003",
                "price": 7.99,
                "compare_price": 10.99,
                "cost_price": 3.20,
                "weight": 0.10,
                "dimensions": "1m",
                "is_featured": True,
            },
            {
                "name": "Lightning to USB-C Cable (1m)",
                "short_description": "MFi certified fast charge cable",
                "description": "Apple MFi certified cable for iPhone/iPad fast charging.",
                "category": category_objs["Cables"],
                "brand": brand_objs["Anker"],
                "sku": "CBL-LTG-1M-004",
                "price": 14.99,
                "compare_price": 19.99,
                "cost_price": 6.00,
                "weight": 0.08,
                "dimensions": "1m",
                "is_featured": False,
            },
            {
                "name": "10,000mAh Power Bank",
                "short_description": "Slim portable PD power bank",
                "description": "USB-C PD and USB-A ports with LED charge indicators.",
                "category": category_objs["Power Banks"],
                "brand": brand_objs["Baseus"],
                "sku": "PWB-10000-005",
                "price": 24.99,
                "compare_price": 34.99,
                "cost_price": 12.00,
                "weight": 0.42,
                "dimensions": "5.4x2.6x0.5 in",
                "is_featured": True,
            },
            {
                "name": "Samsung 25W Super Fast Charger",
                "short_description": "Official Samsung USB-C charger",
                "description": "Genuine Samsung charger for Galaxy devices with PPS.",
                "category": category_objs["Chargers"],
                "brand": brand_objs["Samsung"],
                "sku": "CHG-SAMS-25W-006",
                "price": 21.99,
                "compare_price": 29.99,
                "cost_price": 11.00,
                "weight": 0.20,
                "dimensions": "2.0x1.6x0.9 in",
                "is_featured": False,
            },
            {
                "name": "Wireless Earbuds (BT 5.3)",
                "short_description": "In-ear earbuds with charging case",
                "description": "Low-latency, touch controls, 24h total playback.",
                "category": category_objs["Earphones"],
                "brand": brand_objs["Aukey"],
                "sku": "EAR-WLS-007",
                "price": 29.99,
                "compare_price": 39.99,
                "cost_price": 15.00,
                "weight": 0.15,
                "dimensions": "Case 2.1x1.8x1.0 in",
                "is_featured": True,
            },
            {
                "name": "Silicone Case - iPhone 14",
                "short_description": "Soft-touch protective case",
                "description": "Anti-shock corners and microfiber lining.",
                "category": category_objs["Phone Cases"],
                "brand": brand_objs["Baseus"],
                "sku": "CASE-IP14-SIL-008",
                "price": 12.99,
                "compare_price": 16.99,
                "cost_price": 5.50,
                "weight": 0.12,
                "dimensions": "iPhone 14",
                "is_featured": False,
            },
            {
                "name": "Tempered Glass - Samsung S23",
                "short_description": "9H hardness screen protector",
                "description": "Oleophobic coating with installation frame.",
                "category": category_objs["Screen Protectors"],
                "brand": brand_objs["Samsung"],
                "sku": "GLS-S23-009",
                "price": 9.99,
                "compare_price": 12.99,
                "cost_price": 3.50,
                "weight": 0.05,
                "dimensions": "S23",
                "is_featured": False,
            },
            {
                "name": "3-in-1 Charging Cable",
                "short_description": "USB-A to USB-C/Lightning/Micro-USB",
                "description": "One cable to charge multiple devices with braided jacket.",
                "category": category_objs["Cables"],
                "brand": brand_objs["Anker"],
                "sku": "CBL-3IN1-010",
                "price": 13.99,
                "compare_price": 17.99,
                "cost_price": 6.20,
                "weight": 0.1,
                "dimensions": "1.2m",
                "is_featured": False,
            },
        ]

        created = 0
        for data in products:
            obj, was_created = Product.objects.get_or_create(
                sku=data["sku"],
                defaults={
                    "name": data["name"],
                    "description": data["description"],
                    "short_description": data["short_description"],
                    "category": data["category"],
                    "brand": data["brand"],
                    "price": data["price"],
                    "compare_price": data["compare_price"],
                    "cost_price": data["cost_price"],
                    "weight": data["weight"],
                    "dimensions": data["dimensions"],
                    "status": "published",
                    "is_featured": data["is_featured"],
                    "track_inventory": True,
                    "allow_backorder": True,
                },
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {created} products (or ensured they exist)."))


