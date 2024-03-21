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

# Create .env file in inner backend directory with environment variables
environment_variables_file="backend/.env"
cat << EOF > "$environment_variables_file"
DEBUG=0
DJANGO_ALLOWED_HOSTS=localhost
SECRET_KEY=django-secret-key
SQL_ENGINE=django.db.backends.postgresql
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
EOF

# apply migrations and start the server
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver &
