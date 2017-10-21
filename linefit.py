import sys
import os
import getopt
import utils

K_URG_XY = "urgxy"
K_LONGOPT = [K_URG_XY + "="]


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "", K_LONGOPT)
    except getopt.GetoptError:
        print(usage())
        sys.exit(2)

    if len(args) > 0:
        print(usage())
        sys.exit(2)

    timed_points = None

    for key, value in opts:
        if key == "--" + K_URG_XY:
            try:
                timed_points = utils.parse_urgxy_from_path(value)
            except utils.UtilsException as e:
                print(e.message)
                sys.exit(os.EX_IOERR)

            continue

        print(usage())

    if timed_points is not None:
        print(timed_points)


def usage():
    usage_str = """Usage options:\n\n"""
    usage_str = usage_str + "--" + K_URG_XY + "\t" + "path to URG XY file *.xy\n"
    return usage_str


if __name__ == '__main__':
    main(sys.argv[1:])