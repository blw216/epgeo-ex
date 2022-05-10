from nearest_neighbor_index import SpatialHash
import random

def rand_point() -> tuple:
    return (random.uniform(-1000, 1000), random.uniform(-1000, 1000))

randpts = [rand_point() for _ in range(10000)]

cell_size = 100
spatial_hash = SpatialHash(cell_size)

hashedpts = [spatial_hash.insert_point(pt) for pt in randpts]

print(spatial_hash.contents)
print(f"Length of random points: {len(hashedpts)}")
print(f"Length of hash buckets: {len(set(spatial_hash.contents.keys()))}")
