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
DEBUG=1
SECRET_KEY='django-insecure-7=4n(di4tfh13+__prvqy7jz3gf*=i2k+g-zbh$473axf^h60!'
DJANGO_ALLOWED_HOSTS=localhost
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=attendsensedb
SQL_USER=postgres
SQL_PASSWORD=attendsensePassword
SQL_HOST=34.93.209.162
SQL_PORT=5432
RABBITMQ_USER=user435
RABBITMQ_PASSWORD=pass4934
RABBITMQ_HOST=10.0.0.3
RABBITMQ_PORT=5672
RABBITMQ_QUEUE=attendance_queue
EOF

# apply migrations and start the server
python manage.py makemigrations
python manage.py migrate
python manage.py runserver &
