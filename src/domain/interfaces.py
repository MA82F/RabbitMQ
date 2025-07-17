from abc import ABC, abstractmethod
from typing import Protocol
from .entities import ImageProcessingTask, ProcessingResult


class IImageProcessor(ABC):
    """Interface برای پردازش تصویر"""
    
    @abstractmethod
    def process(self, image_path: str) -> str:
        """پردازش تصویر و بازگردانی مسیر فایل خروجی"""
        pass


class IFileStorage(ABC):
    """Interface برای ذخیره فایل"""
    
    @abstractmethod
    def upload_file(self, local_path: str, remote_path: str) -> bool:
        """آپلود فایل به storage"""
        pass


class IMessagePublisher(ABC):
    """Interface برای ارسال پیام"""
    
    @abstractmethod
    def publish_result(self, result: ProcessingResult) -> None:
        """ارسال نتیجه پردازش"""
        pass


class IMessageConsumer(ABC):
    """Interface برای دریافت پیام"""
    
    @abstractmethod
    def start_consuming(self, callback) -> None:
        """شروع گوش دادن به پیام‌ها"""
        pass
