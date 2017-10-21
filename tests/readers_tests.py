import tempfile
import unittest
import shutil

from os import path

from sympy import Point2D

from readers import XYFileReader, XYFileAreaReader


class TestXYFileReader(unittest.TestCase):

    def test_parse_one_point(self):
        test_str = "222:(1;2;0)"
        timestamp, points = XYFileReader.parse_file_line(test_str)

        assert timestamp == 222 and len(points) == 1
        assert abs(points[0][0] - 1.0) < 1e-6 and abs(points[0][1] - 2.0) < 1e-6

    def test_parse_two_points_and_strip(self):
        test_str = "222: (1;2;0), (3;2;0),  \t\n"
        timestamp, points = XYFileReader.parse_file_line(test_str)

        assert timestamp == 222 and len(points) == 2
        assert abs(points[0][0] - 1.0) < 1e-6 and abs(points[0][1] - 2.0) < 1e-6
        assert abs(points[1][0] - 3.0) < 1e-6 and abs(points[1][1] - 2.0) < 1e-6


class TestXYFileAreaReader(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_one_line(self):
        file_path = path.join(self.test_dir, 'test1.txt')
        with open(file_path, 'w') as f:
            f.write("2372536:(-114.352;-201.86;0),(-113.112;-202.558;0),")

        area = XYFileAreaReader.get_area(file_path)
        assert area.get_objects(Point2D) == {Point2D(-114.352, -201.86), Point2D(-113.112, -202.558)}
