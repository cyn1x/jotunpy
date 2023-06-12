import configparser

CONFIG = configparser.ConfigParser()
CONFIG.read('config.ini')


def update_config(key, value):
    keys = key.split(".")
    current = CONFIG
    for k in keys[:-1]:
        current = current[k]
    current[keys[-1]] = value
