from typing import List

from rdp import rdp
from sympy import Point2D, Segment

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


class RDPSegmentsFinder(SegmentsFinder):

    def __init__(self, epsilon):
        self._epsilon = epsilon

    def find(self, area: Area) -> Area:
        polylines = area.get_objects(Polyline)
        segments = self.find_segments_in_polylines(polylines)
        for segment in segments:
            area.add_object(Segment, segment)
        return area

    @staticmethod
    def _dist_function(point, start, end):
        """
        This is simple method to find the euclidean distance. It was implemented here, since rdp's internal one
        does not work correctly on zero distances
        :param point: Point, which distance is measured to
        :param start: Start point of the segment
        :param end: End point of the segment
        :return: Euclidean distance
        """
        start_point = Point2D(start[0], start[1])
        end_point = Point2D(end[0], end[1])
        point_point = Point2D(point[0], point[1])
        return Segment(start_point, end_point).distance(point_point)

    def reduce_polylines(self, polylines: List[Polyline]) -> List[Polyline]:
        """
        Reduces polylines in list, using RDP algorithm
        :param polylines: Polylines list
        :return: List of reduced polylines
        """

        reduced_polylines = []
        for polyline in polylines:
            if len(polyline.points) > 1:
                reduced_polylines.append(self.find_polyline_in_points(polyline.points))

        return reduced_polylines

    def find_segments_in_polylines(self, polylines: List[Polyline]) -> List[Segment]:
        """
        Finds segments in given polylines (with their reducing using RDP)
        :param polylines: Polylines to extract segments
        :return: List of segments
        """
        segments = []

        reduced_polylines = self.reduce_polylines(polylines)
        for polyline in reduced_polylines:
            segments += polyline.get_segments()

        return segments

    def find_polyline_in_points(self, points: List[Point2D]) -> Polyline:
        """
        Finds polyline in given points list, using The Ramer-Douglas-Peucker algorithm
        :param points: List of points
        :return: Polyline
        """
        points_lists = [[point.x, point.y] for point in points]
        mask = rdp(points_lists, return_mask=True, epsilon=self._epsilon, dist=self._dist_function)

        main_points = [point for point, is_main in zip(points, mask) if is_main]

        polyline = Polyline()

        for point in main_points:
            polyline.add(point)

        return polyline
