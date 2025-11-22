import os
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Generate dummy media images (hero, banners, products) in MEDIA_ROOT"

    def handle(self, *args, **options):
        try:
            from PIL import Image, ImageDraw, ImageFont
        except Exception:
            self.stderr.write(self.style.ERROR("Pillow is required. Install with: pip install Pillow"))
            return

        media_root: Path = Path(settings.MEDIA_ROOT)
        (media_root / "hero").mkdir(parents=True, exist_ok=True)
        (media_root / "banners").mkdir(parents=True, exist_ok=True)
        (media_root / "products").mkdir(parents=True, exist_ok=True)

        # Try to load a default font
        try:
            font = ImageFont.load_default()
        except Exception:
            font = None

        def create_image(path: Path, size, bg_color, text: str):
            img = Image.new("RGB", size, color=bg_color)
            draw = ImageDraw.Draw(img)
            text_color = (255, 255, 255)
            try:
                tw, th = draw.textsize(text, font=font)
            except Exception:
                tw, th = (0, 0)
            x = (size[0] - tw) // 2
            y = (size[1] - th) // 2
            draw.text((x, y), text, fill=text_color, font=font)
            img.save(path, format="JPEG", quality=85)

        # Hero images
        create_image(media_root / "hero" / "hero1.jpg", (1600, 600), (85, 107, 47), "HERO IMAGE 1")
        create_image(media_root / "hero" / "hero2.jpg", (1600, 600), (61, 90, 64), "HERO IMAGE 2")

        # Banners
        create_image(media_root / "banners" / "banner1.jpg", (1400, 400), (45, 56, 45), "BANNER 1")
        create_image(media_root / "banners" / "banner2.jpg", (1400, 400), (32, 40, 34), "BANNER 2")

        # Product images
        product_colors = [
            (110, 123, 70),
            (92, 107, 62),
            (76, 89, 56),
            (58, 71, 49),
            (40, 54, 42),
            (30, 41, 34),
        ]
        for idx, color in enumerate(product_colors, start=1):
            create_image(media_root / "products" / f"sample{idx}.jpg", (800, 800), color, f"PRODUCT {idx}")

        self.stdout.write(self.style.SUCCESS(f"Dummy media created under {media_root}"))


