from multiprocessing import Pool

from commons.logger import get_logger


class Executor:

    def add_all(self, items, method, arguments):
        """Method - first argument of this must be item in list"""
        for item in items:
            args = [item]
            args.extend(arguments)
            self.add(method, args)

    def add(self, method, arguments):
        pass

    def execute(self):
        pass


class SyncExecutor(Executor):

    def __init__(self):
        self.results = []

    def add(self, method, arguments):
        self.results.append(method(*arguments))

    def execute(self):
        return self.results


class AsyncExecutor(Executor):

    def __init__(self):
        self.results = []
        self.total_tasks = 0
        self.completed_tasks = 0
        self.pool = Pool()
        self.logger = get_logger(self.__class__.__name__)

    def add(self, method, arguments):
        self.total_tasks += 1
        self.results.append(self.pool.apply_async(method, arguments))

    def execute(self):
        results = []
        for result in self.results:
            result = result.get()
            self.completed_tasks += 1
            self.logger.debug("execute", f'Executed {self.completed_tasks}/{self.total_tasks}')
            results.append(result)
        self.pool.close()
        self.pool.join()
        return results
