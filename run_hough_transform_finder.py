from core.finders.hough import HoughTransformSegmentsFinder
from core.readers import XYFileAreaReader
from core.visualisers import MatplotlibVisualiser

# Test entry point for development purposes


area = XYFileAreaReader.get_area("example/7.xy")

hough_transform_finder = HoughTransformSegmentsFinder(threshold=1, line_length=10, line_gap=150)
area = hough_transform_finder.find(area)

t = MatplotlibVisualiser()
t.draw(area)