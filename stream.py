import itertools
from collections.abc import Iterable, Callable

from collectors import Collector


class Stream:
    def __init__(self, data: Iterable):
        self.data = data

    def skip(self, num: int):
        return self.__class__(itertools.islice(self.data, num, None))

    def limit(self, max_size: int):
        return self.__class__(itertools.islice(self.data, max_size))

    def map(self, key_func: Callable):
        def _map(key_func, iterable):
            for x in iterable:
                yield key_func(x)

        return self.__class__(_map(key_func, self.data))

    def filter(self, predicate):
        def _filter(predicate, iterable):
            if predicate is None:
                predicate = bool
            for x in iterable:
                if predicate(x):
                    yield x

        return self.__class__(_filter(predicate, self.data))

    def to_list(self) -> list:
        return list(self.data)

    def to_set(self) -> set:
        return set(self.data)

    def all(self, predicate) -> bool:
        return all(predicate(d) for d in self.data)

    def any(self, predicate) -> bool:
        return any(predicate(d) for d in self.data)

    def first_else_none(self, predicate):
        for d in self.data:
            if predicate(d):
                return d
        return None

    def sum(self):
        return sum(self.data)

    def collect(self, collector: Collector):
        supplier = collector.supplier()
        accumulator = collector.accumulator()
        finisher = collector.finisher()
        result_value = supplier()
        for element in self.data:
            accumulator(result_value, element)
        return finisher(result_value)
