#!/bin/bash

# Check root privileges and exit if not root
if [ "$(whoami)" != "root" ]; then
  echo "This script requires root privileges. Please run with sudo."
  exit 1
fi

# Install dependencies, create and activate python virtual environment
sudo apt install python3.11-venv -y
python3 -m venv venv
source venv/bin/activate

# Upgrade pip and install python libraries
pip install --upgrade pip
pip install -r requirements.txt

# Install additional system dependencies
sudo apt install python3.11-dev* -y
sudo apt install g++ cmake -y

# Install face_recognition library
pip3 install face_recognition

# Create .env file with environment variables
cat << EOF > ".env"
DEBUG=0
MIN_MINUTES_THRESHOLD=2
SQL_DATABASE=databaseName
SQL_USER=dbusername
SQL_PASSWORD=dbPassword
SQL_HOST=publicIPOfDatabase
SQL_PORT=5432
RABBITMQ_USER=rabbitmqUser
RABBITMQ_PASSWORD=rabbitmqPassword
RABBITMQ_HOST=privateIPOfRabbitMQ
RABBITMQ_PORT=5672
RABBITMQ_QUEUE=attendance_queue
MQTT_USER=mqttuser
MQTT_PASSWORD=mqttpassword
MQTT_HOST=privateIPOfMQTTBroker
MQTT_PORT=1883
MQTT_TOPIC=attendance
MQTT_AUTH_TOKEN=authToken
GCP_PROJECT_ID=project-id
GCE_INSTANCE_ID=instance-id
GCP_ZONE=zone
GOOGLE_APPLICATION_CREDENTIALS=serviceAccountKey.json
EOF

# Start Application in background
python main.py &
