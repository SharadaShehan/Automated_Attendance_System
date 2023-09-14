import json
company_file_path = "data.json"
url_file_path = "modules/url.json"
runtime_file_path = "modules/runtime.json"

# 20.197.0.180

def create_url_json_file():
    data = {
        "middleware_url": "http://127.0.0.1:8000/middleware"
    }
    with open(url_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


def read_url_json_file():
    try:
        with open(url_file_path, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File '{url_file_path}' not found.")


def create_runtime_json_file():
    data = {
        "record_id": 0,
        "last_deleted_record_id": 0
    }
    with open(runtime_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


def read_runtime_json_file():
    try:
        with open(runtime_file_path, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File '{runtime_file_path}' not found.")


def update_record_id_to_runtime_json_file(record_id):
    existing_data = {}
    try:
        with open(runtime_file_path, "r") as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        print(f"File '{runtime_file_path}' not found.")

    new_data = {
        "record_id": record_id
    }
    existing_data.update(new_data)

    with open(runtime_file_path, "w") as json_file:
        json.dump(existing_data, json_file, indent=4)


def update_last_deleted_record_id_to_runtime_json_file(last_deleted_record_id):
    existing_data = {}
    try:
        with open(runtime_file_path, "r") as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        print(f"File '{runtime_file_path}' not found.")

    new_data = {
        "last_deleted_record_id": last_deleted_record_id
    }
    existing_data.update(new_data)

    with open(runtime_file_path, "w") as json_file:
        json.dump(existing_data, json_file, indent=4)



def create_json_file(company_api_code, company_name):
    data = {
        "company_api_code": company_api_code,
        "company_name": company_name
    }
    with open(company_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


def read_json_file():
    try:
        with open(company_file_path, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File '{company_file_path}' not found.")


def update_company_api_code_to_json_file(company_api_code):
    existing_data = {}
    try:
        with open(company_file_path, "r") as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        print(f"File '{company_file_path}' not found.")

    new_data = {
        "company_api_code": company_api_code
    }
    existing_data.update(new_data)

    with open(company_file_path, "w") as json_file:
        json.dump(existing_data, json_file, indent=4)


def update_company_name_to_json_file(company_name):
    existing_data = {}
    try:
        with open(company_file_path, "r") as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        print(f"File '{company_file_path}' not found.")

    new_data = {
        "company_name": company_name
    }
    existing_data.update(new_data)

    with open(company_file_path, "w") as json_file:
        json.dump(existing_data, json_file, indent=4)

