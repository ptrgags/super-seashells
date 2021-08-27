import numpy

from diffyshell.growth.Rectangle import Rectangle


def test_constructs():
    position = numpy.array([10.0, 10.0])
    dimensions = numpy.array([100.0, 100.0])
    rect = Rectangle(position, dimensions)
    assert numpy.all(rect.position == position)
    assert numpy.all(rect.dimensions == dimensions)
    assert numpy.all(rect.midpoint == numpy.array([60.0, 60.0]))

def test_repr():
    position = numpy.array([10.0, 2.0])
    dimensions = numpy.array([50.0, 100.0])
    rect = Rectangle(position, dimensions)
    assert repr(rect) == "Rectangle (10.0, 2.0, 50.0, 100.0)"

def test_contains():
    position = numpy.array([10.0, 10.0])
    dimensions = numpy.array([100.0, 100.0])
    rect = Rectangle(position, dimensions)
    assert rect.contains(numpy.array([50.0, 50.0]))
    assert rect.contains(numpy.array([10.0, 10.0]))
    assert rect.contains(numpy.array([20.0, 10.0]))
    assert not rect.contains(numpy.array([0.0, 0.0]))
    assert not rect.contains(numpy.array([110.0, 110.0]))
    assert not rect.contains(numpy.array([50.0, 110.0]))
    assert not rect.contains(numpy.array([-100.0, 20.0]))

def test_intersects():
    rect1 = Rectangle(numpy.array([0.0, 0.0]), numpy.array([10.0, 10.0]))
    assert rect1.intersects(rect1)

    rect2 = Rectangle(numpy.array([5.0, 0.0]), numpy.array([8.0, 20.0]))
    assert rect1.intersects(rect2)
    assert rect2.intersects(rect1)

    rect3 = Rectangle(numpy.array([-10, -10]), numpy.array([5.0, 5.0]))
    assert not rect3.intersects(rect1)
    assert not rect1.intersects(rect3)

def test_get_quadrant():    
    rect = Rectangle(numpy.array([0.0, 0.0]), numpy.array([128.0, 256.0]))
    assert rect.get_quadrant(numpy.array([0.0, 0.0])) == 0b00
    assert rect.get_quadrant(numpy.array([70.0, 30.0])) == 0b10
    assert rect.get_quadrant(numpy.array([30.0, 140.0])) == 0b01
    assert rect.get_quadrant(numpy.array([70.0, 140.0])) == 0b11
    assert rect.get_quadrant(numpy.array([64.0, 128.0])) == 0b11

def test_subdivide():
    rect = Rectangle(numpy.array([0.0, 0.0]), numpy.array([128.0, 256.0]))
    children = rect.subdivide()
    half_dimensions = numpy.array([64.0, 128.0])
    expected = [
        Rectangle(numpy.array([0.0, 0.0]), half_dimensions),
        Rectangle(numpy.array([0.0, 128.0]), half_dimensions),
        Rectangle(numpy.array([64.0, 0.0]), half_dimensions),
        Rectangle(numpy.array([64.0, 128.0]), half_dimensions)
    ]
    for i in range(4):
        assert children[i] == expected[i]