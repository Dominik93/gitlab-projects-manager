import time
from enum import Enum


class Level(Enum):
    INFO = 1
    DEBUG = 2
    OFF = 3


def log(level=Level.INFO,
        start_message="Execution started {args}",
        end_message="Execution completed {args}{result} in {duration}ms"):
    def log_decorator(func):
        def log_wrapper(*args, **kwargs):
            start = time.time_ns()
            _print(level, func.__name__, start_message,
                   lambda x: x.format(name=func.__name__, args=args))
            result = func(*args, **kwargs)

            duration = _get_duration(start)
            _print(level, func.__name__, end_message,
                   lambda x: x.format(name=func.__name__, args=args, result=f" returned: {str(result)}",
                                      duration=duration))
            return result

        return log_wrapper

    return log_decorator


def _get_duration(start):
    return _convert_to_ms(time.time_ns() - start)


def _convert_to_ms(ns):
    return int(ns / 1000000)


def _print(level, name, log_format, content_provider):
    if log_format is None:
        return
    if level.value < Level.DEBUG.value:
        log_format = (log_format.replace("{args}", "").replace("{args} ", "")
                      .replace("{result} ", "").replace("{result}", ""))
    if level != Level.OFF:
        _print_console(level, name, log_format, content_provider)
        _print_file(level, name, log_format, content_provider)


def _print_console(level, name, log_format, content_provider):
    print(f'{level.name}:{name}:{content_provider(log_format)}')


def _print_file(level, name, log_format, content_provider):
    log_file = open("app.log", "a")
    log_file.write(f'{level.name}:{name}:{content_provider(log_format)}\n')
    log_file.close()


def _get_log(level, exclude_levels, log_provider):
    if level in exclude_levels:
        return ""
    return log_provider()
