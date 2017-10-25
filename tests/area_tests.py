import unittest

from sympy import Point2D, Segment

from core.base import Area

__author__ = 'Xomak'


class TestArea(unittest.TestCase):

    def test_get_objects_if_empty(self):
        a = Area()
        self.assertListEqual(a.get_objects(Point2D), [])

    def test_get_objects_not_empty(self):
        a = Area()
        point = Point2D(1, 1)
        a.add_object(Point2D, point)
        self.assertListEqual(a.get_objects(Point2D), [point])

    def test_get_objects_separate_lists(self):
        a = Area()
        point = Point2D(1, 1)
        segment = Segment(Point2D(3, 3), Point2D(4, 4))
        a.add_object(Point2D, point)
        a.add_object(Segment, segment)
        self.assertListEqual(a.get_objects(Point2D), [point])
        self.assertListEqual(a.get_objects(Segment), [segment])
