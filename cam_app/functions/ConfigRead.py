import configparser


def create_config(registration_camera, enter_camera, exit_camera):
    config = configparser.ConfigParser()
    config['CAMERAS'] = {
        'registration_camera': int(registration_camera),
        'enter_camera': int(enter_camera),
        'exit_camera': int(exit_camera)
    }
    config['CAPTURE'] = {
        'frame_width': 200,
        'frame_height': 150
    }
    config['BACKEND'] = {
        'base_url': 'http://127.0.0.1:8000/middleware',
    }
    config['MQTT'] = {
        'broker': 'localhost',
        'port': 1883,
        'topic': 'attendance'
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    return True


def check_config_initialized():
    config = configparser.ConfigParser()
    config.read('config.ini')
    if set(config.sections()) == {'BACKEND', 'CAPTURE', 'CAMERAS', 'MQTT'}:
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
