import abc
from collections.abc import Callable


class Collector(abc.ABC):
    @abc.abstractmethod
    def supplier(self) -> Callable:
        pass

    @abc.abstractmethod
    def accumulator(self) -> Callable:
        pass

    def finisher(self) -> Callable:
        return lambda container: container


class ToListCollector(Collector):
    def supplier(self):
        return lambda: []

    def accumulator(self):
        return lambda container, element: container.append(element)


class GroupingByCollector(Collector):
    def __init__(self, classifier: Callable, downstream: Collector | None = None) -> None:
        self.classifier = classifier
        self.downstream = downstream

    def supplier(self):
        return lambda: {}

    def accumulator(self):
        def _inner(container, elements):
            key = self.classifier(elements)

            default_value = []
            if self.downstream:
                default_value = self.downstream.supplier()()

            if key not in container:
                container[key] = default_value

            if self.downstream:
                self.downstream.accumulator()(container[key], elements)
            else:
                container[key].append(elements)

        return _inner

    def finisher(self):
        def _inner(container: dict):
            if not self.downstream:
                return container
            downstream_finisher = self.downstream.finisher()
            for k, v in container.items():
                container[k] = downstream_finisher(v)
            return container

        return _inner


class MaxByCollector(Collector):
    def __init__(self, key_extra: Callable | None = None) -> None:
        self.key_extra = key_extra

    def supplier(self):
        return lambda: [None]

    def accumulator(self) -> Callable:
        def _inner(container, element):
            _max = container[0]
            if _max is None:
                container[0] = _max
                return
            container[0] = max(_max, element, key=self.key_extra)

        return _inner

    def finisher(self):
        return lambda container: container[0]


class MinByCollector(Collector):
    def __init__(self, key_extra: Callable | None = None) -> None:
        self.key_extra = key_extra

    def supplier(self):
        return lambda: [None]

    def accumulator(self) -> Callable:
        def _inner(container, element):
            _min = container[0]
            if _min is None:
                container[0] = element
                return

            container[0] = min(_min, element, key=self.key_extra)

        return _inner

    def finisher(self):
        return lambda container: container[0]


class CountingCollector(Collector):
    def supplier(self):
        return lambda: [0]

    def accumulator(self) -> Callable:
        def _inner(counter, _):
            counter[0] += 1

        return _inner

    def finisher(self):
        return lambda container: container[0]
