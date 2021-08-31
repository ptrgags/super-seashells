import numpy

from diffyshell.growth.Node import Node

def test_constructs():
    position = numpy.array([0, 0])
    node = Node(position)
    assert numpy.all(node.position == position)
    assert numpy.all(node.velocity == numpy.array([0, 0]))
    assert numpy.all(node.acceleration == numpy.array([0, 0]))
    assert node.mass == 1.0
    assert node.quadtree_node == None
    assert node.is_dirty == False

def test_repr():
    node = Node(numpy.array([3, 4]))
    assert repr(node) == "Node (3, 4)"

def test_apply_forces():
    node = Node(numpy.array([0, 0], dtype=numpy.float64))
    net_force = numpy.array([2.0, 4.0])
    delta_time = 0.5
    node.apply_forces(net_force, delta_time)
    assert numpy.all(node.acceleration == numpy.array([2.0, 4.0]))
    assert numpy.all(node.velocity == numpy.array([1.0, 2.0]))
    assert numpy.all(node.position == numpy.array([0.5, 1.0]))