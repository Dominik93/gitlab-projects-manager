from typing import Callable

from commons.optional import Optional, of, empty
from functools import reduce


def flat(items):
    return reduce(list.__add__, items)


def partition_by_number(items: [], number_of_partition: int):
    size = round(len(items) / number_of_partition)
    return partition_by_size(items, size if size > 0 else 1)


def partition_by_size(items: [], size: int):
    if len(items) < size:
        return [items]
    return list(_partition(items, size))


def find_item(items: list[any], predicate: Callable) -> Optional:
    for item in items:
        if predicate(item):
            return of(item)
    return empty()


def _partition(items, size):
    return [items[i:i + size] for i in range(0, len(items), size)]
