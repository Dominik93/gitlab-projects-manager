import json


def read_configuration(name):
    return read(name)


def read(file):
    with open(file + ".json", 'r') as file:
        return json.load(file)
