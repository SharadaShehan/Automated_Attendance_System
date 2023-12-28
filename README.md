<h1 align="center">⚡Automated Attendance System⚡</h1>

<h2 align="center">🏢System Architecture🛠️</h2>


![sysArchi](resources/Attendsense_System_Architecture.jpg)

# Developer Guide

* First, clone the repository. 
    
    ```
    git clone https://github.com/SharadaShehan/Automated_Attendance_System.git
    ```

### Requirements

* Following applications must be installed and running on your local machine, before starting project.

    ```
    PostgreSQL database server
    Mosquitto MQTT Broker
    ```

## Backend

* Python version 3.10.9 is recommended.
* Run Backend in a virtual environment.

<br>

1) Navigate to the backend repository.

    ```
    cd Automated_Attendance_System/backend
    ```

2) Then run this command to activate a python environment. After that activate the environment.

    ```
    python -m venv "venv"
    venv\bin\activate
    ```
    If you are using a different version of python, you may have to type `venv\Scripts\Activate` to activate the created virtual environment.

    If your Python virtual environment works fine, then in the command line should be something similar to this.
    
    ```
    (venv) C:\...\Airline_Reservation_System\backend>
    ```

3) Now you have to install the required python libraries. Then run this command.

    ```
    pip install -r requirements.txt
    ```

4) Run below commands to install `dlib` and `face_recognition` libraries.

    ```
    pip install "ROOT_PATH/Automated_Attendance_System/backend/dlib-19.22.99-cp310-cp310-win_amd64.whl"

    pip install face_recognition
    ```
    Replace `ROOT_PATH` text with actual path of parent directory of Automated_Attendance_System folder.

5) create `.env` file in `/backend/backend/` location with following variables in it.

    ```
    DEBUG=1
    SECRET_KEY=your_secret_key
    DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
    SQL_ENGINE=django.db.backends.postgresql
    SQL_DATABASE=database_name
    SQL_USER=database_user
    SQL_PASSWORD=database_password
    SQL_HOST=localhost
    SQL_PORT=5432
    MQTT_BROKER=localhost
    MQTT_PORT=1883
    MQTT_TOPIC=attendance
    MIN_MINUTES_THRESHOLD=10
    ```
    Replace `SQL_DATABASE`, `SQL_USER`, `SQL_PASSWORD`, `SQL_PORT` environment variables values with relevant credentials for your local PostgreSQL database and `MQTT_BROKER`, `MQTT_PORT`, `MQTT_TOPIC` environment variables values with relevant credentials for your local mosquitto broker.
    `MIN_MINUTES_THRESHOLD` is the minimum duration between two detections from same user to consider second detection as an attendance.

6) In terminal move to location `Automated_Attendance_System/backend/` and Apply Model migrations to PostgreSQL database using following commands.

    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

7) Run this command to run the Local Server.

    ```
    python manage.py runserver
    ```

Node : Following steps must be taken, only when developing frontend application. As data defined in scripts, do not contain sensitive user encodings, this sample database will not support cam stream app.

8) Now you can populate your local database with set of data defined in scripts, by making an API call to below endpoint.

    ```
    http://127.0.0.1:8000/scripts/init
    ```

9) Then, If you want to reset your database with data defined in scripts, run below commands and then make an API call to above API.

    ```
    python manage.py migrate database zero
    python manage.py migrate
    ```

## Cam Stream App

