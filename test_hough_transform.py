from sympy import Point2D

from base import Area
from hough_transform_finder import HoughTransformSegmentsFinder
from readers import XYFileAreaReader
from visualisers import MatplotlibVisualiser

# Test entry point for development purposes


area = XYFileAreaReader.get_area("example/7.xy")

hough_transform_finder = HoughTransformSegmentsFinder(threshold=1, line_length=10, line_gap=100)
area = hough_transform_finder.find(area)

t = MatplotlibVisualiser()
t.draw(area)