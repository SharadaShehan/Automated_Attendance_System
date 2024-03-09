#!/bin/bash

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
cd backend
echo "DEBUG=1
SECRET_KEY='secret-key-of-django-app'
HUB_SECRET_KEY=secret-key-of-hub-app
DJANGO_ALLOWED_HOSTS=localhost
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=database-name
SQL_USER=database-user
SQL_PASSWORD=database-password
SQL_HOST=database-host
SQL_PORT=database-database-port
MIN_MINUTES_THRESHOLD=5" > .env

# Navigate back to the root directory and apply migrations
cd ..
python manage.py makemigrations
python manage.py migrate

# Start the development server in the background
python manage.py runserver &
