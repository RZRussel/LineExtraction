from collections import namedtuple
from typing import Iterable

import numpy as np
from sympy import Point2D

from core.utils import MinFinder, MaxFinder

__author__ = 'Xomak'


class PointsToImageConverter:

    def convert(self, points: Iterable[Point2D]) -> np.ndarray:
        raise NotImplementedError()


class PointToPointConverter:

    def convert(self, point: Point2D) -> Point2D:
        return NotImplementedError()


class ImagePointToCloudPointConverter(PointToPointConverter):

    def __init__(self, origin: Point2D):
        self.origin = Point2D(round(origin.x), round(origin.y))

    def convert(self, point: Point2D) -> Point2D:
        return point + self.origin


class PointsToImageRoundBasedConverter:

    CloudParams = namedtuple('CloudParams', ('min_x', 'max_x', 'min_y', 'max_y', 'min_precision'))

    def __init__(self, min_precision=0.5):
        self.min_precision = min_precision

    @staticmethod
    def find_cloud_params(points: Iterable[Point2D]) -> CloudParams:
        points_list = list(points)

        min_x = MinFinder()
        max_x = MaxFinder()
        min_y = MinFinder()
        max_y = MaxFinder()
        min_precision = MinFinder()

        for i in range(0, len(points_list)):
            point_a = points_list[i]

            min_x.put(point_a.x)
            max_x.put(point_a.x)

            min_y.put(point_a.y)
            max_y.put(point_a.y)

            for j in range(i+1, len(points_list)):
                point_b = points_list[j]
                x_precision = (abs(point_a.x - point_b.x))
                y_precision = (abs(point_a.y - point_b.y))
                min_precision.put(x_precision)
                min_precision.put(y_precision)

        return PointsToImageRoundBasedConverter.CloudParams(min_x.current,
                                                            max_x.current,
                                                            min_y.current,
                                                            max_y.current,
                                                            min_precision.current)

    def convert(self, points: Iterable[Point2D]) -> (np.ndarray, PointToPointConverter):
        params = self.find_cloud_params(points)

        if params.min_precision < self.min_precision:
            raise ValueError("Cloud contains points with precision less then required.")

        width = round(params.max_x) - round(params.min_x) + 1
        height = round(params.max_y) - round(params.min_y) + 1

        new_origin = Point2D(params.min_x, params.min_y)
        result_array = np.zeros((height, width), dtype=int)

        for point in points:
            point_translated = point - new_origin

            row = round(point_translated.y)
            if row >= height:
                row = height - 1

            column = round(point_translated.x)
            if column >= width:
                column = width - 1

            result_array[row, column] = 1

        return result_array, ImagePointToCloudPointConverter(new_origin)
