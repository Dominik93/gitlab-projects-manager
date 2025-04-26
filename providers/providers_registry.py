providers_registry = {}


def add_provider(key):
    def _add_provider(func):
        providers_registry[key] = func
        return func

    print(f'Register {key}')
    return _add_provider
