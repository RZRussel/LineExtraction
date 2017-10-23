import unittest
import math
from sympy import Point2D
from lineregression import LinearRegressionEntity


class TestLineRegressionSegmentsFinder(unittest.TestCase):
    pass


class TestLinearRegression(unittest.TestCase):

    def test_linear_entity_init(self):
        points = [Point2D(0, 0), Point2D(1, 1), Point2D(2, 2)]
        entity = LinearRegressionEntity(points)

        self.assertEqual(entity.points, points)
        self.assertAlmostEqual(first=entity._slope, second=math.tan(math.pi/4.0), delta=1e-6)
        self.assertAlmostEqual(first=entity._offset, second=0, delta=1e-6)
        self.assertIsNotNone(entity.covariance)

    def test_singular_mahalanobis_distance_sqr(self):
        points = [Point2D(0, 0), Point2D(1, 1), Point2D(2, 2)]
        entity = LinearRegressionEntity(points)
        d = LinearRegressionEntity.mahalanobis_distance_sqr(entity, entity)
        self.assertAlmostEqual(first=d, second=0.0, delta=1e-6)

    def test_hard_mahalanobis_distance_sqr(self):
        points1 = [Point2D(2, 2), Point2D(2, 5), Point2D(6, 5), Point2D(7, 3), Point2D(4, 7)]
        points2 = [Point2D(6, 5), Point2D(7, 4), Point2D(8, 7), Point2D(5, 6), Point2D(5, 4)]

        entity1 = LinearRegressionEntity(points1)
        entity2 = LinearRegressionEntity(points2)

        d = LinearRegressionEntity.mahalanobis_distance_sqr(entity1, entity2)
        self.assertAlmostEqual(first=d, second=0.543724758, delta=1e-6)

    def test_init_weighted_mean_entity(self):
        points1 = [Point2D(2, 2), Point2D(2, 5), Point2D(6, 5), Point2D(7, 3), Point2D(4, 7)]
        points2 = [Point2D(6, 5), Point2D(7, 4), Point2D(8, 7), Point2D(5, 6), Point2D(5, 4)]

        entity1 = LinearRegressionEntity(points1)
        entity2 = LinearRegressionEntity(points2)

        weighted_mean_entity = LinearRegressionEntity.weighted_mean_entity([entity1, entity2])
        self.assertIsNotNone(weighted_mean_entity.slope)
        self.assertIsNotNone(weighted_mean_entity.offset)
        self.assertIsNotNone(weighted_mean_entity.covariance)

    def test_trivial_weighted_mean_entity(self):
        points = [Point2D(2, 2), Point2D(2, 5), Point2D(6, 5), Point2D(7, 3), Point2D(4, 7)]
        entity = LinearRegressionEntity(points)

        weighted_entity = LinearRegressionEntity.weighted_mean_entity([entity])
        self.assertAlmostEquals(first=entity.slope, second=weighted_entity.slope, delta=1e-6)
        self.assertAlmostEquals(first=entity.offset, second=weighted_entity.offset, delta=1e-6)
