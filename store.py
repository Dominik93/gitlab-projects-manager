import os.path
import pickle

_STORE = 'store.pkl'


def load(supplier):
    if os.path.isfile(_STORE):
        return _load()
    obj = supplier()
    _store(obj)
    return obj


def _load():
    with open(_STORE, 'rb') as inp:
        return pickle.load(inp)


def _store(obj):
    with open(_STORE, 'wb') as outp:
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)
