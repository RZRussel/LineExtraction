from sympy import Point2D

from core.base import Area
from core.finders.polylines import PolylinesFinder
from core.finders.rdp import RDPSegmentsFinder
from core.readers import XYFileAreaReader
from core.visualisers import MatplotlibVisualiser

# Test entry point for development purposes


def get_square_area():
    top = [Point2D(x, 0) for x in range(0, 5)]
    right = [Point2D(4, y) for y in range(1, 5)]
    bottom = [Point2D(x, 4) for x in range(3, 0, -1)]
    left = [Point2D(0, y) for y in range(4, 0, -1)]
    square = top + right + bottom + left

    area = Area()
    for point in square:
        area.add_object(Point2D, point)

    return area

area = XYFileAreaReader.get_area("example/7.xy")

polylines_finder = PolylinesFinder(epsilon=150)
area = polylines_finder.find(area)

rdp_finder = RDPSegmentsFinder(epsilon=20)
area = rdp_finder.find(area)

t = MatplotlibVisualiser()
t.draw(area)
