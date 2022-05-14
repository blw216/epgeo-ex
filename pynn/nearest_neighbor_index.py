import math
import collections
import operator
from pydantic import BaseModel, ValidationError
from typing import *

class ValidPoint(BaseModel):
    """
    This is a Pydantic class to valid the input for data structures that require
    a valid tuple of x: float, y: float values.
    """
    point: Tuple[float, float]

class ValidPointsIterable(BaseModel):
    """
    This is a Pydantic class to validate the input for the NearestNeighbor
    class.
    """
    points: List[Tuple[float, float]]

class KDBinaryTree(BaseModel):
    """
    This is a Pydantic class that ducments the base node data structure for
    a binary k-d tree.
    """
    BT = collections.namedtuple("BT", ["value", "left", "right"])

class NNClosestNeighbor(BaseModel):
    """
    This is a Pydantic class to document the data structure for the current
    closest point relative to a given query point in a NN search traversing
    a k-d tree.
    """
    NNRecord = collections.namedtuple("NNRecord", ["point", "distance"])

class SpatialUtils:

    @staticmethod
    def _build_kdtree(points: ValidPointsIterable) -> KDBinaryTree:
        """
        This method defines the binary tree data structure and recursively
        calls 'build' to construct a k-d tree spatial index on the provided
        set of points.

        :param points: Iterable of points as defined by the ValidPointsIterable
        class.
        :returns: K-dimensional binary tree as defined by the KDBinaryTree
        class.
        """

        k = len(points[0])

        BT = collections.namedtuple("BT", ["value", "left", "right"])

        def _build(points: ValidPointsIterable, depth: int):
            """
            This function recursively constructs a k-dimensional tree from a
            given set of points.
            """
            if len(points) == 0:
                return None

            points.sort(key=operator.itemgetter(depth % k))
            middle = len(points) // 2

            return BT(
                value = points[middle],
                left = _build(
                    points=points[:middle],
                    depth=depth+1,
                ),
                right = _build(
                    points=points[middle+1:],
                    depth=depth+1,
                ),
            )

        # Recursively build the k-d tree starting at depth of 0    
        tree = _build(points=list(points), depth=0)
        return tree

    @staticmethod
    def _find_nearest_neighbor_kdtree(tree: KDBinaryTree, point: ValidPoint) -> ValidPoint:
        """Find the nearest neighbor in a k-d tree for a given
        point.
        """
        k = len(point)
        NNRecord = collections.namedtuple("NNRecord", ["point", "distance"])

        best = None
        def _search(tree: KDBinaryTree, depth: int):
            """Recursively search through the k-d tree to find the
            nearest neighbor.
            """
            nonlocal best

            if tree is None:
                return

            distance = SpatialUtils.calculate_distance(tree.value, point)
            if best is None or distance < best.distance:
                best = NNRecord(point=tree.value, distance=distance)

            axis = depth % k
            diff = point[axis] - tree.value[axis]
            if diff <= 0:
                close, away = tree.left, tree.right
            else:
                close, away = tree.right, tree.left

            _search(tree=close, depth=depth+1)
            if diff**2 < best.distance:
                _search(tree=away, depth=depth+1)

        _search(tree=tree, depth=0)
        return best.point

    @staticmethod
    def find_nearest_naive(query_point: ValidPoint, haystack: ValidPointsIterable) -> ValidPoint:
        """
        This naive method returns the point in the haystack that is closest to query_point.
        This method was left unchanged to preserve integrity of the test(s).

        :param query_point: The origin point from which the closest point will be found
        :param haystack: The list of points to search against
        :returns: Returns the nearest point as a tuple.
        :raises TypeError: Input tuples must be (float, float)
        """

        min_dist = None
        min_point = None

        # For each point in the haystack
        for point in haystack:
            if point != query_point:
                # Calculate the distance between the query point and haystack[i]
                deltax = point[0] - query_point[0]
                deltay = point[1] - query_point[1]
                dist = math.sqrt((deltax * deltax) + (deltay * deltay))
                # If the haystack[i] point is the closest, set min_point
                if min_dist is None or dist < min_dist:
                    min_dist = dist
                    min_point = point
        return min_point

    @staticmethod
    def calculate_distance(point1: ValidPoint, point2: ValidPoint) -> float:
        """
        This method calculates the distance between two points.

        :param point1: The first point in a distance calculation.
        :param point2: The second point in a distance calculation.
        :returns: Returns the distance between point1 and point2 as a float.
        """
        return float(sum((i-j)**2 for i, j in zip(point1, point2)))

class NearestNeighbor():
    def __init__(self, points: ValidPointsIterable) -> None:
        self.points = points
    def build_index(self, method: str = "kdtree") -> None:
        if method == "kdtree":
            self.sidx = SpatialUtils()._build_kdtree(self.points)
    def search_index(self, query_point: ValidPoint) -> ValidPoint:
        result = SpatialUtils()._find_nearest_neighbor_kdtree(self.sidx, query_point)
        return result
