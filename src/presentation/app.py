from ..application.services import ImageProcessingService
from ..infrastructure.messaging import RabbitMQConsumer


class ImageProcessorApp:
    """Entry point برنامه"""
    
    def __init__(
        self,
        processing_service: ImageProcessingService,
        message_consumer: RabbitMQConsumer
    ):
        self.processing_service = processing_service
        self.message_consumer = message_consumer
    
    def run(self):
        """اجرای برنامه"""
        print("🚀 سرویس پردازش تصویر شروع شد...")
        
        # تعریف callback برای پردازش پیام‌ها
        def handle_message(image_path: str):
            self.processing_service.process_image_task(image_path)
        
        # شروع گوش دادن به پیام‌ها
        self.message_consumer.start_consuming(handle_message)
