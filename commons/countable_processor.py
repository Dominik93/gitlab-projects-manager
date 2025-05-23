import time

from enum import Enum


class ExceptionStrategy(Enum):
    PASS = 1
    INTERRUPT = 2


class CountableProcessor:

    def __init__(self, item_processor: callable, strategy=ExceptionStrategy.INTERRUPT):
        self.exception_strategy = strategy
        self.results = []
        self.item_processor = item_processor

    def run(self, items: list):
        start = time.time_ns()
        total = len(items)
        for idx, item in enumerate(items):
            try:
                self.results.append(self.item_processor(item))
            except Exception as e:
                duration = self._get_duration(start)
                print(f'Exception {e} during iteration {idx + 1}/{total} {duration}ms')
                if self.exception_strategy == ExceptionStrategy.INTERRUPT:
                    return self.results
            duration = self._get_duration(start)
            print(f'Processed {idx + 1}/{total} in {duration}ms')
        return self.results

    def _get_duration(self, start):
        return self._convert_to_ms(time.time_ns() - start)

    def _convert_to_ms(self, ns):
        return int(ns / 1000000)
