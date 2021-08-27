import numpy

from diffyshell.growth.Circle import Circle
from diffyshell.growth.Rectangle import Rectangle

def test_constructs():
    circle = Circle(numpy.array([1.0, 0.0]), 10)
    assert numpy.all(circle.center == numpy.array([1.0, 0.0]))
    assert circle.radius == 10
    assert circle.radius_squared == 100

def test_get_bounding_square():
    circle = Circle(numpy.array([1.0, 0.0]), 10)
    square = circle.get_bounding_square()
    assert isinstance(square, Rectangle)
    assert numpy.all(square.position == numpy.array([-9.0, -10.0]))
    assert numpy.all(square.dimensions == numpy.array([20.0, 20.0]))

def test_contains():
    circle = Circle(numpy.array([1.0, 0.0]), 10)
    assert circle.contains(numpy.array([2.0, 1.0]))
    assert not circle.contains(numpy.array([100.0, 100.0]))