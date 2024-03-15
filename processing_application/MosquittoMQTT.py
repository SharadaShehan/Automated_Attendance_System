import os, datetime, pickle
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from Database import get_user_data

load_dotenv()

def connect_to_mqtt():
    """Establishes a connection to the MQTT broker."""
    try:
        # Read credentials from environment variables
        mqtt_user = os.getenv('MQTT_USER')
        mqtt_password = os.getenv('MQTT_PASSWORD')
        mqtt_host = os.getenv('MQTT_HOST')
        mqtt_port = os.getenv('MQTT_PORT')

        # Create a connection to the MQTT broker
        client = mqtt.Client("mqttClient", protocol=mqtt.MQTTv31)
        client.username_pw_set(mqtt_user, mqtt_password)
        client.connect(mqtt_host, int(mqtt_port), 60)
        return client

    except (Exception, mqtt.error) as error:
        print("Error while connecting to MQTT:", error)
        return None

def publish_event(client, message):
    """Publishes a message to the MQTT broker."""
    try:
        mqtt_topic = os.getenv('MQTT_TOPIC')
        client.publish(mqtt_topic, message)
        print("Message published successfully")
        return True

    except (Exception, mqtt.error) as error:
        print("Error while publishing message:", error)
        return None

def attendance_updated_event(client, db_conn, user_id, entrance):
    """Publishes an attendance update event to the MQTT broker."""
    user_data = get_user_data(user_id, db_conn)
    message = {
        "first_name": user_data[2],
        "last_name": user_data[3],
        "gender": user_data[4],
        "entrance": int(entrance),
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    success = publish_event(client, pickle.dumps(message))
    return success
