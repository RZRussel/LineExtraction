import unittest

from sympy import Point2D
import numpy as np

from converters import PointsToImageRoundBasedConverter

__author__ = 'Xomak'


class PointsToImageRoundBasedConverterTest(unittest.TestCase):

    def test_convert_simple_points_image_correct(self):

        points = [Point2D(-1, -1), Point2D(1, 1)]
        image_reference = np.zeros((3, 3), dtype=int)
        image_reference[0, 0] = 1
        image_reference[2, 2] = 1

        converter = PointsToImageRoundBasedConverter()
        image, inverse_converter = converter.convert(points)

        self.assertTrue(np.array_equal(image, image_reference))

    def test_convert_simple_points_inverse_correct(self):

        points = [Point2D(-1, -1), Point2D(1, 1)]

        converter = PointsToImageRoundBasedConverter()
        image, inverse_converter = converter.convert(points)

        self.assertEqual(inverse_converter.convert(Point2D(0, 0)), points[0])
        self.assertEqual(inverse_converter.convert(Point2D(2, 2)), points[1])

    def test_convert_decimal_points_image(self):

        points = [Point2D(10.4, 10.3), Point2D(11.3, 11.4)]
        image_reference = np.zeros((2, 2), dtype=int)
        image_reference[0, 0] = 1
        image_reference[1, 1] = 1

        converter = PointsToImageRoundBasedConverter()
        image, inverse_converter = converter.convert(points)

        self.assertTrue(np.array_equal(image, image_reference))

    def test_convert_decimal_points_inverse_correct(self):

        points = [Point2D(10.4, 10.3), Point2D(11.3, 11.4)]
        converter = PointsToImageRoundBasedConverter()
        image, inverse_converter = converter.convert(points)

        self.assertEqual(inverse_converter.convert(Point2D(0, 0)), Point2D(10, 10))
        self.assertEqual(inverse_converter.convert(Point2D(1, 1)), Point2D(11, 11))
