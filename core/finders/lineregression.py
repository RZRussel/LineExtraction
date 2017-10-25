import math
import sys
from typing import List

import numpy as np
from sympy import Point2D, Line2D, Segment

from core.base import Area
from core.finders.base import SegmentsFinder
from core.finders.segments import SegmentsInLineFinder


class LinearRegressionEntity:

    def __init__(self, points=None, slope=None, offset=None, covariance=None):
        if points is not None:
            x_values = np.array(list(map(lambda p: p.x, points)), dtype=float)
            y_values = np.array(list(map(lambda p: p.y, points)), dtype=float)

            line_params = np.polyfit(x_values, y_values, 1)
            cov = np.cov(x_values, y_values)

            self._slope = line_params[0]
            self._offset = line_params[1]
            self._covariance = cov
            self._points = points
        else:
            self._slope = slope
            self._offset = offset
            self._covariance = covariance

    @property
    def slope(self) -> float:
        return self._slope

    @property
    def offset(self) -> float:
        return self._offset

    @property
    def covariance(self) -> np.array:
        return self._covariance

    @property
    def points(self) -> List[Point2D]:
        return self._points

    @staticmethod
    def euqlid_distance_sqr(entity1: 'LinearRegressionEntity', entity2: 'LinearRegressionEntity') -> float:
        points1 = np.array([entity1.slope, entity1.offset])
        points2 = np.array([entity2.slope, entity2.offset])
        points_diff = points2 - points1

        return points_diff.dot(points_diff.T)

    @staticmethod
    def mahalanobis_distance_sqr(entity1: 'LinearRegressionEntity', entity2: 'LinearRegressionEntity') -> float:
        points1 = np.array([entity1.slope, entity1.offset])
        points2 = np.array([entity2.slope, entity2.offset])
        points_diff = points2 - points1
        covariance = entity1.covariance + entity2.covariance

        if not is_singular_covariance(covariance):
            return (points_diff.dot(np.linalg.inv(covariance))).dot(points_diff.T)
        else:
            return (points_diff.dot(np.linalg.pinv(covariance))).dot(points_diff.T)

    @staticmethod
    def weighted_mean_entity(entities: List['LinearRegressionEntity']) -> 'LinearRegressionEntity':
        if len(entities) == 0:
            raise ValueError("Entities list must not be empty")

        inv_weighted_cov = None
        weighted_point = None

        for entity in entities:
            if not is_singular_covariance(entity.covariance):
                inv_cov = np.linalg.inv(entity.covariance)
            else:
                inv_cov = np.linalg.pinv(entity.covariance)

            if weighted_point is None:
                weighted_point = inv_cov.dot(np.array([entity.slope, entity.offset]).T)
            else:
                weighted_point = weighted_point + inv_cov.dot(np.array([entity.slope, entity.offset]).T)

            if inv_weighted_cov is None:
                inv_weighted_cov = inv_cov
            else:
                inv_weighted_cov = inv_weighted_cov + inv_cov

        if not is_singular_covariance(inv_weighted_cov):
            weighted_cov = np.linalg.inv(inv_weighted_cov)
        else:
            weighted_cov = np.linalg.pinv(inv_weighted_cov)

        weighted_point = weighted_cov.dot(weighted_point.T)

        return LinearRegressionEntity(slope=weighted_point[0], offset=weighted_point[1], covariance=weighted_cov)


def is_singular_covariance(covariance: np.array) -> bool:
    return math.fabs(np.linalg.det(covariance)) < sys.float_info.epsilon


class LinearRegressionCoordinator:

    def __init__(self, entity: LinearRegressionEntity, start_index: int):
        if entity is None:
            raise ValueError("Can't coordinate empty entity")

        if start_index < 0:
            raise ValueError("Entity's start must not be negative")

        self._entity = entity
        self._start_index = start_index

    @property
    def entity(self) -> LinearRegressionEntity:
        return self._entity

    @property
    def start_index(self) -> int:
        return self._start_index

    def can_merge(self, coordinator: 'LinearRegressionCoordinator') -> bool:
        if coordinator is None:
            return False

        if self.start_index < coordinator.start_index:
            left = self
            right = coordinator
        else:
            left = coordinator
            right = self

        left_points = left.entity.points
        right_points = right.entity.points

        if left_points is None or right_points is None:
            return False

        if left.start_index + len(left_points) < right.start_index:
            return False

        return True

    def merge(self, coordinator: 'LinearRegressionCoordinator') -> 'LinearRegressionCoordinator':
        if coordinator is None:
            raise ValueError("Can't merge with None")

        if self.start_index < coordinator.start_index:
            left = self
            right = coordinator
        else:
            left = coordinator
            right = self

        left_points = left.entity.points
        right_points = right.entity.points

        if left_points is None or right_points is None:
            raise ValueError("No points found to merge")

        if left.start_index + len(left_points) < right.start_index:
            raise ValueError("Intervals must intersect to merge")

        new_points = []
        new_points.extend(left_points)

        cut_position = left.start_index + len(left_points)
        cut_len = right.start_index + len(right_points) - cut_position
        if cut_len > 0:
            new_points.extend(right.entity.points[len(right_points) - cut_len:])

        new_entity = LinearRegressionEntity(points=new_points)
        return LinearRegressionCoordinator(new_entity, left.start_index)


