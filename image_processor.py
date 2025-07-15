import pika
import boto3
from PIL import Image
import os
import json


RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'image_tasks'

RESPONSE_QUEUE = 'image_responses'

MINIO_ENDPOINT = 'https://mymin.darkube.app'
MINIO_ACCESS_KEY = 'zg5UaX56OxCVaTvPZ3Hn'
MINIO_SECRET_KEY = 'wLJfbqIo8DCnBc23Fv8g2tdVQqDOrLsq4jICzYAS'
MINIO_BUCKET = 'processed'

s3 = boto3.client('s3',
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    region_name='us-east-1'  # می‌تونه هر چیزی باشه اگه Hamravesh بررسی نکنه
)


def process_image(image_path):
    try:
        print(f"🖼 پردازش تصویر: {image_path}")

        img = Image.open(image_path).convert('L')  # grayscale
        output_path = f"processed_{os.path.basename(image_path)}"
        img.save(output_path, optimize=True, quality=60)

        # آپلود به MinIO
        s3.upload_file(output_path, MINIO_BUCKET, output_path)
        print(f"✅ آپلود شد به MinIO: {output_path}")

        send_response(os.path.basename(image_path), "success")

    except Exception as e:
        print(f"❌ خطا در پردازش یا آپلود: {e}")
        send_response(os.path.basename(image_path), "failed")



def send_response(filename, status):
    message = json.dumps({
        "filename": filename,
        "status": status
    })
    channel.basic_publish(
        exchange='',
        routing_key=RESPONSE_QUEUE,
        body=message
    )
    print(f"📤status sent {message}")

def callback(ch, method, properties, body):
    image_path = body.decode()
    print(f"📥message recieved: {image_path}")
    process_image(image_path)

# اتصال به RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
channel = connection.channel()
channel.queue_declare(queue=RESPONSE_QUEUE)
channel.queue_declare(queue=QUEUE_NAME)

print(f"🎧 در حال گوش دادن به صف '{QUEUE_NAME}' ...")
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
