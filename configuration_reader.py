import json

_CONFIG = "config.json"


def read_configuration():
    return read(_CONFIG)


def read(file):
    with open(file, 'r') as file:
        return json.load(file)
