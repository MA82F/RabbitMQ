# Image Processor Server - Onion Architecture

این پروژه یک سرویس پردازش تصویر است که با معماری Onion پیاده‌سازی شده است.

## معماری

### Onion Architecture Layers:

1. **Domain Layer** (`src/domain/`): مرکز معماری

   - `entities.py`: Entity ها و Business Objects
   - `interfaces.py`: Abstract interfaces و contracts

2. **Application Layer** (`src/application/`): Use Cases

   - `services.py`: Application Services و Use Cases

3. **Infrastructure Layer** (`src/infrastructure/`): External Dependencies

   - `image_processor.py`: پیاده‌سازی پردازش تصویر با Pillow
   - `storage.py`: پیاده‌سازی ذخیره فایل در MinIO
   - `messaging.py`: پیاده‌سازی پیام‌رسانی با RabbitMQ
   - `config.py`: مدیریت تنظیمات
   - `di_container.py`: Dependency Injection

4. **Presentation Layer** (`src/presentation/`): Entry Points
   - `app.py`: Main application class

## مزایای این معماری:

- **Separation of Concerns**: هر لایه مسئولیت مشخصی دارد
- **Testability**: قابلیت تست بالا با mock کردن dependencies
- **Maintainability**: قابلیت نگهداری و توسعه آسان
- **Flexibility**: امکان تغییر پیاده‌سازی بدون تأثیر روی لایه‌های دیگر

## نحوه اجرا:

```bash
# نصب dependencies
pip install -r requirements.txt

# اجرای سرویس
python main.py

# ارسال پیام تست
python send_test_message.py
```

## متغیرهای محیطی:

```env
RABBITMQ_HOST=localhost
RABBITMQ_QUEUE=image_tasks
RABBITMQ_RESPONSE_QUEUE=image_responses
MINIO_ENDPOINT=https://mymin.darkube.app
MINIO_ACCESS_KEY=your_access_key
MINIO_SECRET_KEY=your_secret_key
MINIO_BUCKET=processed
IMAGE_QUALITY=60
```