class LineRegressionSegmentsFinder(SegmentsFinder):

    def __init__(self, window_size: int, merge_threshold: float, segment_eps: float, segmentation_size=3):
        if window_size % 2 != 1:
            raise ValueError("Window size must be odd number")

        if segmentation_size > 0 and segmentation_size % 2 != 1:
            raise ValueError("Segmentation size must be odd number")

        self._window_size = window_size
        self._segmentation_size = segmentation_size
        self._merge_threshold = merge_threshold
        self._segment_eps = segment_eps

    def find(self, area: Area):
        points = list(area.get_objects(Point2D))

        if self._segmentation_size > 0:
            segmentation_coordinators = self._perform_segmentation(points)
        else:
            segmentation_coordinators = self._perform_segmentation_simplified(points)

        for coordinator in segmentation_coordinators:
            line = Line2D(p1=Point2D(0, coordinator.entity.offset), slope=coordinator.entity.slope)
            segment_finder = SegmentsInLineFinder()
            segments = segment_finder.find_segments(line, coordinator.entity.points, self._segment_eps)
            for segment in segments:
                area.add_object(Segment, segment)

        return area

    def _perform_segmentation(self, points: List[Point2D]) -> List[LinearRegressionCoordinator]:
        coordinators = self._build_linear_regression_coordinators(points)

        segmentation_coord = []
        merged_coordinator = None
        for i in range(0, len(coordinators)):
            lind = i - (self._segmentation_size - 1) // 2
            if lind < 0:
                lind = 0

            rind = i + (self._segmentation_size - 1) // 2
            if rind >= len(coordinators):
                rind = len(coordinators) - 1

            curr_coordinators = coordinators[lind:rind+1]
            curr_entities = list(map(lambda c: c.entity, curr_coordinators))
            weighted_mean_entity = LinearRegressionEntity.weighted_mean_entity(curr_entities)

            d = 0.0
            for entity in curr_entities:
                d += LinearRegressionEntity.mahalanobis_distance_sqr(entity, weighted_mean_entity)

            if d < self._merge_threshold:
                for coord in curr_coordinators:
                    if merged_coordinator is None:
                        merged_coordinator = coord
                    else:
                        merged_coordinator = merged_coordinator.merge(coord)
            elif merged_coordinator is not None:
                segmentation_coord.append(merged_coordinator)
                merged_coordinator = None

        if merged_coordinator is not None:
            segmentation_coord.append(merged_coordinator)

        return segmentation_coord

    def _perform_segmentation_simplified(self, points: List[Point2D]) -> List[LinearRegressionCoordinator]:
        coordinators = self._build_linear_regression_coordinators(points)

        if len(coordinators) == 0:
            return []

        segmentation_coord = []
        merged_coordinator = coordinators[0]
        for i in range(1, len(coordinators)):
            curr_coord = coordinators[i]

            d = LinearRegressionEntity.mahalanobis_distance_sqr(merged_coordinator.entity, curr_coord.entity)

            if d < self._merge_threshold:
                merged_coordinator = merged_coordinator.merge(curr_coord)
            else:
                segmentation_coord.append(merged_coordinator)
                merged_coordinator = curr_coord

        if merged_coordinator is not None:
            segmentation_coord.append(merged_coordinator)

        return segmentation_coord

    def _build_linear_regression_coordinators(self, points: List[Point2D]) -> List[LinearRegressionCoordinator]:
        coordinators = []
        for i in range(0, len(points) - self._window_size):
            fit_points = points[i:i + self._window_size]
            entity = LinearRegressionEntity(fit_points)
            coordinators.append(LinearRegressionCoordinator(entity=entity, start_index=i))
        return coordinators
