from dotenv import load_dotenv
import os, pickle

load_dotenv()
min_minutes_threshold = int(os.getenv('MIN_MINUTES_THRESHOLD'))

def callback_function(users_encodings, db_conn, mqtt_client, ch, method, properties, body):
    """Callback function to process messages from the RabbitMQ queue."""
    try:
        # Decode the message
        message = pickle.loads(body)
        print("Received message:", message)

        # Process the message
        # ...

        # Publish a message to the MQTT broker
        # publish_message(mqtt_client, message)

        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except (Exception) as error:
        print("Error while processing message:", error)
        ch.basic_nack(delivery_tag=method.delivery_tag)
