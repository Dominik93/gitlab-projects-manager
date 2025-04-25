import json

CONFIG = "config.json"


def read_configuration():
    with open(CONFIG, 'r') as file:
        return json.load(file)
