from sympy import Point2D

from core.base import Area
from core.finders.ransac import RansacSegmentsFinder
from core.readers import XYFileAreaReader
from core.visualisers import MatplotlibVisualiser

# Test entry point for development purposes


area = XYFileAreaReader.get_area("example/7.xy")

ransac_finder = RansacSegmentsFinder(20, 150)
area = ransac_finder.find(area)

t = MatplotlibVisualiser()
t.draw(area)