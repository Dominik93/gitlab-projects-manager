import time
from enum import Enum

from commons.logger import get_logger


class ExceptionStrategy(Enum):
    PASS = 1
    INTERRUPT = 2
    ASK = 3


class CountableProcessor:

    def __init__(self, items: list):
        self.items = items
        self.results = []
        self.logger = get_logger(self.__class__.__name__)

    def run(self, item_processor: callable, input_provider=lambda: input("You want to continue? Y/N"),
            exception_strategy=ExceptionStrategy.INTERRUPT):
        all_start = time.time_ns()
        total = len(self.items)
        for idx, item in enumerate(self.items):
            item_start = time.time_ns()
            try:
                self.logger.debug("run", f'Process {item}')
                self.results.append(item_processor(item))
            except Exception as e:
                item_duration = self._get_duration(item_start)
                all_duration = self._get_duration(all_start)
                self.logger.error("run",
                                  f'Exception "{e}" during iteration {idx + 1}/{total} in {item_duration}/{all_duration}ms')
                if exception_strategy == ExceptionStrategy.ASK:
                    retry = input_provider()
                    if retry == 'N':
                        return self.results
                if exception_strategy == ExceptionStrategy.INTERRUPT:
                    self.logger.warn("run", f'Processing interrupted, returning already processed items')
                    return self.results
            item_duration = self._get_duration(item_start)
            all_duration = self._get_duration(all_start)
            self.logger.info("run", f'Processed {idx + 1}/{total} in {item_duration}/{all_duration}ms')
        return self.results

    def _get_duration(self, start):
        return self._convert_to_ms(time.time_ns() - start)

    def _convert_to_ms(self, ns):
        return int(ns / 1000000)
