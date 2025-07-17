from ..application.services import ImageProcessingService
from ..infrastructure.config import AppConfig
from ..infrastructure.image_processor import PillowImageProcessor
from ..infrastructure.storage import MinIOStorage
from ..infrastructure.messaging import RabbitMQPublisher, RabbitMQConsumer


class DIContainer:
    """Dependency Injection Container"""
    
    def __init__(self, config: AppConfig):
        self.config = config
        self._setup_dependencies()
    
    def _setup_dependencies(self):
        """راه‌اندازی وابستگی‌ها"""
        # Infrastructure services
        self.image_processor = PillowImageProcessor(quality=self.config.image_quality)
        
        self.file_storage = MinIOStorage(
            endpoint=self.config.minio_endpoint,
            access_key=self.config.minio_access_key,
            secret_key=self.config.minio_secret_key,
            bucket=self.config.minio_bucket
        )
        
        self.message_publisher = RabbitMQPublisher(
            host=self.config.rabbitmq_host,
            response_queue=self.config.response_queue
        )
        
        self.message_consumer = RabbitMQConsumer(
            host=self.config.rabbitmq_host,
            queue_name=self.config.queue_name
        )
        
        # Application services
        self.image_processing_service = ImageProcessingService(
            image_processor=self.image_processor,
            file_storage=self.file_storage,
            message_publisher=self.message_publisher
        )
