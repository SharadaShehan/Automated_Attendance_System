<h1 align="center">Automated Attendance System - Development</h1>


## Cam Stream Application


* Run Application in a virtual environment.

1) Navigate to the cam app repository.

    ```
    cd Automated_Attendance_System/cam_application
    ```

2) Then run following commands to create and activate a python environment.

    ```
    py -m venv venv
    ```
    ```
    venv\Scripts\Activate
    ```

    If your Python virtual environment works fine, then in the command line should be something similar to this.
    
    ```
    (venv) C:\...\Automated_Attendance_System\backend>
    ```

3) Now, in order to install the required python libraries run this command.

    ```
    pip install -r requirements.txt
    ```

4) Create `.env` file in `/cam_application/` home directory with following variables in it.

    ```
    FRAME_WIDTH=200
    FRAME_HEIGHT=150
    BACKEND_BASE_URL=http://backend-vm-public-ip/middleware
    MQTT_USER=mqtt-username
    MQTT_PASSWORD=mqtt-password
    MQTT_HOST=mqtt-broker-vm-public-ip
    MQTT_PORT=1883
    MQTT_TOPIC=attendance
    MQTT_AUTH_TOKEN=auth-token
    ```
    `FRAME_WIDTH`, `FRAME_HEIGHT` environment variables define the size of frames you are expecting to send to backend for processing.
    
    Replace `BACKEND_BASE_URL` environment variable value with the base url of the backend server.
    Replace `MQTT_USER`, `MQTT_PASSWORD`, `MQTT_HOST`, `MQTT_PORT`, `MQTT_TOPIC` environment variables values with relevant credentials for your mosquitto broker.
    
    Replace `MQTT_AUTH_TOKEN` environment variable value with a token string that can be used to verify messages are published by processing application.
    
5) In home directory, Run following command to start the Cam Stream App.
    
    ```
    python main.py
    ```

## Backend

* Windows OS - Development Environment Setup

1) Navigate to the backend repository.

    ```
    cd Automated_Attendance_System/backend
    ```

2) Then run following commands to create and activate a python environment.

    ```
    py -m venv venv
    ```
    ```
    venv\Scripts\Activate
    ```

    If your Python virtual environment works fine, then in the command line should be something similar to this.
    
    ```
    (venv) C:\...\Automated_Attendance_System\backend>
    ```

3) Installing the required python libraries.

    Open backend project in PyCharm IDE. Configure IDE to use python interpreter which is in the created virtual environment. Then, open `requirements.txt` file in IDE and IDE will recommend to install libraries listed in file. Allow it to install them.

4) Run below commands to install `dlib` and `face_recognition` libraries. Replace `ROOT_PATH` text with actual path of parent directory of Automated_Attendance_System folder.

    ```
    pip install "ROOT_PATH/Automated_Attendance_System/backend/dlib-19.22.99-cp310-cp310-win_amd64.whl"
    ```
    ```
    pip install face_recognition
    ```

5) Create `.env` file in `/backend/backend/` location with following variables in it.

    ```
    DEBUG=1
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
    ```
    Replace `SQL_DATABASE`, `SQL_USER`, `SQL_HOST`,`SQL_PASSWORD`, `SQL_PORT` environment variables values with relevant credentials for your PostgreSQL database and  `RABBITMQ_USER`, `RABBITMQ_PASSWORD`, `RABBITMQ_HOST`, `RABBITMQ_PORT` environment variables values with relevant credentials for your RabbitMQ server.

6) In command line, move to location `Automated_Attendance_System/backend/` and Apply Model migrations to PostgreSQL database using following commands.

    ```
    python manage.py makemigrations
    ```
    ```
    python manage.py migrate
    ```

7) Run this command to run the Local Server.

    ```
    python manage.py runserver
    ```


* Linux OS - Production Environment Setup

  First, enable SQL server to communicate with 0.0.0.0/0 IP addresses. Then, follow below steps to deploy the backend application.

1) Navigate to the backend repository.

    ```
    cd Automated_Attendance_System/backend
    ```

2) Edit environment variables in `deploy.sh` file.

3) Run the following commands to deploy the backend application along with nginx server. Replace `ip_address_of_backend_vm` with the public IP address of the VM.

    ```
    sudo chmod +x run_nginx_server.sh
    sudo chmod +x deploy.sh
    sudo ./run_nginx_server.sh ip_address_of_backend_vm
    sudo ./deploy.sh
    ```

    Finally, enable SQL server to communicate only with necessary IP addresses (backend server and prcessing application server IP addresses).

