from typing import Dict, List

from sympy import Point2D

from core.base import Area

__author__ = 'Xomak'


class XYFileReader:

    @staticmethod
    def get_data(file_path) -> Dict[int, List[Point2D]]:
        timed_points = {}
        with open(file_path, 'r') as file:
            for line in file.readlines():
                timestamp, points = XYFileReader.parse_file_line(line)
                timed_points[timestamp] = points
        return timed_points

    @staticmethod
    def parse_file_line(string):
        comps = string.split(":")

        if len(comps) != 2:
            raise IOError("Undefined urgxy format: 'timestamp: list' expected")

        try:
            timestamp = int(comps[0])
        except ValueError:
            raise IOError("Timestamp should has int type")

        points_list = []
        points_comps = comps[1].strip(" ,\t\n").split(",")
        for point_str in points_comps:
            point_comps = point_str.strip(" ()").split(";")
            if len(point_comps) != 3:
                raise IOError("Undefined urgxy format: (x;y;z) list expected but received " + point_comps)
            points_list.append(Point2D(float(point_comps[0]), float(point_comps[1])))

        return timestamp, points_list


class XYFileAreaReader(XYFileReader):

    @staticmethod
    def get_area(file_path, ignore_zero_point=True, merge_duplicates=True):
        timestamped_points_lists = XYFileReader.get_data(file_path)
        if len(timestamped_points_lists) != 1:
            raise NotImplemented("Area construction is not supported for files with not one instance of data")

        area = Area()
        timestamped_points = next(iter(timestamped_points_lists.values()))

        previous_point = None
        zero_point = Point2D(0, 0)

        for point in timestamped_points:
            if (not merge_duplicates or point != previous_point) and (not ignore_zero_point or point != zero_point):
                area.add_object(Point2D, point)
            previous_point = point

        return area
