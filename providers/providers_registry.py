providers_registry = {}


def add_provider(key):
    def _add_provider(func):
        providers_registry[key] = func
        return func

    return _add_provider
