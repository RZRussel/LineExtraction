from sympy import Point2D

from base import Area
from finders import RansacSegmentsFinder
from readers import XYFileAreaReader
from visualisers import MatplotlibVisualiser

# Test entry point for development purposes


area = XYFileAreaReader.get_area("example/7.xy")

ransac_finder = RansacSegmentsFinder(20, 150)
area = ransac_finder.find(area)

t = MatplotlibVisualiser()
t.draw(area)