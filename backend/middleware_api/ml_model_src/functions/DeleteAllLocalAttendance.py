from modules.DatabaseQueries import delete_attendance_record_from_database, is_attendance_table_empty
from modules.ConfigureJsonFile import read_runtime_json_file, update_record_id_to_runtime_json_file, update_last_deleted_record_id_to_runtime_json_file


def delete_all_local_attendance():
    record_id = read_runtime_json_file()['record_id']
    last_deleted_record_id = read_runtime_json_file()['last_deleted_record_id']

    while True:
        if not record_id:
            return
        last_deleted_record_id += 1
        print(last_deleted_record_id)
        if last_deleted_record_id > record_id:
            if is_attendance_table_empty():
                update_record_id_to_runtime_json_file(0)
                update_last_deleted_record_id_to_runtime_json_file(0)
            else:
                update_last_deleted_record_id_to_runtime_json_file(last_deleted_record_id-1)
            return
        delete_attendance_record_from_database(last_deleted_record_id)


# delete_all_local_attendance()
