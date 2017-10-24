import unittest

from sympy import Line, Point2D, sqrt, Segment

from finders import SegmentsInLineFinder

__author__ = 'Xomak'


class SegmentsInlineFinderTest(unittest.TestCase):
    def test_project_on_line_simple(self):
        line = Line(Point2D(0, 0), Point2D(10, 0))
        points_coords = (
            (-10, 5),
            (-5, -5),
            (0, 5),
            (5, -5)
        )

        points = [Point2D(coord[0], coord[1]) for coord in points_coords]
        points_reference = [SegmentsInLineFinder.ProjectedPoint(
            Point2D(coord[0], coord[1]),
            Point2D(coord[0], 0),
            coord[0])
                            for coord in points_coords]

        points_test = SegmentsInLineFinder.project_on_line(line, points)

        self.assertListEqual(points_reference, points_test)

    def test_project_on_line_parallel(self):
        """
        Simple test, building line and points near it, which can form parallel line.
        """

        line = Line(Point2D(0, 0), Point2D(4, 4))

        not_line_points = set()

        start_point = Point2D(0, -2)

        points_reference = []

        not_line_point = start_point
        for i in range(0, 5):
            not_line_points.add(Point2D(not_line_point.x, not_line_point.y))

            projected_point = SegmentsInLineFinder.ProjectedPoint(not_line_point, Point2D(not_line_point.x - 1,
                                                                                          not_line_point.y + 1),
                                                                  (i - 1) * sqrt(2))

            points_reference.append(projected_point)
            not_line_point = Point2D(not_line_point.x + 1, not_line_point.y + 1)

        points_test = SegmentsInLineFinder.project_on_line(line, not_line_points)

        self.assertListEqual(points_test, points_reference)

    def test_find_segments_one_segment(self):
        line = Line(Point2D(0, 0), Point2D(10, 0))
        points_coords = (
            (-10, 5),
            (-5, -5),
            (0, 5),
            (5, -5)
        )

        points = [Point2D(coord[0], coord[1]) for coord in points_coords]

        segments_reference = [Segment(Point2D(-10, 0), Point2D(5, 0))]
        segments_test = SegmentsInLineFinder.find_segments(line, points, 6)

        self.assertListEqual(segments_reference, segments_test)

    def test_find_segments_two_segments(self):
        line = Line(Point2D(0, 0), Point2D(10, 0))
        points_coords = (
            (-10, 5),
            (-5, -5),
            (0, 5),
            (5, -5),
            (15, 10),
            (18, 5)
        )

        points = [Point2D(coord[0], coord[1]) for coord in points_coords]

        segments_reference = [Segment(Point2D(-10, 0), Point2D(5, 0)), Segment(Point2D(15, 0), Point2D(18, 0))]
        segments_test = SegmentsInLineFinder.find_segments(line, points, 6)

        self.assertListEqual(segments_reference, segments_test)
