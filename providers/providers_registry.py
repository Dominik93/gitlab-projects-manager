from commons.logger import log, Level

providers_registry = {}


@log(Level.DEBUG, start_message=None, end_message="Register {args}")
def add_provider(key):
    def _add_provider(func):
        providers_registry[key] = func
        return func

    return _add_provider
