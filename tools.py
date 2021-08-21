import json
from os import readlink 


default_config = {
    'start_pos_x' : 10,
    'start_pos_y' : 10,
    'default_size':35,
    'zoom_size':70,
    'shape':'square',
    'border_color':'#7a0bbf',
    'border_size':6,
    'mirrored' : True
    }

def reed_config_json():   
    try:
        with open('config.json','r', encoding='utf8') as file:
            json_config = json.load(file)
            if check_config_json(json_config):
                return json_config
            else:
                return default_config

    except:
        return default_config
        
def write_config_json(preferences):
    try:
        with open('config.json','w', encoding='utf8') as file:
            json.dump(preferences, file, indent=2)
            return True
    except:
        return False

def check_config_json(json_file):
    if json_file.keys() == default_config.keys():
        return True
    else:
        return False


