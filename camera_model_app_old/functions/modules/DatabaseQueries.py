import sqlite3
import pickle
database_path = '../storage/database.db'


def create_database():
    conn = sqlite3.connect(database_path)

    cursor1 = conn.cursor()
    drop_user_table_query = '''
    DROP TABLE IF EXISTS users
    '''
    cursor1.execute(drop_user_table_query)
    conn.commit()

    cursor2 = conn.cursor()
    create_user_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            backend_id INTEGER,
            first_name TEXT,
            last_name TEXT,
            user_api_code INTEGER,
            encodings BLOB
        )
    '''
    cursor2.execute(create_user_table_query)
    conn.commit()

    cursor3 = conn.cursor()
    drop_attendance_table_query = '''
        DROP TABLE IF EXISTS attendance
        '''
    cursor3.execute(drop_attendance_table_query)
    conn.commit()

    cursor4 = conn.cursor()
    create_attendance_table_query = '''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY,
            backend_id INTEGER,
            user_api_code INTEGER,
            date TEXT,
            time TEXT,
            entrance INTEGER
        )
    '''
    # entrance is a boolean value ( 0 or 1 )
    cursor4.execute(create_attendance_table_query)
    conn.commit()

    conn.close()



def insert_user_to_database(backend_id, first_name, last_name, user_api_code, encodings):
    bytes_encodings = pickle.dumps(encodings)
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    insert_query = '''
        INSERT INTO users (backend_id, first_name, last_name, user_api_code, encodings)
        VALUES (?, ?, ?, ?, ?)
    '''

    cursor.execute(insert_query, (backend_id, first_name, last_name, user_api_code, bytes_encodings))
    conn.commit()
    conn.close()


def get_users_encodings_from_database():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    return_encodings_query = '''
        SELECT backend_id, user_api_code, encodings
        FROM users
    '''

    cursor.execute(return_encodings_query)
    rows = cursor.fetchall()

    users = []
    for row in rows:
        backend_id, user_api_code, bytes_encodings = row
        encodings = pickle.loads(bytes_encodings)
        users.append({
            'backend_id': backend_id,
            'user_api_code': user_api_code,
            'encodings': encodings
        })

    conn.close()
    return users




def insert_attendance_record_to_database(backend_id, user_api_code, date, time, entrance):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    insert_query = '''
        INSERT INTO attendance (backend_id, user_api_code, date, time, entrance)
        VALUES (?, ?, ?, ?, ?)
    '''

    cursor.execute(insert_query, (backend_id, user_api_code, date, time, entrance))
    conn.commit()
    conn.close()



def get_attendance_record_from_database(record_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    select_query = '''
        SELECT backend_id, user_api_code, date, time, entrance
        FROM attendance
        WHERE id = ?
    '''

    cursor.execute(select_query, (record_id,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        return None

    backend_id, user_api_code, date, time, entrance = row
    attendance_record = {
        'backend_id': backend_id,
        'user_api_code': user_api_code,
        'date': date,
        'time': time,
        'entrance': entrance
    }

    conn.close()
    return attendance_record


def is_attendance_table_empty():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    select_query = '''
        SELECT COUNT(*) FROM attendance
    '''
    cursor.execute(select_query)
    row = cursor.fetchone()

    conn.close()

    if row is not None and row[0] == 0:
        return True
    return False


def delete_attendance_record_from_database(record_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    delete_query = '''
        DELETE FROM attendance
        WHERE id = ?
    '''

    cursor.execute(delete_query, (record_id,))
    conn.commit()
    conn.close()



