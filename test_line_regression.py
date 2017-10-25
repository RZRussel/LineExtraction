from core.finders.lineregression import LineRegressionSegmentsFinder
from core.readers import XYFileAreaReader
from core.visualisers import MatplotlibVisualiser

# Test entry point for development purposes


area = XYFileAreaReader.get_area("example/7.xy")

line_regression_finder = LineRegressionSegmentsFinder(window_size=9, merge_threshold=1.0,
                                                      segment_eps=40.0, segmentation_size=0)
area = line_regression_finder.find(area)

t = MatplotlibVisualiser()
t.draw(area)