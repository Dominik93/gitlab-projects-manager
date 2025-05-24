import time
from enum import Enum


class Level(Enum):
    INFO = 1
    DEBUG = 2
    TRACE = 3
    OFF = 4


def log(level=Level.INFO,
        start_message="Execution started {name}{args}",
        end_message="Execution completed {name}{args}{result} in {duration}ms"):
    def log_decorator(func):
        def log_wrapper(*args, **kwargs):
            start = time.time_ns()
            log_args = _get_log(level, [Level.INFO, Level.OFF], lambda: args)
            _print(level, start_message, lambda x: x.format(name=func.__name__, args=log_args))
            result = func(*args, **kwargs)

            duration = _get_duration(start)
            log_result = _get_log(level, [Level.INFO, Level.OFF], lambda: f" returned: {str(result)}")
            _print(level, end_message,
                   lambda x: x.format(name=func.__name__, args=log_args, result=log_result, duration=duration))
            return result

        return log_wrapper

    return log_decorator


def _get_duration(start):
    return _convert_to_ms(time.time_ns() - start)


def _convert_to_ms(ns):
    return int(ns / 1000000)


def _print(level, log_format, content_provider):
    if log_format is None:
        return
    if level != Level.OFF:
        print(content_provider(log_format))


def _get_log(level, exclude_levels, log_provider):
    if level in exclude_levels:
        return ""
    return log_provider()
