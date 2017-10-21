class UtilsException(Exception):
    def __init__(self, message):
        self.message = message


def parse_urgxy_from_path(path):
    timed_points = {}
    with open(path, 'r') as file:
        for line in file.readlines():
            timestamp, points = parse_urgxy_from_str(line)
            timed_points[timestamp] = points
    return timed_points


def parse_urgxy_from_str(str):
    comps = str.split(":")
    if len(comps) != 2:
        raise UtilsException("Undefined urgxy format: 'timestamp: list' expected")

    timestamp = float(comps[0])

    points_list = []
    points_comps = comps[1].strip(" ,\t\n").split(",")
    for point_str in points_comps:
        point_comps = point_str.strip(" ()").split(";")
        if len(point_comps) != 3:
            raise UtilsException("Undefined urgxy format: (x;y;z) list expected but received " + point_comps)
        points_list.append((float(point_comps[0]), float(point_comps[1])))

    return timestamp, points_list

