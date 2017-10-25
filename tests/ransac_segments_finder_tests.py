import unittest
import math

from sympy import Point2D, Segment, pi

from core.finders.ransac import RansacSegmentsFinder

__author__ = 'Xomak'


class RansacSegmentsFinderTest(unittest.TestCase):

    @staticmethod
    def are_points_close(point1: Point2D, point2: Point2D):
        return math.isclose(float(point1.x), float(point2.x)) \
               and math.isclose(float(point1.y), float(point2.y))

    @staticmethod
    def are_segments_close(segment1: Segment, segment2: Segment):
        return RansacSegmentsFinderTest.are_points_close(segment1.p1, segment2.p1) \
               and RansacSegmentsFinderTest.are_points_close(segment1.p2, segment2.p2)

    def test_find_segments_in_polylines_two_lines(self):
        top = [Point2D(x, 0) for x in range(0, 5)]
        bottom = [Point2D(x, 4) for x in range(0, 5)]
        points = top + bottom

        originating_point = Point2D(0, 0)
        points_rotated = []

        for point in points:
            points_rotated.append(point.rotate(pi/4, originating_point))

        segments_reference = {Segment(points_rotated[0], points_rotated[4]),
                              Segment(points_rotated[5], points_rotated[9])}

        finder = RansacSegmentsFinder(0.001, 1.1)
        segments = finder.find_segments_in_points(points_rotated)

        for segment_real in segments:
            found_similarities = 0
            similar = None

            for segment_reference in segments_reference:
                if self.are_segments_close(segment_real, segment_reference):
                    similar = segment_reference
                    found_similarities += 1

            self.assertEqual(1, found_similarities)
            segments_reference.remove(similar)


