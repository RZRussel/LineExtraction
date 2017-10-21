from typing import Set

from base import Area, SimpleArea

__author__ = 'Xomak'


class AreasSplitter:

    def __init__(self, points):
        self._points = points

    def get_areas(self) -> Set[Area]:
        pass


class SimpleAreaSplitter(AreasSplitter):

    def get_areas(self) -> Set[SimpleArea]:
        pass
