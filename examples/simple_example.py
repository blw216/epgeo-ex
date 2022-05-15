# Activate the environment for this example:
# [~epgeo-ex/]$ source epgenv/bin/activate

from pynn import NearestNeighbor
import pandas as pd

# Read in the trajectory data
user000 = pd.read_csv('../example_data/data_000_track.csv')
user010 = pd.read_csv('../example_data/data_010_track.csv')
print(f"User 000: (Rows: {user000.shape[0]}) | User 010: (Rows: {user010.shape[0]})")

# Build the spatial index on the larger of the two data sets
user010_points = list(zip(user010.longitude, user010.latitude))
user010_sindex = NearestNeighbor(user010_points).build_index()

# For each point in user000, find the nearest point in user010
user000['points'] = list(zip(user000.longitude, user000.latitude))
user000['user010_nn'] = user000.points.apply(lambda x: user010_sindex.search_index(x))
print(user000.head())
