import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class AppConfig:
    """تنظیمات برنامه"""
    # RabbitMQ
    rabbitmq_host: str
    queue_name: str
    response_queue: str
    
    # MinIO
    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket: str
    
    # Image Processing
    image_quality: int = 60

    @classmethod
    def from_env(cls) -> 'AppConfig':
        """ایجاد configuration از متغیرهای محیطی"""
        return cls(
            rabbitmq_host=os.getenv("RABBITMQ_HOST", "localhost"),
            queue_name=os.getenv("RABBITMQ_QUEUE", "image_tasks"),
            response_queue=os.getenv("RABBITMQ_RESPONSE_QUEUE", "image_responses"),
            minio_endpoint=os.getenv("MINIO_ENDPOINT", "https://mymin.darkube.app"),
            minio_access_key=os.getenv("MINIO_ACCESS_KEY", "zg5UaX56OxCVaTvPZ3Hn"),
            minio_secret_key=os.getenv("MINIO_SECRET_KEY", "wLJfbqIo8DCnBc23Fv8g2tdVQqDOrLsq4jICzYAS"),
            minio_bucket=os.getenv("MINIO_BUCKET", "processed"),
            image_quality=int(os.getenv("IMAGE_QUALITY", "60"))
        )
