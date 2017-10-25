from skimage import transform
from converters import PointsToImageRoundBasedConverter

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

    def find_segments_from_points(self, points: List[Point2D]) -> List[Segment]:
        points_converter = PointsToImageRoundBasedConverter(min_precision=0.0)
        image, image_converter = points_converter.convert(points)

        hough_lines = self._find_segments_in_image(image)
        segments = []
        for start, end in hough_lines:
            start_point = image_converter.convert(Point2D(start[0], start[1]))
            end_point = image_converter.convert(Point2D(end[0], end[1]))
            segment = Segment(start_point, end_point)
            segments.append(segment)

        return segments

    def _find_segments_in_image(self, image: np.array) -> List[tuple]:
        return transform.probabilistic_hough_line(image, self._threshold, self._line_length, self._line_gap)
