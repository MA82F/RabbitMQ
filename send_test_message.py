import pika
import os
from dotenv import load_dotenv

load_dotenv()

# تنظیمات از متغیرهای محیطی
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
QUEUE_NAME = os.getenv("RABBITMQ_QUEUE", "image_tasks")

connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME)

message = "test-image.png"
channel.basic_publish(exchange='',
                      routing_key=QUEUE_NAME,
                      body=message)

print(f"✅ پیام ارسال شد: {message}")
connection.close()
