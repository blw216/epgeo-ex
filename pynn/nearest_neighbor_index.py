import math
from pydantic import BaseModel, ValidationError
from typing import *

class ValidPoint(BaseModel):
    """
    This is a Pydantic class to validate the input for NearestNeighborIndex
    and SpatialHash classes.
    """
    points: List[Tuple[float, float]]

class SpatialHash:
    """
    This is a class for creating a spatial hash index using a common
    algorithm typically used for object collision in computer graphics.

    Hash bucket size controlled by cell_size attribute, and must be tuned per
    data set.

    In the case of the points created by rand_point(), the whole number can range
    from -999 to 999,therefore a cell_size of 100 will produce a maximum of
    361 buckets, as the range of potential values produced by
    int(point/cell_size) is -9 <-- 0 --> 9, i.e. 19 total values multiplied by
    19 potential combinations = 361.

    Attributes:
        cell_size (int): the cell and hash partition size
        contents {tuple: list(tuple)}: key values pairs populated by insert_point
        neighbors {tuple: tuple}: Hash partition neighbor lookup table
    """
    def __init__(self, cell_size: int) -> None:
        self.cell_size = cell_size
        self.contents = {}
        self.neighbors = {}

    def _hash(self, point: ValidPoint):
        hash = int(point[0]/self.cell_size), int(point[1]/self.cell_size)
        return hash

    def _find_hash_neighbor(self, idx_point: Tuple[float, float]) -> None:
        min_dist = None
        min_point = None
        for point in self.contents.keys():
            if point != idx_point:
                deltax = point[0] - query_point[0]
                deltay = point[1] - query_point[1]
                dist = math.sqrt((deltax * deltax) + (deltay * deltay))
                pass

    def insert_point(self, point: Tuple[float, float]) -> None:
        print(point, self._hash(point))
        self.contents.setdefault(self._hash(point), []).append(point)


class NearestNeighborIndex:
    """
    This is a class for performing nearest neighbor searches on points.

    Atributes:
        points (tuple(float, float)): The 2D array of points to be indexed.
    """
    def __init__(self, points) -> None:
        """
        Inits NearestNeighborIndex class.
        Takes an array of 2d tuples (float, float) as input points to be indexed.

        :param points: The list of points to be indexed
        :returns: None
        :raises TypeError: Input list must be (float, float)
        """
        self.points = points
        try:
            ValidPoint(points=self.points)
        except ValidationError as e:
            print(e.json())
            raise TypeError("Incorrect data structure. Input must be List[Tuple[float, float]]")

    @staticmethod
    def build_index(method='hash'):
        pass

    @staticmethod
    def find_nearest_naive(query_point: Tuple, haystack: List[Tuple[float, float]]) -> Tuple:
        """
        This naive method returns the point in the haystack that is closest to query_point.

        :param query_point: The origin point from which the closest point will be found
        :param haystack: The list of points to search against
        :returns: Returns the nearest point as a tuple.
        :raises TypeError: Input tuples must be (float, float)
        """

        min_dist = None
        min_point = None

        # For each point in the haystack
        for point in haystack:
            # Calculate the distance between the query point and haystack[i]
            deltax = point[0] - query_point[0]
            deltay = point[1] - query_point[1]
            dist = math.sqrt((deltax * deltax) + (deltay * deltay))
            # If the haystack[i] point is the closest, set min_point
            if min_dist is None or dist < min_dist:
                min_dist = dist
                min_point = point

        return min_point

    def find_nearest_fast(self, query_point):
        """
        TODO comment me.
        """

        return NearestNeighborIndex.find_nearest_naive(query_point, self.points)

        # TODO implement me so this class runs much faster.
        # return self.find_nearest_fast(from_point)
