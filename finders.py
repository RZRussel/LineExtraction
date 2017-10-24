from collections import namedtuple
from typing import List, Iterable

import numpy as np
from rdp import rdp
from skimage.measure import LineModelND
from skimage.measure import ransac
from sympy import Point2D, Segment, Line, Ray

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


class SegmentsInLineFinder(Finder):
    ProjectedPoint = namedtuple('ProjectedPoint', ('point', 'projection', 'line_coordinate'))
    FoundSegment = namedtuple('FoundSegment', ('segment', 'points_number', 'density'))

    def find(self, area: Area) -> Area:
        # TODO: Implement this
        raise NotImplementedError()

    @staticmethod
    def project_on_line(line: Line, points: Iterable[ProjectedPoint]) -> List[ProjectedPoint]:
        some_line_point = line.p1
        line_points = []

        for current_point in points:

            projection = line.projection(current_point)
            if projection == some_line_point:
                line_coordinate = 0
            else:
                dst_ray = Ray(some_line_point, projection)
                is_inversed = dst_ray.angle_between(line) != 0
                line_coordinate = some_line_point.distance(projection)
                if is_inversed:
                    line_coordinate = -line_coordinate

            line_points.append(SegmentsInLineFinder.ProjectedPoint(current_point, projection, line_coordinate))

        line_points.sort(key=lambda point: point.line_coordinate)
        return line_points

    @staticmethod
    def find_segments(line: Line, points: Iterable[Point2D], epsilon: float) -> List[Segment]:
        return [found_segment.segment for found_segment in
                SegmentsInLineFinder.find_segments_with_density(line, points, epsilon)]

    @staticmethod
    def find_segments_with_density(line: Line, points: Iterable[Point2D], epsilon: float) -> List[FoundSegment]:
        line_points = SegmentsInLineFinder.project_on_line(line, points)

        segments = []
        current_start_point = None
        current_segment_points_number = 0

        for i, current_point in enumerate(line_points):

            if current_start_point is None:
                current_start_point = current_point
                current_segment_points_number = 0

            current_segment_points_number += 1

            if i == len(line_points) - 1 \
                    or abs(current_point.line_coordinate - line_points[i + 1].line_coordinate) > epsilon:
                if current_point != current_start_point:
                    segment = Segment(current_start_point.projection, current_point.projection)
                    density = current_segment_points_number / segment.length
                    segments.append(SegmentsInLineFinder.FoundSegment(segment, current_segment_points_number, density))
                current_start_point = None

        return segments


class RansacSegmentsFinder(SegmentsFinder):
    """
    RANSAC segments finder. Currently it does not support segments, parallel to Y-axis.
    """

    def __init__(self, residual_threshold, segments_threshold, max_trials=1000,
                 density_threshold=None, length_threshold=None):
        """
        Inits finder
        :param residual_threshold: Residual threshold for RANSAC
        :param segments_threshold: Maximal distance between points in one line to be considered as one segment
        :param max_trials: Max trials for one RANSAC
        :param density_threshold: Threshold for new segments finder (if previous segment's density is less
        than this value, process will be stopped)
        :param length_threshold: Threshold for new segments finder (if previous segment's length is less
        than this value, process will be stopped)
        """
        self.length_threshold = length_threshold
        self.density_threshold = density_threshold
        self.max_trials = max_trials
        self.segments_threshold = segments_threshold
        self.residual_threshold = residual_threshold

    def find(self, area: Area) -> Area:
        points = area.get_objects(Point2D)
        segments = self.find_segments_in_points(points)
        for segment in segments:
            area.add_object(Segment, segment)
        return area

    def find_segments_in_points(self, points: List[Point2D]) -> List[Segment]:
        np_points = np.ndarray((len(points), 2))

        segments = []

        for idx, point in enumerate(points):
            np_points[idx, 0] = point.x
            np_points[idx, 1] = point.y

        is_density_valid = True
        is_length_valid = True

        while len(np_points) > 2 \
                and (self.density_threshold is None or is_density_valid) \
                and (self.length_threshold is None or is_length_valid):

            model_robust, inliers_mask = ransac(np_points, LineModelND, min_samples=2,
                                                residual_threshold=self.residual_threshold, max_trials=self.max_trials)

            inliers = np_points[inliers_mask]

            line_params = model_robust.params

            origin = Point2D(line_params[0][0], line_params[0][1])
            direction = Point2D(line_params[1][0], line_params[1][1])

            line = Line(origin, origin + direction)
            points = [Point2D(point[0], point[1]) for point in inliers]
            found_segments = SegmentsInLineFinder.find_segments_with_density(line, points, 150)
            current_segments = []
            densities = []
            lengths = []

            for found_segment in found_segments:
                current_segments.append(found_segment.segment)
                densities.append(found_segment.density)
                lengths.append(found_segment.segment.length)

            if len(densities) > 0:
                avg_density = np.mean(densities)
                avg_length = np.mean(lengths)
                if self.density_threshold:
                    is_density_valid = avg_density > self.density_threshold
                if self.length_threshold:
                    is_length_valid = avg_length > self.length_threshold
            else:
                is_density_valid = False
                is_length_valid = False

            segments += current_segments

            np_points = np_points[~inliers_mask]

        return segments
