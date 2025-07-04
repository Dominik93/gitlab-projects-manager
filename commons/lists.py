from functools import reduce
from typing import Callable

from commons.optional import Optional, of, empty



def flat(items):
    return reduce(list.__add__, items)
def partition(items, size):
    if len(items) < size:
        return [items]
    return list(_partition(items, size))


def find_item(items: list[any], predicate: Callable) -> Optional:
    for item in items:
        if predicate(item):
            return of(item)
    return empty()


def _partition(items, size):
    for i in range(0, len(items) // size):
        yield items[i:: size]

