import unittest

from sympy import Point2D, Segment

from core.base import Polyline, Area
from core.finders.rdp import RDPSegmentsFinder

__author__ = 'Xomak'


class RDPSegmentsFinderTest(unittest.TestCase):

    def test_find_polyline_in_points_simple(self):
        points = [Point2D(0, 0), Point2D(1, 1), Point2D(2, 2), Point2D(3, 3)]

        polyline_reference = Polyline()
        polyline_reference.add(points[0])
        polyline_reference.add(points[3])

        finder = RDPSegmentsFinder(epsilon=0.5)
        polyline = finder.find_polyline_in_points(points)

        self.assertEqual(polyline, polyline_reference)

    def test_find_simple(self):
        points = [Point2D(0, 0), Point2D(1, 1), Point2D(2, 2), Point2D(3, 3)]
        area = Area()
        polyline = Polyline()
        for point in points:
            polyline.add(point)

        area.add_object(Polyline, polyline)
        finder = RDPSegmentsFinder(epsilon=0.5)
        finder.find(area)

        self.assertListEqual(area.get_objects(Segment), [Segment(points[0], points[-1])])

    def test_find_segments_in_polylines_square(self):
        top = [Point2D(x, 0) for x in range(0, 5)]
        right = [Point2D(4, y) for y in range(1, 5)]
        bottom = [Point2D(x, 4) for x in range(3, 0, -1)]
        left = [Point2D(0, y) for y in range(4, 0, -1)]
        square = top + right + bottom + left

        polyline = Polyline()
        for point in square:
            polyline.add(point)

        segments_reference = {Segment(square[0], square[4]),
                              Segment(square[4], square[8]),
                              Segment(square[8], square[12]),
                              Segment(square[12], square[15])}

        finder = RDPSegmentsFinder(epsilon=0.5)
        segments = finder.find_segments_in_polylines([polyline])

        self.assertSetEqual(set(segments),  segments_reference)
