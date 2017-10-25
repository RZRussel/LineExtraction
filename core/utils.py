__author__ = 'Xomak'


class MinMaxFinder:
    def __init__(self):
        self._current = None

    def _condition(self, value):
        raise NotImplementedError()

    @property
    def current(self):
        return self._current

    def put(self, value: float):
        if self._current is None or self._condition(value):
            self._current = value


class MinFinder(MinMaxFinder):
    def _condition(self, value):
        return value < self._current


class MaxFinder(MinMaxFinder):
    def _condition(self, value):
        return value > self._current
