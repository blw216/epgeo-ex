# Example data pulled from Microsoft Research 'Geolife' trajectory data set
# https://www.microsoft.com/en-us/research/publication/geolife-gps-trajectory-dataset-user-guide/

# Activate the environment for this example:
# [~epgeo-ex/]$ source epgenv/bin/activate

from pynn import NearestNeighbor
import pandas as pd

# Read in the trajectory data
user000 = pd.read_csv('../example_data/data_000_track.csv')
user179 = pd.read_csv('../example_data/data_179_track.csv')
print(f"User 000: (Rows: {user000.shape[0]}) | User 010: (Rows: {user179.shape[0]})")

# Build the spatial index on the larger of the two data sets
user179_points = list(zip(user179.longitude, user179.latitude))
user179_sindex = NearestNeighbor(user179_points).build_index()

# For each point in user000, find the nearest point in user010
user000['points'] = list(zip(user000.longitude, user000.latitude))
# user179_nn column contains the point in user179 closest to the provided point
# In each row from user000
user000['user179_nn'] = user000.points.apply(lambda x: user179_sindex.search_index(x))
print(user000.head())
