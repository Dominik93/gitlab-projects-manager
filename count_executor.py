
def run_countable(items, runnable):
    i = 0
    total = len(items)
    for item in items:
        runnable(item)
        i += 1
        print(f'Executed {i}/{total}')


def provide_countable(items, supplier) -> list:
    results = []
    i = 0
    total = len(items)
    for item in items:
        results.append(supplier(item))
        i += 1
        print(f'Executed {i}/{total}')
    return results
