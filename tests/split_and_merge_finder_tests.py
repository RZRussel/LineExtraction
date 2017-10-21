import unittest

from sympy import Point2D, Segment

from finders import SplitAndMergeFinder

__author__ = 'Xomak'


class SplitAndMergeFinderTest(unittest.TestCase):

    def test_find_split_point(self):
        points = [Point2D(0, 0), Point2D(5, 0), Point2D(2, 0), Point2D(5, 5)]
        s = SplitAndMergeFinder(0, 0, 0)
        segment = SplitAndMergeFinder._fit_segment(points)
        self.assertEqual(s._find_split_point(segment, points).point, Point2D(5, 0))

    def test_fit_segment(self):
        a = Point2D(0, 0)
        b = Point2D(5, 5)
        points = [a, Point2D(5, 0), Point2D(2, 0), b]
        self.assertEqual(SplitAndMergeFinder._fit_segment(points), Segment(a, b))

    def test_sort_points(self):
        points = [Point2D(5, 5), Point2D(0, 0), Point2D(5, 0), Point2D(5, 18), Point2D(4, 100)]
        SplitAndMergeFinder._sort_points(points)
        self.assertEqual(points, [Point2D(0, 0), Point2D(4, 100), Point2D(5, 0), Point2D(5, 5), Point2D(5, 18)])

    def test_find_segment_simple(self):
        a = Point2D(0, 0)
        b = Point2D(5, 5)
        t = SplitAndMergeFinder(0, 0, 0)
        segments = t._find_segments([a, b])
        self.assertEqual(segments, [Segment(a, b)])

    def test_find_segment_two_segments(self):
        s1 = [Point2D(x, 0) for x in range(0, 5)]
        s2 = [Point2D(4, y) for y in range(1, 5)]
        t = SplitAndMergeFinder(1, 0, 0)
        segments = t._find_segments(s1 + s2)
        self.assertSetEqual(set(segments), set([Segment(s1[0], s1[-1]), Segment(s1[-1], s2[-1])]))

    # def test_find_segment_square(self):
    #     s1 = [Point2D(x, 0) for x in range(0, 5)]
    #     s2 = [Point2D(4, y) for y in range(1, 5)]
    #     s3 = [Point2D(x, 4) for x in range(0, 4)]
    #     s4 = [Point2D(0, y) for y in range(1, 4)]
    #     t = SplitAndMergeFinder(1, 0, 0)
    #     segments = t._find_segments(s1 + s2 + s3 + s4)
    #     self.assertSetEqual(set(segments), set())






