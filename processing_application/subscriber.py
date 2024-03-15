import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")

def on_message(client, userdata, message):
    print("Received message: " + str(message.payload.decode("utf-8")))

def on_disconnect(client, userdata, rc):
    print("Disconnected, reason: " + str(rc))

# Set your broker address, port, username, and password
broker_address = "35.207.228.39"
port = 1883
username = "user435"
password = "pass4934"

client = mqtt.Client("testClient", protocol=mqtt.MQTTv31)
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# Set username and password before connecting
client.username_pw_set(username, password)

# Connect to the broker
client.connect(broker_address, port, 60)

# Subscribe to topics after connecting
client.subscribe("attendance")

# Start the network loop
client.loop_forever()
