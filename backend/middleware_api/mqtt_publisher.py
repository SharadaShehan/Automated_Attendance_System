import paho.mqtt.publish as publish
from django.conf import settings

class MQTTPublisher:
    def __init__(self):
        self.broker_address = settings.MQTT_BROKER_ADDRESS

    def publish_message(self, topic, message):
        try:
            publish.single(topic, message, hostname=self.broker_address)
            print(f"Message '{message}' published to topic '{topic}'")
        except Exception as e:
            print(f"Error publishing message: {e}")
