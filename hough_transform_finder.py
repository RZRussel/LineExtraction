import numpy as np
from skimage import transform

from finders import *
from base import Area


class HoughTransformSegmentsFinder(SegmentsFinder):

    def __init__(self, threshold=10, line_length=50, line_gap=10):
        self._threshold = threshold
        self._line_length = line_length
        self._line_gap = line_gap

    def find(self, area: Area) -> Area:
        points = area.get_objects(Point2D)

        segments = self.find_segments_from_points(points)
        for segment in segments:
            area.add_object(Segment, segment)

        return area

    def find_segments_from_points(self, points):
        hough_lines = []
        segments = []
        for start, end in hough_lines:
            segment = Segment(Point2D(start[0], start[1]), Point2D(end[0], end[1]))
            segments.append(segment)

        return segments

    def _find_segments_in_image(self, image: np.array) -> List[tuple]:
        return transform.probabilistic_hough_line(image, self._threshold, self._line_length, self._line_gap)
