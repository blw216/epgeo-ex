"""nn_search_test"""

import random
import time
import unittest

from pynn import NearestNeighbor, SpatialUtils

class NearestNeighborTest(unittest.TestCase):

    def test_basic(self):
        """
        test_basic tests a handful of nearest neighbor queries to make sure they return the right
        result.
        """

        test_points = [
            (1, 2),
            (1, 0),
            (10, 5),
            (-1000, 20),
            (3.14159, 42),
            (42, 3.14159),
        ]

        uut = NearestNeighbor(test_points).build_index()

        self.assertEqual((1, 0), uut.search_index((0, 0)))
        self.assertEqual((-1000, 20), uut.search_index((-2000, 0)))
        self.assertEqual((42, 3.14159), uut.search_index((40, 3)))

    def test_benchmark(self):
        """
        test_benchmark tests a bunch of values using the slow and fast version of the index
        to determine the effective speedup.
        """

        def rand_point(): return (random.uniform(-1000, 1000), random.uniform(-1000, 1000))

        index_points = [rand_point() for _ in range(10000)]
        query_points = [rand_point() for _ in range(1000)]

        expected = []
        actual = []

        # Run the baseline slow tests to get the expected values.
        start = time.time()
        for query_point in query_points:
            expected.append(SpatialUtils().find_nearest_naive(query_point, index_points))
        slow_time = time.time() - start

        # Don't include the indexing time when benchmarking
        uut = NearestNeighbor(index_points).build_index()

        # Run the indexed tests
        start = time.time()
        for query_point in query_points:
            actual.append(uut.search_index(query_point))
        new_time = time.time() - start

        print(f"slow time: {slow_time:0.2f}sec")
        print(f"new time: {new_time:0.2f}sec")
        print(f"speedup: {(slow_time / new_time):0.2f}x")
        self.assertEqual(expected, actual)
