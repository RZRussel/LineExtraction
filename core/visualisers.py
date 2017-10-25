from typing import List, Dict, Any, Tuple

import matplotlib.pyplot as plt
from sympy import Segment, Point2D

from core.base import Polyline, Area

__author__ = 'Xomak'


class MatplotlibVisualiser:
    STYLE = {
        'segments': {
            'style': 'b',
            'extra': {
                'alpha': 0.4,
                'linewidth': 5
            }
        },
        'polylines': {
            'style': 'g'
        },
        'points': {
            'style': 'ro',
            'extra': {
                'markersize': 5
            }
        }
    }

    def draw_segments(self, segments: List[Segment], style: str, extra_style_params: Dict[str, Any]):
        for segment in segments:
            plt.plot((segment.p1.x, segment.p2.x), (segment.p1.y, segment.p2.y), style, **extra_style_params)

    def draw_polylines(self, polylines: List[Polyline], style: str, extra_style_params: Dict[str, Any]):
        for polyline in polylines:
            if len(polyline.points) > 1:
                self.draw_segments(polyline.get_segments(), style, extra_style_params)

    def draw_points(self, points: List[Point2D], style: str, extra_style_params: Dict[str, Any]):
        points_x = []
        points_y = []

        for point in points:
            points_x.append(point.x)
            points_y.append(point.y)

        plt.plot(points_x, points_y, style, **extra_style_params)

    def get_style_for(self, object_type: str) -> Tuple[str, Dict[str, Any]]:
        dict_rec = self.STYLE[object_type]
        extra = dict_rec['extra'] if 'extra' in dict_rec else {}
        return dict_rec['style'], extra

    def draw(self, area: Area, draw_points=True, draw_polylines=True, draw_segments=True):
        if draw_points:
            point_style, points_kwargs = self.get_style_for('points')
            self.draw_points(area.get_objects(Point2D), point_style, points_kwargs)

        if draw_polylines:
            polylines_style, polylines_kwargs = self.get_style_for('polylines')
            self.draw_polylines(area.get_objects(Polyline), polylines_style, polylines_kwargs)

        if draw_segments:
            segments_style, segments_kwargs = self.get_style_for('segments')
            self.draw_segments(area.get_objects(Segment), segments_style, segments_kwargs)

        plt.show()
