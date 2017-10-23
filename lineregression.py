import numpy
import sympy
import math
import sys
from finders import *


class LineRegressionSegmentsFinder(SegmentsFinder):

    def __init__(self, window_size, segmentation_size, segmentation_threshold):
        if window_size % 2 != 1:
            raise ValueError("Window size must be odd number")

        if segmentation_size % 2 != 1:
            raise ValueError("Segmentation size must be odd number")

        self._window_size = window_size
        self._segmentation_size = segmentation_size
        self._segmentation_threshold = segmentation_threshold

    def find(self, area: Area):
        points = list(area.get_objects(sympy.Point2D))
        segmentation_entities = self._perform_segmentation(points)

    def _perform_segmentation(self, points):
        line_entities = []
        for i in range(0, len(points) - self._window_size):
            fit_points = points[i:i + self._window_size]
            line_entities.append(LinearRegressionEntity(fit_points))

        segmentation_entities = []
        current_segment = []
        for i in range(0, len(line_entities)):
            lind = i - (self._segmentation_size - 1)/2
            if lind < 0:
                lind = 0

            rind = i + (self._segmentation_size - 1)/2
            if rind >= len(line_entities):
                rind = len(line_entities) - 1

            curr_entities = line_entities[lind:rind+1]
            weighted_mean_entity = LinearRegressionEntity.weighted_mean_entity(curr_entities)

            d = 0.0
            for entity in curr_entities:
                d = d + LinearRegressionEntity.mahalanobis_distance_sqr(entity, weighted_mean_entity)

            if d < self._segmentation_threshold:
                current_segment.extend(curr_entities[-1].points)
            elif len(current_segment) > 0:
                segmentation_entities.append(LinearRegressionEntity(current_segment))
                current_segment = []

        return segmentation_entities


class LinearRegressionEntity:

    def __init__(self, points=None, slope=None, offset=None, covariance=None):
        if points is not None:
            x_values = numpy.array(list(map(lambda p: p.x, points)), dtype=float)
            y_values = numpy.array(list(map(lambda p: p.y, points)), dtype=float)

            line_params = numpy.polyfit(x_values, y_values, 1)
            cov = numpy.cov(x_values, y_values)

            self._slope = line_params[0]
            self._offset = line_params[1]
            self._covariance = cov
            self._points = points
        else:
            self._slope = slope
            self._offset = offset
            self._covariance = covariance

    @property
    def slope(self):
        return self._slope

    @property
    def offset(self):
        return self._offset

    @property
    def covariance(self):
        return self._covariance

    @property
    def points(self):
        return self._points

    @staticmethod
    def mahalanobis_distance_sqr(entity1, entity2):
        points1 = numpy.array([entity1.slope, entity1.offset])
        points2 = numpy.array([entity2.slope, entity2.offset])
        points_diff = points2 - points1
        covariance = entity1.covariance + entity2.covariance

        if not is_singular_covariance(covariance):
            return (points_diff.dot(numpy.linalg.inv(covariance))).dot(points_diff.T)
        else:
            return (points_diff.dot(numpy.linalg.pinv(covariance))).dot(points_diff.T)

    @staticmethod
    def weighted_mean_entity(entities):
        if len(entities) == 0:
            raise ValueError("Entities list must not be empty")

        inv_weighted_cov = None
        weighted_point = None

        for entity in entities:
            if is_singular_covariance(entity.covariance):
                raise ValueError("Singular covariance matrix")

            inv_cov = numpy.linalg.inv(entity.covariance)

            if weighted_point is None:
                weighted_point = inv_cov.dot(numpy.array([entity.slope, entity.offset]).T)
            else:
                weighted_point = weighted_point + inv_cov.dot(numpy.array([entity.slope, entity.offset]).T)

            if inv_weighted_cov is None:
                inv_weighted_cov = inv_cov
            else:
                inv_weighted_cov = inv_weighted_cov + inv_cov

        if is_singular_covariance(inv_weighted_cov):
            raise ValueError("Singular weighted inverse covariance matrix")

        weighted_cov = numpy.linalg.inv(inv_weighted_cov)
        weighted_point = weighted_cov.dot(weighted_point.T)

        return LinearRegressionEntity(slope=weighted_point[0], offset=weighted_point[1], covariance=weighted_cov)


def is_singular_covariance(covariance: numpy.array):
    return math.fabs(numpy.linalg.det(covariance)) < sys.float_info.epsilon
