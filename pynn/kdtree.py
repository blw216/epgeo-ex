import collections
import operator

BT = collections.namedtuple("BT", ["value", "left", "right"])
BT.__doc__ = """
A Binary Tree (BT) with a node value, and left- and
right-subtrees.
"""
NNRecord = collections.namedtuple("NNRecord", ["point", "distance"])
NNRecord.__doc__ = """
Used to keep track of the current best guess during a nearest
neighbor search."""

def SED(X, Y):
    """Compute the squared Euclidean distance between X and Y."""
    return sum((i-j)**2 for i, j in zip(X, Y))

def kdtree(points):
    """Construct a k-d tree from an iterable of points.

    This algorithm is taken from Wikipedia. For more details,

    > https://en.wikipedia.org/wiki/K-d_tree#Construction

    """
    k = len(points[0])

    def build(*, points, depth):
        """Build a k-d tree from a set of points at a given
        depth.
        """
        if len(points) == 0:
            return None

        points.sort(key=operator.itemgetter(depth % k))
        middle = len(points) // 2

        return BT(
            value = points[middle],
            left = build(
                points=points[:middle],
                depth=depth+1,
            ),
            right = build(
                points=points[middle+1:],
                depth=depth+1,
            ),
        )

    return build(points=list(points), depth=0)

def find_nearest_neighbor(tree, point):
    """Find the nearest neighbor in a k-d tree for a given
    point.
    """
    k = len(point)

    best = None
    def search(*, tree, depth):
        """Recursively search through the k-d tree to find the
        nearest neighbor.
        """
        nonlocal best

        if tree is None:
            return

        distance = SED(tree.value, point)
        if best is None or distance < best.distance:
            best = NNRecord(point=tree.value, distance=distance)

        axis = depth % k
        diff = point[axis] - tree.value[axis]
        if diff <= 0:
            close, away = tree.left, tree.right
        else:
            close, away = tree.right, tree.left

        search(tree=close, depth=depth+1)
        if diff**2 < best.distance:
            search(tree=away, depth=depth+1)

    search(tree=tree, depth=0)
    return best.point
