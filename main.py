#!/usr/bin/env python3
"""
Image Processor Server با معماری Onion
"""

from src.infrastructure.config import AppConfig
from src.infrastructure.di_container import DIContainer
from src.presentation.app import ImageProcessorApp


def main():
    """نقطه ورود اصلی برنامه"""
    # بارگذاری تنظیمات
    config = AppConfig.from_env()
    
    # راه‌اندازی Dependency Injection
    container = DIContainer(config)
    
    # ایجاد و اجرای برنامه
    app = ImageProcessorApp(
        processing_service=container.image_processing_service,
        message_consumer=container.message_consumer
    )
    
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n🛑 برنامه متوقف شد")
    except Exception as e:
        print(f"❌ خطای غیرمنتظره: {e}")


if __name__ == "__main__":
    main()
