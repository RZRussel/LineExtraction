from typing import List

import numpy as np
from skimage.measure import ransac, LineModelND
from sympy import Point2D, Segment, Line

from core.base import Area
from core.finders.base import SegmentsFinder
from core.finders.segments import SegmentsInLineFinder

__author__ = 'Xomak'


class RansacSegmentsFinder(SegmentsFinder):
    """
    RANSAC segments finder. Currently it does not support segments, parallel to Y-axis.
    """

    def __init__(self, residual_threshold, segments_threshold, max_trials=1000,
                 density_threshold=None, length_threshold=None):
        """
        Inits finder
        :param residual_threshold: Residual threshold for RANSAC
        :param segments_threshold: Maximal distance between points in one line to be considered as one segment
        :param max_trials: Max trials for one RANSAC
        :param density_threshold: Threshold for new segments finder (if previous segment's density is less
        than this value, process will be stopped)
        :param length_threshold: Threshold for new segments finder (if previous segment's length is less
        than this value, process will be stopped)
        """
        self.length_threshold = length_threshold
        self.density_threshold = density_threshold
        self.max_trials = max_trials
        self.segments_threshold = segments_threshold
        self.residual_threshold = residual_threshold

    def find(self, area: Area) -> Area:
        points = area.get_objects(Point2D)
        segments = self.find_segments_in_points(points)
        for segment in segments:
            area.add_object(Segment, segment)
        return area

    def find_segments_in_points(self, points: List[Point2D]) -> List[Segment]:
        np_points = np.ndarray((len(points), 2))

        segments = []

        for idx, point in enumerate(points):
            np_points[idx, 0] = point.x
            np_points[idx, 1] = point.y

        is_density_valid = True
        is_length_valid = True

        while len(np_points) > 2 \
                and (self.density_threshold is None or is_density_valid) \
                and (self.length_threshold is None or is_length_valid):

            model_robust, inliers_mask = ransac(np_points, LineModelND, min_samples=2,
                                                residual_threshold=self.residual_threshold, max_trials=self.max_trials)

            inliers = np_points[inliers_mask]

            line_params = model_robust.params

            origin = Point2D(line_params[0][0], line_params[0][1])
            direction = Point2D(line_params[1][0], line_params[1][1])

            line = Line(origin, origin + direction)
            points = [Point2D(point[0], point[1]) for point in inliers]
            found_segments = SegmentsInLineFinder.find_segments_with_density(line, points, 150)
            current_segments = []
            densities = []
            lengths = []

            for found_segment in found_segments:
                current_segments.append(found_segment.segment)
                densities.append(found_segment.density)
                lengths.append(found_segment.segment.length)

            if len(densities) > 0:
                avg_density = np.mean(densities)
                avg_length = np.mean(lengths)
                if self.density_threshold:
                    is_density_valid = avg_density > self.density_threshold
                if self.length_threshold:
                    is_length_valid = avg_length > self.length_threshold
            else:
                is_density_valid = False
                is_length_valid = False

            segments += current_segments

            np_points = np_points[~inliers_mask]

        return segments