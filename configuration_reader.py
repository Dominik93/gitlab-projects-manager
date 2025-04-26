import json

_CONFIG = "config.json"


def read_configuration():
    with open(_CONFIG, 'r') as file:
        return json.load(file)
