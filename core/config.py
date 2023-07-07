import configparser

import yaml

CONFIG = configparser.ConfigParser()
CONFIG.read('config.ini')


def update_config(key, value):
    keys = key.split(".")
    current = CONFIG
    for k in keys[:-1]:
        current = current[k]
    current[keys[-1]] = value


def import_env():
    with open('config.yaml', 'r') as file:
        data = yaml.safe_load(file)

    return data
