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

Line regression implementation based on [paper](https://www.research-collection.ethz.ch/bitstream/handle/20.500.11850/82607/eth-8401-01.pdf) is still in development.
For now simplified version is implemented. It differs from the original one in how windows are merged. In simplified version just
consecutive windows are merged to form one segment if a threshold (see `merged_threshold` parameter) is not exceeded.
Mahalanobis distance is used to compare lines in line model space to make merge decision.
To run simplified algorithm pass `segmentation_size=0` to constructor of the `LineRegressionSegmentsFinder` class.
To customize number of points for each window `window_size` parameter can be setup.
Remained parameter - `segmentation_eps` is used in order to make decision whether segments which lies close should be merged.

## RANSAC

RANSAC algorithm is based on RANSAC from scikit-image. Obviously, RANSAC in scikit is used to fit one model in data and we can not simply obtain several lines.
That is why we developed an algorithm, which uses RANSAC sequentially. After each iteration inliers of the found line are removed from consideration.

As a stop condition we use:

* Average density of gathered segments is lower than required
* Average length of gathered segments is lower than required
* There are no points left

Also, RANSAC provides us lines, but not segments, and that is why we developed SegmentsInlineFinder, which return segments by given points cloud and lines, returning segments, where points are concentrated.

## Hough transform

Currently, hough transform is based on probabilistic_hough_transform from scikit-image. Drawback is that we have to convert points cloud to the (MxN) matrix, representing image, therefore, we should deal with float number. Currently it is implemented simple converter, converting floats ints by rounding, but, obviously, it is not the best way.

## Usage

Please, be sure that you have installed Python 3.5 (or later).

Install required dependencies:

```pip install -r requirements.pip```

To run visualization of the algorithm's work execute corresponding `run_*_finder.py` (e.g. `run_ransac_finder.py`).
Visualization utilizes matplotlib library and in case of problems with its installation please refer to the
official [source](https://matplotlib.org/faq/installing_faq.html).
Datasets extracted from the LIDAR are provided in `example/` directory and can be used for experiments.

To run benchmarking for algorithms in the project directory execute:

```pytest benchmark.py```

## Authors

* Konstantin Danilov
* Ruslan Rezin