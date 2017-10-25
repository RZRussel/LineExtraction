from collections import namedtuple
from typing import Iterable, List

from sympy import Line, Ray, Point2D, Segment

from core.base import Area
from core.finders.base import Finder

__author__ = 'Xomak'


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