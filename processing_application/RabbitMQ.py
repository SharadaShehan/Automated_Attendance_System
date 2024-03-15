import pika, os
from dotenv import load_dotenv

load_dotenv()

def connect_to_rabbitmq():
    """Establishes a connection to the RabbitMQ server."""
    try:
        # Read credentials from environment variables
        rabbitmq_user = os.getenv('RABBITMQ_USER')
        rabbitmq_password = os.getenv('RABBITMQ_PASSWORD')
        rabbitmq_host = os.getenv('RABBITMQ_HOST')
        rabbitmq_port = os.getenv('RABBITMQ_PORT')

        # Create a connection to the RabbitMQ server
        credentials = pika.PlainCredentials(username=rabbitmq_user, password=rabbitmq_password)
        parameters = pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, virtual_host='/', credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        return channel

    except (Exception, pika.exceptions.AMQPError) as error:
        print("Error while connecting to RabbitMQ:", error)
        return None


def process_messages(channel, callback_function):
    """Starts consuming messages from the RabbitMQ server."""
    try:
        rabbitmq_queue = os.getenv('RABBITMQ_QUEUE')
        channel.basic_consume(queue=rabbitmq_queue, on_message_callback=callback_function, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    except (Exception, pika.exceptions.AMQPError) as error:
        print("Error while processing messages:", error)
        return None

