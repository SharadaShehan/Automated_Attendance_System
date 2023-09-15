from modules.InitializeSystem import create_directories
from modules.DatabaseQueries import create_database, insert_user_to_database
from modules.ApiCalls import re_register_company_api_call
from modules.ConfigureJsonFile import create_url_json_file, create_json_file, create_runtime_json_file


def re_register_company(registration_key):
    create_url_json_file()
    create_runtime_json_file()
    success, company_name, company_api_code, users_details = re_register_company_api_call(registration_key)
    if success:
        create_directories()
        create_json_file(company_api_code, company_name)
        create_database()
        for user_details in users_details:
            insert_user_to_database(**user_details)
        return True
    return False

re_register_company("fBHybXBYl37ncy5TaYlqiXEE2fsJwsmo")

