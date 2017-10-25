from sympy import Point2D

from base import Area
from lineregression import LineRegressionSegmentsFinder
from readers import XYFileAreaReader
from visualisers import MatplotlibVisualiser

# Test entry point for development purposes


area = XYFileAreaReader.get_area("example/7.xy")

line_regression_finder = LineRegressionSegmentsFinder(window_size=3, merge_threshold=50.0,
                                                      segment_eps=40.0, segmentation_size=0)
area = line_regression_finder.find(area)

t = MatplotlibVisualiser()
t.draw(area)