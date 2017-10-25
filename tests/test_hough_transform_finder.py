import unittest
import numpy as np
from hough_transform_finder import HoughTransformSegmentsFinder


class TestHoughTransformFinder(unittest.TestCase):

    def test_find_segments_from_points(self):
        img = np.zeros((100, 100))

        for i in range(0, 20):
            img[0][i] = 1
            img[i][0] = 1
            img[19][i] = 1
            img[i][19] = 1

        hough_transform_finder = HoughTransformSegmentsFinder(line_length=10)
        hough_lines = hough_transform_finder._find_segments_in_image(img)

        self.assertEqual(len(hough_lines), 4)
