import numpy
import sympy
from finders import *


class LineRegressionSegmentsFinder(SegmentsFinder):

    def __init__(self, window_size, threshold):
        self._window_size = window_size
        self._threshold = threshold

    def find(self, area: Area):
        points = list(area.get_objects(sympy.Point2D))
        points.sort(key=lambda x: x.args)

        line_params = []
        for i in range(0, len(points) - self._window_size):
            fit_points = points[i:i+self._window_size]
            line_params.append(self.fit_line(fit_points))

    def fit_line(self, points):
        x_values = list(map(lambda p: p.x, points))
        y_values = list(map(lambda p: p.y, points))

        line_coeffs = numpy.polyfit(numpy.array(x_values, dtype=float), numpy.array(y_values, dtype=float), 1)
        return sympy.Line2D(sympy.Point2D(0, line_coeffs[1]), slope=line_coeffs[0])
