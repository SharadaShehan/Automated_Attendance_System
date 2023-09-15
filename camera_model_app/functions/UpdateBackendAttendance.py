from modules.ApiCalls import record_entrance_api_call, record_leave_api_call
from modules.DatabaseQueries import get_attendance_record_from_database, delete_attendance_record_from_database
from modules.ConfigureJsonFile import read_runtime_json_file, update_record_id_to_runtime_json_file


def update_backend_attendance():
    record_id = read_runtime_json_file()['record_id']

    while True:
        record_id += 1
        attendance_record = get_attendance_record_from_database(record_id)
        if not attendance_record:
            record_id -= 1
            break
        record_details = [attendance_record['backend_id'], attendance_record['user_api_code'], attendance_record['date'], attendance_record['time']]
        try:
            if attendance_record['entrance']:
                success = record_entrance_api_call(*record_details)
            else:
                success = record_leave_api_call(*record_details)
            print(success)
            if success:
                update_record_id_to_runtime_json_file(record_id)
            else:
                raise Exception
        except:
            record_id -= 1

# update_backend_attendance()






