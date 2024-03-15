import paho.mqtt.client as mqtt

# Set your broker address, port, username, and password
broker_address = "35.207.228.39"
port = 1883
username = "user435"
password = "pass4934"

client = mqtt.Client("testClient1", protocol=mqtt.MQTTv31)

# Set username and password before connecting
client.username_pw_set(username, password)

# Connect to the broker
client.connect(broker_address, port, 60)

# Function to publish a message
def publish_message(topic, message):
    client.publish(topic, message)

# Example usage: Publish a message to the "test" topic
publish_message("test", "Hello from the publisher!")

print("Published message to 'test' topic")
