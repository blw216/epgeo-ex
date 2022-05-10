from nearest_neighbor_index import SpatialHash, NearestNeighborIndex
import random

def rand_point() -> tuple:
    return (random.uniform(-1000, 1000), random.uniform(-1000, 1000))

randpts = [rand_point() for _ in range(10000)]

other_pts = [rand_point() for _ in range(100)]

cell_size = 100
spatial_hash = SpatialHash(cell_size)

hashedpts = [spatial_hash.insert_point(pt) for pt in randpts]

print(f"Length of random points: {len(hashedpts)}")
print(f"Length of hash buckets: {len(set(spatial_hash.contents.keys()))}")


nni = NearestNeighborIndex(randpts)
print(f"Length of nni.points: {len(nni.points)}")
nni.build_index()
print(nni.index)

for pt in randpts:
    nn = nni.find_nearest_fast(pt, other_pts)
    print(pt, nn)
