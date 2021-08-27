import numpy

class Rectangle:
    def __init__(self, position, dimensions):
        self.position = position
        self.dimensions = dimensions
        self.midpoint = position + 0.5 * dimensions
    
    def __repr__(self):
        x, y = self.position
        w, h = self.dimensions
        return f"Rectangle ({x}, {y}, {w}, {h})"

    def __eq__(self, other):
        positions_match = numpy.all(self.position == other.position)
        dimensions_match = numpy.all(self.dimensions == other.dimensions)
        return positions_match and dimensions_match

    def contains(self, point):
        min_condition = point >= self.position
        max_condition = point < (self.position + self.dimensions)
        return numpy.all(min_condition & max_condition)

    def intersects(self, other):
        left, top = self.position
        right, bottom = self.position + self.dimensions

        other_left, other_top = other.position
        other_right, other_bottom = other.position + other.dimensions

        if left > other_right or other_left > right:
            return False
        
        if top > other_bottom or other_top > bottom:
            return False

        return True
        
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