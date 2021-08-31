import numpy

from diffyshell.growth.Rectangle import Rectangle
from diffyshell.growth.Quadtree import Quadtree
from diffyshell.growth.Node import Node

BOUNDS = Rectangle(numpy.array([0, 0]), numpy.array([256, 256]))

def node(x, y):
    return Node(numpy.array([x, y]))

def test_constructs():
    quadtree = Quadtree(BOUNDS, 4)
    assert quadtree.bounds == BOUNDS
    assert quadtree.capacity == 4
    assert quadtree.points == []
    assert quadtree.children == []

def test_contains():
    quadtree = Quadtree(BOUNDS, 4)
    assert quadtree.contains(node(0, 0))
    assert quadtree.contains(node(10, 10))
    assert not quadtree.contains(node(-1, -1))
    assert not quadtree.contains(node(256, 256))

def test_is_leaf():
    quadtree = Quadtree(BOUNDS, 2)
    assert quadtree.is_leaf
    quadtree.insert_point(node(10, 0))
    quadtree.insert_point(node(130, 5))
    quadtree.insert_point(node(10, 150))
    assert not quadtree.is_leaf
    assert all(c.is_leaf for c in quadtree.children)

def test_is_empty():
    quadtree = Quadtree(BOUNDS, 2)
    assert quadtree.is_empty
    quadtree.insert_point(node(10, 10))
    assert not quadtree.is_empty

    # once the quadtree subdivides, the parent node should
    # become empty
    quadtree.insert_point(node(130, 5))
    quadtree.insert_point(node(10, 150))
    assert quadtree.is_empty

def test_insert_point():
    # points, one in each quadrant
    point1 = node(10, 10)
    point2 = node(130, 0)
    point3 = node(5, 130)
    point4 = node(200, 200)
    
    # 2 more points in one of the quadrants
    point5 = node(200, 5)
    point6 = node(130, 90)

    # at the beginning the quadtree should be empty
    quadtree = Quadtree(BOUNDS, 2)
    assert quadtree.points == []

    # the first two inserts add to the root cell
    quadtree.insert_point(point1)
    assert quadtree.points == [point1]
    quadtree.insert_point(point2)
    assert quadtree.points == [point1, point2]

    # the third insert will subdivide the root cell
    quadtree.insert_point(point3)
    assert quadtree.points == []
    expected = [[point1], [point3], [point2], []]
    assert [c.points for c in quadtree.children] == expected

    # the fourth insert will put a point in the empty box
    quadtree.insert_point(point4)
    assert quadtree.points == []
    expected = [[point1], [point3], [point2], [point4]]
    assert [c.points for c in quadtree.children] == expected

    # the fifth insert will add a point to the top right box (index 0b10)
    quadtree.insert_point(point5)
    assert quadtree.points == []
    expected = [[point1], [point3], [point2, point5], [point4]]
    assert [c.points for c in quadtree.children] == expected

    # the sixth insert will split the top right box
    quadtree.insert_point(point6)
    assert quadtree.points == []
    expected = [[point1], [point3], [], [point4]]
    assert [c.points for c in quadtree.children] == expected
    top_right = quadtree.children[0b10]
    expected = [[point2], [point6], [point5], []]
    assert [c.points for c in top_right.children] == expected