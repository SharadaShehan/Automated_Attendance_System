<h1 align="center">⚡Automated Attendance System⚡</h1>

<h2 align="center">🏢System Architecture🛠️</h2>


![sysArchi](resources/Attendsense_System_Architecture.jpg)

# Developer Guide

* First, clone the repository. 
    
    ```bash
    git clone https://github.com/SharadaShehan/Automated_Attendance_System.git
    ```

## Backend
Recommendations : <br>
Python version : `Python 3.10.9`  <br>
IDE : `PyCharm`

Note : Develop the backend in a virtual environment.

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
    pip install "path_to_parent_directory/Automated_Attendance_System/backend/dlib-19.22.99-cp310-cp310-win_amd64.whl"

    pip install face_recognition
    ```

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
    ```
    Replace `SQL_DATABASE`, `SQL_USER`, `SQL_PASSWORD`, `SQL_PORT`  environment variables values with relevant credentials for your local PostgreSQL database.

6) Apply Model migrations to PostgreSQL database.

    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

7) Run this command to run the Local Server.

    ```
    python manage.py runserver
    ```



