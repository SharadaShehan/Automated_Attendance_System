import environ, psycopg2

env = environ.Env()
environ.Env.read_env()

def connect_to_database():
    """Establishes a secure connection to the PostgreSQL database."""
    try:
        # Read credentials from environment variables
        db_name = env('SQL_DATABASE')
        db_user = env('SQL_USER')
        db_password = env('SQL_PASSWORD')
        db_host = env('SQL_HOST')
        db_port = env('SQL_PORT')

        # Connect using a connection string for enhanced security
        connection_string = f"dbname={db_name} user={db_user} password={db_password} host={db_host} port={db_port}"
        conn = psycopg2.connect(connection_string)
        return conn

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to database:", error)
        return None

def get_users_encodings(db_conn):
    """Retrieves the user encodings from the database."""
    try:
        cursor = db_conn.cursor()
        cursor.execute("SELECT id, encodings FROM users")
        rows = cursor.fetchall()
        return rows

    except (Exception, psycopg2.Error) as error:
        print("Error while retrieving user encodings:", error)
        return None
