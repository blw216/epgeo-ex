import math
from pydantic import BaseModel, ValidationError
from typing import *

class ValidPoints(BaseModel):
    """
    This is a Pydantic class to validate the input for NearestNeighborIndex
    """
    points: List[Tuple[float, float]]

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
            ValidPoints(points=self.points)
        except ValidationError as e:
            print(e.json())
            raise TypeError("Incorrect data structure. Input must be List[Tuple[float, float]]")

    @staticmethod
    def build_index(self):
        pass

    @staticmethod
    def find_nearest_slow(query_point: Tuple, haystack: List[Tuple[float, float]]) -> Tuple:
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

        return NearestNeighborIndex.find_nearest_slow(query_point, self.points)

        # TODO implement me so this class runs much faster.
        # return self.find_nearest_fast(from_point)
