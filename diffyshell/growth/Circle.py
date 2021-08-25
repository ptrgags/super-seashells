import numpy
from diffyshell.growth.Rectangle import Rectangle

class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
        self.radius_squared = radius * radius
    
    def get_bounding_square(self):
        r = self.radius
        position = self.center - r
        dimensions = 2 * numpy.array([r])

        return Rectangle(position, dimensions)

    def contains(self, point):
        from_center = point - self.center
        r_sqr = numpy.dot(from_center, from_center)
        return r_sqr < self.radius_squared