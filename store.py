import os.path
import pickle


def get(storage):
    if os.path.isfile(storage):
        return _load(storage)
    raise Exception(f"Object {storage} not found.")


def load(supplier, storage):
    if os.path.isfile(storage):
        return _load(storage)
    obj = supplier()
    _store(obj, storage)
    return obj


def _load(obj):
    with open(obj, 'rb') as inp:
        return pickle.load(inp)


def _store(obj, storage):
    with open(storage, 'wb') as outp:
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)