## Processing Application

* Windows OS - Development Environment Setup

1) Navigate to the processing_application repository.

    ```
    cd Automated_Attendance_System/processing_application
    ```

2) Then run following commands to create and activate a python environment.

    ```
    py -m venv venv
    ```
    ```
    venv\Scripts\Activate
    ```

    If your Python virtual environment works fine, then in the command line should be something similar to this.
    
    ```
    (venv) C:\...\Automated_Attendance_System\processing_application>
    ```

3) Installing the required python libraries.

    Open backend project in PyCharm IDE. Configure IDE to use python interpreter which is in the created virtual environment. Then, open `requirements.txt` file in IDE and IDE will recommend to install libraries listed in file. Allow it to install them.

4) Run below commands to install `dlib` and `face_recognition` libraries. Replace `ROOT_PATH` text with actual path of parent directory of Automated_Attendance_System folder.

    ```
    pip install "ROOT_PATH/Automated_Attendance_System/processing_application/dlib-19.22.99-cp310-cp310-win_amd64.whl"
    ```
    ```
    pip install face_recognition
    ```

5) Create `.env` file with following variables in it.

    ```
    DEBUG=1
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
    ```
    Replace `SQL_DATABASE`, `SQL_USER`, `SQL_HOST`,`SQL_PASSWORD`, `SQL_PORT` environment variables values with relevant credentials for your PostgreSQL database and  `RABBITMQ_USER`, `RABBITMQ_PASSWORD`, `RABBITMQ_HOST`, `RABBITMQ_PORT` environment variables values with relevant credentials for your RabbitMQ server.
    
    Replace `MQTT_USER`, `MQTT_PASSWORD`, `MQTT_HOST`, `MQTT_PORT` environment variables values with relevant credentials for your mosquitto broker.
    Replace `MQTT_AUTH_TOKEN` environment variable value with same token string that is used in cam application.

    Replace `GCP_PROJECT_ID`, `GCE_INSTANCE_ID`, `GCP_ZONE` environment variables values with relevant credentials for your Google Cloud Platform project id, vm instance,
    zone. Create a service account key in GCP and download it as a json file. Rename it as `serviceAccountKey.json` and place it in the processing_application home directory.

6) Run this command to run the Processing Application.

    ```
    python main.py
    ```

* Linux OS - Production Environment Setup

  First, enable SQL server to communicate with 0.0.0.0/0 IP addresses. Then, follow below steps to deploy the processing application

1) Navigate to the processing_application repository.

    ```
    cd Automated_Attendance_System/processing_application
    ```

2) Edit environment variables in `deploy.sh` file. Create a service account key in GCP and download it as a json file. Rename it as `serviceAccountKey.json` and place it in the processing_application home directory (upload it to the VM and move it to processing_application home directory).

3) Run the following commands to deploy the processing application.

    ```
    sudo chmod +x deploy.sh
    sudo ./deploy.sh
    ```

    Finally, enable SQL server to communicate only with necessary IP addresses (backend server and prcessing application server IP addresses).

## AMQP Broker

* Linux OS - Production Environment Setup

1) Run below commands to install and run RabbitMQ broker in a VM. Replace `username` and `password` with your desired username and password. Replace `distribution_name` with the name of the Linux distribution you are using.

    ```
    sudo apt-get update
    sudo apt install git -y
    git clone https://github.com/SharadaShehan/Automated_Attendance_System.git
    cd Automated_Attendance_System
    sudo chmod +x run_rabbitmq_broker.sh
    sudo ./run_rabbitmq_broker.sh distribution_name username password
    ```
2) Run below command to create a queue named `attendance_queue` in RabbitMQ broker. Replace `username` and `password` with credentials you used to create the RabbitMQ broker.

    ```
    curl -X PUT http://localhost:15672/api/queues/%2F/attendance_queue -u username:password -H 'Content-Type: application/json' -d '{"durable": true}'
    ```

## MQTT Broker

* Linux OS - Production Environment Setup

1) Run below commands to install and run Mosquitto MQTT broker in a VM. Replace `username` and `password` with your desired username and password.

    ```
    sudo apt-get update
    sudo apt install git -y
    git clone https://github.com/SharadaShehan/Automated_Attendance_System.git
    cd Automated_Attendance_System
    sudo chmod +x run_mosquitto_broker.sh
    sudo ./run_mosquitto_broker.sh username password
    ```

