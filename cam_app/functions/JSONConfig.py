import json

config_file_path = "./temp/data.json"


def create():
    data = {
        "middleware_url": "http://127.0.0.1:8000/middleware"
    }
    with open(config_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


def read_url():
    try:
        with open(config_file_path, "r") as file:
            data = json.load(file)
        return data["middleware_url"]
    except FileNotFoundError:
        print(f"File '{config_file_path}' not found.")


def update_company_name(company_name):
    existing_data = {}
    try:
        with open(config_file_path, "r") as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        print(f"File '{config_file_path}' not found.")

    new_data = {
        "company_name": company_name
    }
    existing_data.update(new_data)

    with open(config_file_path, "w") as json_file:
        json.dump(existing_data, json_file, indent=4)

def read_company_name():
    try:
        with open(config_file_path, "r") as file:
            data = json.load(file)
        return data["company_name"]
    except FileNotFoundError:
        return None


def update_init_token(token):
    existing_data = {}
    try:
        with open(config_file_path, "r") as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        print(f"File '{config_file_path}' not found.")

    new_data = {
        "init_token": token
    }
    existing_data.update(new_data)

    with open(config_file_path, "w") as json_file:
        json.dump(existing_data, json_file, indent=4)

def read_init_token():
    try:
        with open(config_file_path, "r") as file:
            data = json.load(file)
        return data["init_token"]
    except FileNotFoundError:
        return None


def update_access_token(token):
    existing_data = {}
    try:
        with open(config_file_path, "r") as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        print(f"File '{config_file_path}' not found.")

    new_data = {
        "access_token": token
    }
    existing_data.update(new_data)

    with open(config_file_path, "w") as json_file:
        json.dump(existing_data, json_file, indent=4)

def read_access_token():
    try:
        with open(config_file_path, "r") as file:
            data = json.load(file)
        return data["access_token"]
    except FileNotFoundError:
        print(f"File '{config_file_path}' not found.")
