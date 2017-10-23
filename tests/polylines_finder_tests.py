import unittest

from sympy import Point2D

from base import Area, Polyline
from finders import PolylinesFinder

__author__ = 'Xomak'


class TestPolylinesFinder(unittest.TestCase):

    def test_find_polylines_one_point(self):
        point = Point2D(1, 1)
        polyline = Polyline()
        polyline.add(point)

        finder = PolylinesFinder(epsilon=0.5)
        self.assertListEqual(finder.find_polylines([point]), [polyline])

    def test_find_polylines_two_near_points(self):
        point1 = Point2D(1, 1)
        point2 = Point2D(1, 2)
        polyline = Polyline()
        polyline.add(point1)
        polyline.add(point2)

        finder = PolylinesFinder(epsilon=2)
        self.assertListEqual(finder.find_polylines([point1, point2]), [polyline])

    def test_find_polylines_two_distant_points(self):
        point1 = Point2D(1, 1)
        point2 = Point2D(1, 2)
        polyline1 = Polyline()
        polyline1.add(point1)
        polyline2 = Polyline()
        polyline2.add(point2)

        finder = PolylinesFinder(epsilon=0.5)
        self.assertListEqual(finder.find_polylines([point1, point2]), [polyline1, polyline2])

    def test_find_polylines_two_distant_polylines(self):
        points = [Point2D(1, 1), Point2D(1, 1.1), Point2D(2, 2), Point2D(2, 2.1)]
        polylines = [Polyline(), Polyline()]
        polylines[0].add(points[0])
        polylines[0].add(points[1])
        polylines[1].add(points[2])
        polylines[1].add(points[3])

        finder = PolylinesFinder(epsilon=0.5)
        self.assertListEqual(finder.find_polylines(points), [polylines[0], polylines[1]])

    def test_find_simple(self):
        point = Point2D(1, 1)
        polyline = Polyline()
        polyline.add(point)

        area = Area()
        area.add_object(Point2D, point)

        finder = PolylinesFinder(epsilon=0.5)
        finder.find(area)
        self.assertListEqual(area.get_objects(Polyline), [polyline])
