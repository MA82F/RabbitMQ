import pika
import json
from typing import Callable
from ..domain.interfaces import IMessagePublisher, IMessageConsumer
from ..domain.entities import ProcessingResult


class RabbitMQPublisher(IMessagePublisher):
    """پیاده‌سازی ارسال پیام با RabbitMQ"""
    
    def __init__(self, host: str, response_queue: str):
        self.host = host
        self.response_queue = response_queue
        self._setup_connection()
    
    def _setup_connection(self):
        """راه‌اندازی اتصال به RabbitMQ"""
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.host)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.response_queue)
    
    def publish_result(self, result: ProcessingResult) -> None:
        """ارسال نتیجه پردازش"""
        message = json.dumps({
            "filename": result.filename,
            "status": result.status.value,
            "output_path": result.output_path,
            "error_message": result.error_message
        })
        
        self.channel.basic_publish(
            exchange='',
            routing_key=self.response_queue,
            body=message
        )
        
        print(f"📤 نتیجه ارسال شد: {message}")


class RabbitMQConsumer(IMessageConsumer):
    """پیاده‌سازی دریافت پیام با RabbitMQ"""
    
    def __init__(self, host: str, queue_name: str):
        self.host = host
        self.queue_name = queue_name
        self._setup_connection()
    
    def _setup_connection(self):
        """راه‌اندازی اتصال به RabbitMQ"""
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.host)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)
    
    def start_consuming(self, callback: Callable[[str], None]) -> None:
        """شروع گوش دادن به پیام‌ها"""
        def message_handler(ch, method, properties, body):
            image_path = body.decode()
            print(f"📥 پیام دریافت شد: {image_path}")
            callback(image_path)
        
        print(f"🎧 در حال گوش دادن به صف '{self.queue_name}' ...")
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=message_handler,
            auto_ack=True
        )
        
        self.channel.start_consuming()
