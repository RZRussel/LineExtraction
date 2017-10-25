# LineExtraction
Library, containing implementations of some line extraction algorithms.

* Split and merge (based on RDP)
* Line-regression
* RANSAC
* Hough transofrm

## Warning

Something went wrong and we have inadequate runtimes for the algorithms.
Now we think, that it is related with sympy. For instance, code, creating 600 sympy.Point2D objects with float coordinates takes about 30 seconds!

## Split and merge
Split and merge algorithm works with given polynomial line. Algorithm for line gathering was implemented: it goes point by point from the LIDAR in order, given by LIDAR and connects point in one polynomial line, in case distance between them is less than some given threshold.

For split-and-merge part Ramer-Douglas-Peucker algorithm was used. Implementation was used from rdp pip package. We developed our wrapper for that, linking algorithm to the our project’s structure.

## Line regression

## RANSAC

RANSAC algorithm is based on RANSAC from scikit-image. Obviously, RANSAC in scikit is used to fit one model in data and we can not simply obtain several lines.
That is why we developed an algorithm, which uses RANSAS sequentially. After each iteration inliers of the found line are removed from consideration.

As a stop condition we use:

* Average density of gathered segments is lower than required
* Average length of gathered segments is lower than required
* There are no points left

Also, RANSAC provides us lines, but not segments, and that is why we developed SegmentsInlineFinder, which return segments by given points cloud and lines, returning segments, where points are concentrated.

## Hough transform

Currently, hough transform is based on probabilistic_hough_transform from scikit-image. Drawback is that we have to convert points cloud to the (MxN) matrix, representing image, therefore, we should deal with float number. Currently it is implemented simple converter, converting floats ints by rounding, but, obviously, it is not the best way.

## Authors

* Konstantin Danilov
* Ruslan Rezin