import pika, sys, os, environ, psycopg2
from Database import connect_to_database, get_users_encodings

env = environ.Env()
environ.Env.read_env()

min_minutes_threshold = int(env('MIN_MINUTES_THRESHOLD'))

def connect_to_rabbitmq(callback_function):
    """Establishes a connection to the RabbitMQ server."""
    try:
        # Read credentials from environment variables
        rabbitmq_user = env('RABBITMQ_USER')
        rabbitmq_password = env('RABBITMQ_PASSWORD')
        rabbitmq_host = env('RABBITMQ_HOST')
        rabbitmq_port = env('RABBITMQ_PORT')
        rabbitmq_queue = env('RABBITMQ_QUEUE')

        # Create a connection to the RabbitMQ server
        credentials = pika.PlainCredentials(username=rabbitmq_user, password=rabbitmq_password)
        parameters = pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, virtual_host='/', credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.basic_consume(queue=rabbitmq_queue, on_message_callback=callback_function, auto_ack=True)
        return channel

    except (Exception, pika.exceptions.AMQPError) as error:
        print("Error while connecting to RabbitMQ:", error)
        return None




def callback(ch, method, properties, body):
    print(f" [x] Received {body}")


def main():
    db_conn = connect_to_database()
    if db_conn is None:
        print("Exiting...")
        return

    users_encodings = get_users_encodings(db_conn)
    if users_encodings is None:
        print("Exiting...")
        return
    print(users_encodings)
    #
    # channel = connect_to_rabbitmq(callback)
    # if channel is None:
    #     print("Exiting...")
    #     return
    #
    # print(' [*] Waiting for messages. To exit press CTRL+C')
    # channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

