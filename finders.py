from typing import List

from sympy import Point2D

from base import Area, Polyline

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


class PolylinesFinder(Finder):

    def __init__(self, epsilon):
        self._epsilon = epsilon

    def _accept_point(self, point1: Point2D, point2: Point2D):
        return point1.distance(point2) < self._epsilon

    def find(self, area: Area) -> Area:
        points = area.get_objects(Point2D)
        polylines = self.find_polylines(points)
        for line in polylines:
            area.add_object(Polyline, line)
        return area

    def find_polylines(self, points: List[Point2D]) -> List[Polyline]:

        if len(points) == 0:
            raise ValueError("There is no points")

        found_polylines = []
        current_polyline = Polyline()
        previous_point = None

        for current_point in points:
            if previous_point is not None and not self._accept_point(current_point, previous_point):
                found_polylines.append(current_polyline)
                current_polyline = Polyline()
            current_polyline.add(current_point)
            previous_point = current_point

        found_polylines.append(current_polyline)

        return found_polylines
