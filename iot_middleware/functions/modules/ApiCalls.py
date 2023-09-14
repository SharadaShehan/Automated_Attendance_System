import requests
from .ConfigureJsonFile import read_url_json_file, read_json_file


def register_company_api_call(input_company_name, foreground_color, background_color, deep_color, email, password, first_name, last_name, encodings, register_code):
    middleware_url = read_url_json_file()['middleware_url']
    transmittable_encodings = encodings.tolist()
    json_dict = {
        "name": input_company_name,
        "style_guide": {
            "foreground_color" : foreground_color,
            "background_color" : background_color,
            "deep_color" : deep_color
        },
        "default_executive_account": {
            "email" : email,
            "password" : password,
            "first_name" : first_name,
            "last_name" : last_name,
            "encodings": transmittable_encodings
        },
        "register_code": register_code
    }

    resp = requests.post(middleware_url + "/create/company", json=json_dict)
    if resp.status_code == 201:
        resp_data = resp.json()
        company_name = resp_data['name']
        company_api_code = resp_data['company_api_code']

        backend_id = resp_data['default_executive_id']
        user_api_code = resp_data['default_executive_api_code']
        user_details = (backend_id, first_name, last_name, user_api_code, encodings)
        company_details = (company_api_code, company_name)
        return True, company_details, user_details
    return False, None, None

def re_register_company_api_call(registration_key):
    middleware_url = read_url_json_file()['middleware_url']
    resp = requests.get(middleware_url+f'/retriew-company-details/{registration_key}')
    if resp.status_code == 200:
        resp_data = resp.json()
        company_name = resp_data['company_name']
        company_api_code = resp_data['company_api_code']
        users_details = resp_data['users_details']
        return True, company_name, company_api_code, users_details
    return False, None, None, None


def register_user_api_call(email, password, first_name, last_name, encodings):
    middleware_url = read_url_json_file()['middleware_url']
    company_api_code = read_json_file()['company_api_code']
    transmittable_encodings = encodings.tolist()
    json_dict = {
        "email" : email,
        "password" : password,
        "first_name" : first_name,
        "last_name" : last_name,
        "encodings" : transmittable_encodings,
        "company_api_code" : company_api_code
    }
    resp = requests.post(middleware_url + "/create/user", json=json_dict)
    if resp.status_code == 201:
        resp_data = resp.json()
        backend_id = resp_data['id']
        user_api_code = resp_data['user_api_code']
        user_details = (backend_id, first_name, last_name, user_api_code, encodings)
        return True, user_details
    return False, None



def record_entrance_api_call(backend_id, user_api_code, date, time):
    middleware_url = read_url_json_file()['middleware_url']
    json_dict = {
        "user_api_code": user_api_code,
        "date": date,
        "time": time
    }
    resp = requests.patch(middleware_url + "/update/user-attendance/entrance/" + str(backend_id), json=json_dict)
    if resp.status_code == 200:
        return True
    return False



def record_leave_api_call(backend_id, user_api_code, date, time):
    middleware_url = read_url_json_file()['middleware_url']
    json_dict = {
        "user_api_code": user_api_code,
        "date": date,
        "time": time
    }
    resp = requests.patch(middleware_url + "/update/user-attendance/leave/" + str(backend_id), json=json_dict)
    if resp.status_code == 200:
        return True
    return False


def check_registration_validity():
    middleware_url = read_url_json_file()['middleware_url']
    company_api_code = read_json_file()['company_api_code']
    resp = requests.get(middleware_url + f"/check-validity/{company_api_code}")
    if resp.status_code == 200:
        if resp.json()['is_valid']:
            return True
    return False

