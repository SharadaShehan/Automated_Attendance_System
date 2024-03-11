import pika

USERNAME = "user435"
PASSWORD = "pass4934"
HOST = "10.0.0.3"
QUEUE = "attendance_queue"

# Replace with your RabbitMQ server details and consumer credentials
credentials = pika.PlainCredentials(username=USERNAME, password=PASSWORD)
parameters = pika.ConnectionParameters(host=HOST, port=5672, virtual_host='/', credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# channel.queue_declare(queue=QUEUE)

channel.basic_publish(exchange='', routing_key=QUEUE, body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()
