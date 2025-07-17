from PIL import Image
import os
from ..domain.interfaces import IImageProcessor


class PillowImageProcessor(IImageProcessor):
    """پیاده‌سازی پردازش تصویر با Pillow"""
    
    def __init__(self, quality: int = 60):
        self.quality = quality
    
    def process(self, image_path: str) -> str:
        """تبدیل تصویر به grayscale و فشرده‌سازی"""
        try:
            # باز کردن و تبدیل به grayscale
            img = Image.open(image_path).convert('L')
            
            # تعیین مسیر خروجی
            output_path = f"processed_{os.path.basename(image_path)}"
            
            # ذخیره با فشرده‌سازی
            img.save(output_path, optimize=True, quality=self.quality)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"خطا در پردازش تصویر: {str(e)}")
