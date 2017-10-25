from core.finders.hough import HoughTransformSegmentsFinder
from core.readers import XYFileAreaReader
from core.visualisers import MatplotlibVisualiser

# Test entry point for development purposes


area = XYFileAreaReader.get_area("example/5.xy")

hough_transform_finder = HoughTransformSegmentsFinder(threshold=1, line_length=10, line_gap=100)
area = hough_transform_finder.find(area)

t = MatplotlibVisualiser()
t.draw(area)