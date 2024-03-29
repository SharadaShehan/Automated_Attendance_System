import psycopg2, os, json, numpy as np
from dotenv import load_dotenv
import json

load_dotenv()

def connect_to_database():
    """Establishes a secure connection to the PostgreSQL database."""
    try:
        # Read credentials from environment variables
        db_name = os.getenv('SQL_DATABASE')
        db_user = os.getenv('SQL_USER')
        db_password = os.getenv('SQL_PASSWORD')
        db_host = os.getenv('SQL_HOST')
        db_port = os.getenv('SQL_PORT')

        # Connect using a connection string for enhanced security
        connection_string = f"dbname={db_name} user={db_user} password={db_password} host={db_host} port={db_port}"
        conn = psycopg2.connect(connection_string)
        return conn

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to database:", error)
        return None

def get_users_data(db_conn):
    """Retrieves the user encodings from the database."""
    try:
        cursor = db_conn.cursor()
        cursor.execute("SELECT id, encodings FROM database_customuser")
        rows = cursor.fetchall()
        users_data = [
            { "id": row[0], "encodings": np.array(json.loads(row[1])) }
            for row in rows
        ]
        return users_data

    except (Exception, psycopg2.Error) as error:
        print("Error while retrieving user encodings:", error)
        return None

def get_user_data(user_id, db_conn):
    """Retrieves the user data from the database."""
    try:
        cursor = db_conn.cursor()
        cursor.execute(
            f"SELECT id, attendance, first_name, last_name, gender FROM database_customuser WHERE id={user_id}")
        user_data = cursor.fetchone()
        return user_data
    except (Exception, psycopg2.Error) as error:
        print("Error while retrieving user data:", error)
        return None

def update_user_attendance(user_id, attendance, db_conn):
    """Updates the user attendance in the database."""
    try:
        cursor = db_conn.cursor()
        cursor.execute(
            f"UPDATE database_customuser SET attendance='{attendance}' WHERE id={user_id}")
        db_conn.commit()
        return True
    except (Exception, psycopg2.Error) as error:
        print("Error while updating user attendance:", error)
        return False