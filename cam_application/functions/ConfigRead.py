import configparser
import os, re
from dotenv import load_dotenv

def create_config(registration_camera, enter_camera, exit_camera):
    load_dotenv()
    config = configparser.ConfigParser()
    config['CAMERAS'] = {
        'registration_camera': int(registration_camera),
        'enter_camera': int(enter_camera),
        'exit_camera': int(exit_camera)
    }
    config['CAPTURE'] = {
        'frame_width': int(os.getenv('FRAME_WIDTH')),
        'frame_height': int(os.getenv('FRAME_HEIGHT'))
    }
    config['BACKEND'] = {
        'base_url': os.getenv('BACKEND_BASE_URL')
    }
    config['MQTT'] = {
        'broker': os.getenv('MQTT_BROKER_URL'),
        'port': int(os.getenv('MQTT_BROKER_PORT')),
        'topic': os.getenv('MQTT_TOPIC')
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    return True


def check_config_initialized():
    config = configparser.ConfigParser()
    config.read('config.ini')
    if set(config.sections()) == {'BACKEND', 'CAPTURE', 'CAMERAS', 'MQTT'} or set(config.sections()) == {'BACKEND', 'CAPTURE', 'CAMERAS', 'MQTT', 'COMPANY'}:
        if set(config['BACKEND'].keys()) == {'base_url'} and config['BACKEND']['base_url'] and \
           set(config['CAPTURE'].keys()) == {'frame_width', 'frame_height'} and config['CAPTURE']['frame_width'] and config['CAPTURE']['frame_height'] and \
           set(config['CAMERAS'].keys()) == {'registration_camera', 'enter_camera', 'exit_camera'} and config['CAMERAS']['registration_camera'] and config['CAMERAS']['enter_camera'] and config['CAMERAS']['exit_camera'] and \
           set(config['MQTT'].keys()) == {'broker', 'port', 'topic'} and config['MQTT']['broker'] and config['MQTT']['port'] and config['MQTT']['topic']:
            return True
    return False


def update_company_name(company_name):
    existing_data = {}
    try:
        with open('config.ini', "r") as configfile:
            existing_data = configfile.read()
    except FileNotFoundError:
        print(f"File 'config.ini' not found.")
        return False

    new_data = f"[COMPANY]\ncompany_name = {company_name}\n"
    existing_data = existing_data + new_data

    with open('config.ini', "w") as configfile:
        configfile.write(existing_data)

    return True


def update_camera_config(registration_camera, enter_camera, exit_camera):
    existing_data = {}
    try:
        with open('config.ini', "r") as configfile:
            existing_data = configfile.read()
    except FileNotFoundError:
        print(f"File 'config.ini' not found.")
        return False

    # Define the pattern to match the camera configuration lines
    pattern = r"\[CAMERAS\].*?registration_camera = .*?\n.*?enter_camera = .*?\n.*?exit_camera = .*?\n"

    # Create the new camera configuration data
    new_data = f"[CAMERAS]\nregistration_camera = {registration_camera}\nenter_camera = {enter_camera}\nexit_camera = {exit_camera}\n"

    # Replace the existing camera configuration data with the new data
    updated_data = re.sub(pattern, new_data, existing_data, flags=re.DOTALL)

    with open('config.ini', "w") as configfile:
        configfile.write(updated_data)

    return True


def check_company_initialized():
    config = configparser.ConfigParser()
    config.read('config.ini')
    if set(config.sections()) == {'BACKEND', 'CAPTURE', 'CAMERAS', 'MQTT', 'COMPANY'}:
        if set(config['BACKEND'].keys()) == {'base_url'} and config['BACKEND']['base_url'] and \
           set(config['CAPTURE'].keys()) == {'frame_width', 'frame_height'} and config['CAPTURE']['frame_width'] and config['CAPTURE']['frame_height'] and \
           set(config['CAMERAS'].keys()) == {'registration_camera', 'enter_camera', 'exit_camera'} and config['CAMERAS']['registration_camera'] and config['CAMERAS']['enter_camera'] and config['CAMERAS']['exit_camera'] and \
           set(config['MQTT'].keys()) == {'broker', 'port', 'topic'} and config['MQTT']['broker'] and config['MQTT']['port'] and config['MQTT']['topic'] and \
           set(config['COMPANY'].keys()) == {'company_name'} and config['COMPANY']['company_name']:
            return True
    return False


def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config
