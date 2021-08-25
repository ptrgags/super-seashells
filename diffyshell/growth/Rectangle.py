import numpy

class Rectangle:
    def __init__(self, position, dimensions):
        self.position = position
        self.dimensions = dimensions
        self.midpoint = position + 0.5 * dimensions
    
    def contains(self, point):
        pass

    def intersects(self, other):
        pass

    def get_quadrant(self, point):
        x_bit, y_bit = point >= self.midpoint
        # cast bool -> int
        return int(x_bit) << 1 | int(y_bit)

    def subdivide(self):
        x, y = self.position
        half_dimensions = 0.5 * self.dimensions
        mid_x, mid_y = self.midpoint

        return [
            Rectangle(numpy.array([x, y]), half_dimensions),
            Rectangle(numpy.array([x, mid_y]), half_dimensions),
            Rectangle(numpy.array([mid_x, y]), half_dimensions),
            Rectangle(numpy.array([mid_x, mid_y]), half_dimensions)
        ]