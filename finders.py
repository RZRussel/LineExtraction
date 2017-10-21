from collections import namedtuple
from typing import List

from sympy import Point2D, Segment

from base import Area

__author__ = 'Xomak'


class Finder:
    pass


class SegmentsFinder(Finder):

    def find(self, area: Area) -> Area:
        pass


class SplitAndMergeFinder(Finder):

    DistantPoint = namedtuple('DistantPoint', ['point', 'index', 'distance'])

    def __init__(self, split_threshold, merge_dst_threshold, merge_angle_threshold):
        self.split_threshold = split_threshold
        self.merge_dst_threshold = merge_dst_threshold
        self.merge_angle_threshold = merge_angle_threshold

    @staticmethod
    def _find_split_point(segment: Segment, points: List[Point2D]):
        most_distant_point = None

        for idx, point in enumerate(points):
            distance = segment.distance(point)
            if most_distant_point is None or distance > most_distant_point.distance:
                most_distant_point = SplitAndMergeFinder.DistantPoint(point, idx, distance)

        return most_distant_point

    @staticmethod
    def _sort_points(points):
        points.sort(key=lambda point: (point.x, point.y))

    @staticmethod
    def _fit_segment(sorted_points):
        return Segment(sorted_points[0], sorted_points[-1])

    def find(self, area: Area) -> Area:
        pass

    def _find_segments(self, points: List[Point2D]) -> List[Segment]:
        self._sort_points(points)
        point_sets = [points]
        segments = []

        while len(point_sets):
            current_points = point_sets.pop()
            segment = self._fit_segment(current_points)
            if len(current_points) > 2:
                split_point = self._find_split_point(segment, current_points)
                if split_point.distance > self.split_threshold:
                    first_part = current_points[split_point.index:]
                    second_part = current_points[:split_point.index+1]
                    point_sets.append(first_part)
                    point_sets.append(second_part)
                else:
                    segments.append(segment)
            else:
                segments.append(segment)

        return segments

    def _merge_segments(self, segments):
        raise NotImplemented()
        # while len(segments) >= 2:
        #     segment1 = segments.pop()
        #     segment2 = segments.pop()
        #
        #     angle = segment1.angle_between(segment2)
        #     if angle < self.merge_angle_threshold:
        #         pass






