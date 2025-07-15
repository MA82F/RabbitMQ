import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='image_tasks')

message = "test-image.png"
channel.basic_publish(exchange='',
                      routing_key='image_tasks',
                      body=message)

print(f"✅ Sent message: {message}")
connection.close()
