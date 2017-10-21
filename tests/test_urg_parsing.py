import unittest
from utils import *


class TestURGParsing(unittest.TestCase):
    def test_urgxy_one_point(self):
        test_str = "222:(1;2;0)"
        timestamp, points = parse_urgxy_from_str(test_str)

        assert timestamp == 222 and len(points) == 1
        assert abs(points[0][0] - 1.0) < 1e-6 and abs(points[0][1] - 2.0) < 1e-6

    def test_urgxy_two_points_and_strip(self):
        test_str = "222: (1;2;0), (3;2;0),  \t\n"
        timestamp, points = parse_urgxy_from_str(test_str)

        assert timestamp == 222 and len(points) == 2
        assert abs(points[0][0] - 1.0) < 1e-6 and abs(points[0][1] - 2.0) < 1e-6
        assert abs(points[1][0] - 3.0) < 1e-6 and abs(points[1][1] - 2.0) < 1e-6
