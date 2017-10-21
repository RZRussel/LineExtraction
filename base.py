from typing import Set

__author__ = 'Xomak'


class Area:

    def __init__(self):
        self._objects_dict = dict()

    def get_objects(self, objects_type) -> Set:
        return set(self._objects_dict[objects_type])

    def add_object(self, object_type, object_to_add):
        if object_type not in self._objects_dict:
            self._objects_dict[object_type] = set()
        self._objects_dict[object_type].add(object_to_add)


class SimpleArea(Area):

    def __init__(self, x, y):
        super().__init__()
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y
