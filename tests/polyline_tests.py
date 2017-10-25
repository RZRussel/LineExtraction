import unittest

from sympy import Point2D, Segment

from core.base import Polyline

__author__ = 'Xomak'


class PolylineTest(unittest.TestCase):

    def test_get_segments_simple(self):
        t = Polyline()
        points = [Point2D(0, 0), Point2D(1, 1), Point2D(2, 2)]
        for point in points:
            t.add(point)

        self.assertListEqual(t.get_segments(), [Segment(points[0], points[1]), Segment(points[1], points[2])])

    def test_get_segments_same_point(self):
        t = Polyline()
        points = [Point2D(0, 0), Point2D(0, 0), Point2D(2, 2)]
        for point in points:
            t.add(point)

        self.assertRaises(ValueError, t.get_segments)
