from nearest_neighbor_index import NearestNeighbor, SpatialUtils
import random
import time
import numpy as np

def rand_point() -> tuple:
    return (random.uniform(-1000, 1000), random.uniform(-1000, 1000))

querypts = [rand_point() for _ in range(1000)]
haystack = [rand_point() for _ in range(1000)]

start = time.time()
slow_results = []
for pt in querypts:
    slow = SpatialUtils.find_nearest_naive(pt, haystack)
    slow_results.append(slow)
end = time.time()
slow_time = end-start
print(f"Slow: {slow_time}")

nns = NearestNeighbor(haystack)
nns.build_index()

start=time.time()
fast_results = []
for pt in querypts:
    fast = nns.search_index(pt)
    fast_results.append(fast)
end=time.time()
fast_time=end-start
print(f"fast: {fast_time}")
print(f"fast/slow array equality: {np.array_equal(np.array(slow_results), np.array(fast_results))}")
print(f"Speedup: {slow_time/fast_time:0.2f}")
