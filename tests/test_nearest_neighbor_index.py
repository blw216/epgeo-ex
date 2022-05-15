import random
import time
import unittest
import pandas as pd
import os
from pathlib import Path

from pynn import NearestNeighbor, SpatialUtils

# Generally you want unit tests that are self contained but in the name of
# Expediency for this example, I am accesing the example_data CSV's.
this_dir = Path(__file__).parent

class NearestNeighborTest(unittest.TestCase):

    def test_nearest_neighbor_result_accuracy(self):
        """
        This test compares a handful of NN index search results to several
        hard-coded correct values.
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

    def test_speed_benchmark(self):
        """
        This test demonstrates the optimization of the spatial index, and
        asserts that the list of nearest neighbors identified by the
        optimized index search is the same as the list of nearest neighbors
        identified by the brute force approach.
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
        start = time.time()
        uut = NearestNeighbor(index_points).build_index()
        end = time.time()
        print(f"Index time: {(end-start):0.2f}")

        # Run the indexed tests
        start = time.time()
        for query_point in query_points:
            actual.append(uut.search_index(query_point))
        new_time = time.time() - start

        # Assert that the list of actual nn values == expected nn values
        self.assertEqual(expected, actual)
        print(f"Brute force approach time: {slow_time:0.2f}sec")
        print(f"Indexed approach time: {new_time:0.2f}sec")
        print(f"Speedup: {(slow_time / new_time):0.2f}x")

    def test_spatial_example(self):
        # Read in the spatial example data
        user000 = pd.read_csv(os.path.join(this_dir.parent, 'example_data/data_000_track.csv'))
        user179 = pd.read_csv(os.path.join(this_dir.parent, 'example_data/data_179_track.csv'))
        # Lists for storing expected and actual NN results
        expected = []
        actual = []
        # Build the index
        user000_points = list(zip(user000.longitude, user000.latitude))
        user179_points = list(zip(user179.longitude, user179.latitude))
        sidx = NearestNeighbor(user179_points).build_index()
        # Generate the brute force results
        start = time.time()
        for point in user000_points:
            expected.append(SpatialUtils().find_nearest_naive(point, user179_points))
        end = time.time()
        brute_time = end-start
        print(f"Trajectory example brute force time: {brute_time:0.2f}sec")
        start = time.time()
        for point in user000_points:
            actual.append(sidx.search_index(point))
        end = time.time()
        index_time = end-start
        print(f"Trajectory example indexed search time: {index_time:0.2f}sec")
        print(f"Trajectory search speedup: {(brute_time/index_time):0.2f}x")
        self.assertEqual(expected, actual)
