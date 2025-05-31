import json
import os.path
import pickle
from enum import Enum


class Storage(Enum):
    PICKLE = 1
    JSON = 2


def create_store(storage: Storage):
    if storage == Storage.PICKLE:
        return PickleStore()
    if storage == Storage.JSON:
        return JsonStore()


class Store:

    def __init__(self, loader, saver, extension):
        self.loader = loader
        self.saver = saver
        self.extension = extension

    def load(self, supplier, storage):
        if os.path.isfile(storage + "." + self.extension):
            return self.loader(storage + "." + self.extension)
        obj = supplier()
        self.saver(obj, storage + "." + self.extension)
        return obj

    def get(self, storage):
        if os.path.isfile(storage + "." + self.extension):
            return self.loader(storage + "." + self.extension)
        raise Exception(f"Store {storage} not exist")

    def store(self, obj, storage):
        self.saver(obj, storage + "." + self.extension)


class JsonStore(Store):

    def __init__(self):
        super().__init__(lambda storage: self._load(storage),
                         lambda obj, storage: self._store(obj, storage),
                         "json")

    def _store(self, obj, storage):
        with open(storage, 'w', encoding='utf-8') as f:
            json.dump(obj, f, ensure_ascii=False, indent=4)

    def _load(self, storage):
        with open(storage, encoding='utf-8') as f:
            return json.load(f)


class PickleStore(Store):

    def __init__(self):
        super().__init__(lambda storage: self._load(storage),
                         lambda obj, storage: self._store(obj, storage),
                         "pkl")

    def _store(self, obj, storage):
        with open(storage, 'wb') as outp:
            pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)

    def _load(self, storage):
        with open(storage, 'rb') as inp:
            return pickle.load(inp)
