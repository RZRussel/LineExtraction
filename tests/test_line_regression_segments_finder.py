import unittest
import math
from sympy import Point2D
from lineregression import LinearRegressionEntity, LinearRegressionCoordinator, LineRegressionSegmentsFinder


class TestLineRegressionSegmentsFinder(unittest.TestCase):

    def test_horizontal_segmentation(self):
        points = []

        for i in range(0, 20):
            points.append(Point2D(i * 0.1, 0.0))

        finder = LineRegressionSegmentsFinder(7, 3, 0.5, 0.5)
        entities = finder._perform_segmentation(points)
        self.assertEqual(len(entities), 1)

    def test_vertical_segmentation(self):
        points = []

        for i in range(0, 20):
            points.append(Point2D(i * 0.1, 0.0))

        finder = LineRegressionSegmentsFinder(7, 3, 0.5, 0.5)
        entities = finder._perform_segmentation(points)
        self.assertEqual(len(entities), 1)

    def test_one_segment_segmentation(self):
        points = []

        for i in range(0, 20):
            points.append(Point2D(i * 0.1, i * 0.2))

        finder = LineRegressionSegmentsFinder(7, 3, 0.5, 0.5)
        entities = finder._perform_segmentation(points)
        self.assertEqual(len(entities), 1)

    def test_square_segmentation(self):
        points = []

        for i in range(0, 20):
            points.append(Point2D(i*0.1, 0.0))
        for i in range(0, 20):
            points.append(Point2D(2.0 + i*0.1, i*0.1))
        for i in range(0, 20):
            points.append(Point2D(4.0 - i*0.1, 2.0))
        for i in range(0, 20):
            points.append(Point2D(2.0 - i*0.1, 2.0 - i * 0.1))

        finder = LineRegressionSegmentsFinder(7, 3, 0.5, 0.5)
        entities = finder._perform_segmentation(points)
        self.assertEqual(len(entities), 4)


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


class TestLinearRegressionCoordination(unittest.TestCase):

    def test_init(self):
        points = [Point2D(6, 5), Point2D(7, 4), Point2D(8, 7), Point2D(5, 6), Point2D(5, 4)]
        entity = LinearRegressionEntity(points)
        coordinator = LinearRegressionCoordinator(entity, 10)

        self.assertEqual(first=entity, second=coordinator.entity)
        self.assertEqual(first=coordinator.start_index, second=10)

    def test_can_merge_false(self):
        points1 = [Point2D(6, 5), Point2D(7, 4), Point2D(8, 7), Point2D(5, 6), Point2D(5, 4)]
        entity1 = LinearRegressionEntity(points1)
        coordinator1 = LinearRegressionCoordinator(entity1, 2)

        points2 = [Point2D(6, 5), Point2D(7, 4), Point2D(8, 7), Point2D(5, 6), Point2D(5, 4)]
        entity2 = LinearRegressionEntity(points2)
        coordinator2 = LinearRegressionCoordinator(entity2, 8)

        self.assertFalse(coordinator2.can_merge(coordinator1))

    def test_can_merge_true(self):
        points1 = [Point2D(6, 5), Point2D(7, 4), Point2D(8, 7), Point2D(5, 6), Point2D(5, 4)]
        entity1 = LinearRegressionEntity(points1)
        coordinator1 = LinearRegressionCoordinator(entity1, 2)

        points2 = [Point2D(6, 5), Point2D(7, 4), Point2D(8, 7), Point2D(5, 6), Point2D(5, 4)]
        entity2 = LinearRegressionEntity(points2)
        coordinator2 = LinearRegressionCoordinator(entity2, 5)

        self.assertTrue(coordinator2.can_merge(coordinator1))

    def test_merge_intersected(self):
        points1 = [Point2D(6, 5), Point2D(7, 4), Point2D(8, 7), Point2D(5, 6), Point2D(5, 4)]
        entity1 = LinearRegressionEntity(points1)
        coordinator1 = LinearRegressionCoordinator(entity1, 2)

        points2 = [Point2D(6, 5), Point2D(7, 4), Point2D(8, 7), Point2D(5, 6), Point2D(5, 4)]
        entity2 = LinearRegressionEntity(points2)
        coordinator2 = LinearRegressionCoordinator(entity2, 6)

        coordinator = coordinator2.merge(coordinator1)

        self.assertEqual(first=coordinator.start_index, second=2)
        self.assertEqual(first=len(coordinator.entity.points), second=9)

    def test_merge_separated(self):
        points1 = [Point2D(6, 5), Point2D(7, 4), Point2D(8, 7), Point2D(5, 6), Point2D(5, 4)]
        entity1 = LinearRegressionEntity(points1)
        coordinator1 = LinearRegressionCoordinator(entity1, 2)

        points2 = [Point2D(6, 5), Point2D(7, 4), Point2D(8, 7), Point2D(5, 6), Point2D(5, 4)]
        entity2 = LinearRegressionEntity(points2)
        coordinator2 = LinearRegressionCoordinator(entity2, 7)

        coordinator = coordinator2.merge(coordinator1)

        self.assertEqual(first=coordinator.start_index, second=2)
        self.assertEqual(first=len(coordinator.entity.points), second=10)

    def test_merge_same(self):
        points1 = [Point2D(6, 5), Point2D(7, 4), Point2D(8, 7), Point2D(5, 6), Point2D(5, 4)]
        entity1 = LinearRegressionEntity(points1)
        coordinator1 = LinearRegressionCoordinator(entity1, 2)

        points2 = [Point2D(6, 5), Point2D(7, 4), Point2D(8, 7), Point2D(5, 6), Point2D(5, 4)]
        entity2 = LinearRegressionEntity(points2)
        coordinator2 = LinearRegressionCoordinator(entity2, 2)

        coordinator = coordinator2.merge(coordinator1)

        self.assertEqual(first=coordinator.start_index, second=2)
        self.assertEqual(first=len(coordinator.entity.points), second=5)
