from core.base import Area

__author__ = 'Xomak'


class Finder:
    pass


class SegmentsFinder(Finder):
    def find(self, area: Area) -> Area:
        """
        Finds objects in Area, and adds them to the same Area object
        :param area: Area to find objects
        :return: The same object (but modified)
        """
        pass