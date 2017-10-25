from finders import PolylinesFinder, RDPSegmentsFinder, RansacSegmentsFinder
from hough_transform_finder import HoughTransformSegmentsFinder
from lineregression import LineRegressionSegmentsFinder
from readers import XYFileAreaReader

__author__ = 'Xomak'

global_params = {}

def get_area():
    area = XYFileAreaReader.get_area("example/6.xy")
    return area


def rdp(area):
    polylines_finder = PolylinesFinder(epsilon=150)
    area = polylines_finder.find(area)

    rdp_finder = RDPSegmentsFinder(epsilon=20)
    area = rdp_finder.find(area)


def line_regression(area):
    line_regression_finder = LineRegressionSegmentsFinder(window_size=3, merge_threshold=5,
                                                          segment_eps=150, segmentation_size=0)
    area = line_regression_finder.find(area)


def ransac(area):
    ransac_finder = RansacSegmentsFinder(20, 150)
    area = ransac_finder.find(area)


def hough(area):
    hough_transform_finder = HoughTransformSegmentsFinder(threshold=1, line_length=10, line_gap=150)
    area = hough_transform_finder.find(area)


def test_get(benchmark):
    global_params['area'] = benchmark(get_area)


def test_rdp(benchmark):
    benchmark(rdp, global_params['area'])


def test_hough(benchmark):
    benchmark(hough, global_params['area'])


def test_line_regression(benchmark):
    benchmark(line_regression, global_params['area'])


def test_ransac(benchmark):
    benchmark(ransac, global_params['area'])
