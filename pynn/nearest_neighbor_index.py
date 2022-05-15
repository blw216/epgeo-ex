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
    """
    This class contains several static methods that are spatial utilities.
    """
    @staticmethod
    def _build_kdtree(points: ValidPointsIterable) -> KDBinaryTree:
        """
        This method defines the binary tree data structure and recursively
        calls the 'build' method to construct a k-d tree spatial index on the
        provided set of points.

        :param points: Iterable of points as defined by the ValidPointsIterable
        class.
        :returns: K-dimensional binary tree as defined by the KDBinaryTree
        class.
        """

        k = len(points[0])
        BT = collections.namedtuple("BT", ["value", "left", "right"])

        def _build(points: ValidPointsIterable, depth: int):
            """
            Recursively construct a k-dimensional tree from a given set of points.
            """
            if len(points) == 0:
                return None

            points.sort(key=operator.itemgetter(depth % k))
            middle = len(points) // 2
            BTNode = BT(
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
            return BTNode

        # Recursively build the k-d tree starting at depth of 0
        tree = _build(points=list(points), depth=0)
        return tree

    @staticmethod
    def _find_nearest_neighbor_kdtree(tree: KDBinaryTree,
                                        point: ValidPoint) -> ValidPoint:
        """
        PRIVATE - Find the nearest neighbor in a k-d tree for a given point.
        """
        k = len(point)
        NNRecord = collections.namedtuple("NNRecord", ["point", "distance"])

        best = None
        def _search(tree: KDBinaryTree, depth: int):
            """Recursively search through the k-d tree to find the
            nearest neighbor.
            """
            # Need to access 'best' out of _search scope
            nonlocal best

            if tree is None:
               return None

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
    def find_nearest_naive(query_point: ValidPoint,
                            haystack: ValidPointsIterable) -> ValidPoint:
        """
        This brute force method returns the point in the haystack that is
        closest to query_point. This method was left unchanged - other than
        type hinting - to preserve integrity of the test(s).

        :param query_point: The origin point from which the closest point will
        be searched for.
        :param haystack: The list of points to search against
        :param validate: Boolean to determine input type validation. Causes
        performance degradation.
        :returns: Returns the nearest point as a tuple.
        :raises TypeError: Input tuples must be (float, float)
        """

        # Initialize minimum point and distance variables
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
        # Validate the input points
        try:
            point1 = ValidPoint(point=point1)
            point2 = ValidPoint(point=point2)
            point1 = point1.point
            point2 = point2.point
        except ValidationError as e:
            print(e.json())
        # Calculate and return the distance between two points
        return float(sum((i-j)**2 for i, j in zip(point1, point2)))

class NearestNeighbor:
    """
    This class constructs a NearestNeighbor object from which an iterable
    of points can be ingested, validated, and indexed using a kd-tree spatial
    index for performant nearest neighbor queries.

    Attributes:
        points (ValidPointsIterable): the points that will be indexed.
    """
    def __init__(self, points) -> None:
        """
        Initializes the NearestNeighbor class. performs input type validation
        using the ValidPointsIterable Pydantic class.

        :param points: The iterable of ValidPoint objects
        :returns: None
        :raises ValidationError: Input iterable must consist of [ValidPoint, ...]
        """
        # Validate the points iterable input
        try:
            points = ValidPointsIterable(points=points)
            self.points = points.points
        except ValidationError as e:
            print(e.json())

    def build_index(self, method: str = "kdtree") -> None:
        """
        This method builds the spatial index on the NearestNeighbor points
        attribute, using a kd-tree method.

        :param method: A string value declaring the spatial index method to be
        used. Future extensions of this class may include more spatial indexing
        methods.
        :returns: self
        """
        valid_methods = ['kdtree']
        if method not in valid_methods:
            raise ValueError(f"Error: sidx_type must be in ({valid_methods})")
        else:
            self.sidx_method = method
        if self.sidx_method == 'kdtree':
            self.sidx = SpatialUtils()._build_kdtree(self.points)
        return self

    def search_index(self, query_point: ValidPoint) -> ValidPoint:
        """
        This method searches the spatial index created by build_index and
        returns the nearest neighbor in the index to the input query_point.

        :param query_point: ValidPoint object from which to find the NN in the index
        """
        try:
            query_point = ValidPoint(point=query_point)
            query_point = query_point.point
        except ValidationError as e:
            print(e.json())
        result = SpatialUtils()._find_nearest_neighbor_kdtree(self.sidx, query_point)
        return result
