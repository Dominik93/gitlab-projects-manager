import time


def run_countable(items, runnable):
    start = time.time_ns()
    i = 0
    total = len(items)
    for item in items:
        runnable(item)
        i += 1
        duration = int((time.time_ns() - start) / 1000000)
        print(f'Executed {i}/{total} {duration}ms')


def provide_countable(items, supplier) -> list:
    start = time.time_ns()
    results = []
    i = 0
    total = len(items)
    for item in items:
        results.append(supplier(item))
        i += 1
        duration = int((time.time_ns() - start) / 1000000)
        print(f'Executed {i}/{total} {duration}ms')
    return results
