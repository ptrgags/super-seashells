def partition(array, condition):
    true_list = []
    false_list = []
    for x in array:
        if condition:
            true_list.append(x)
        else:
            false_list.append(x)
    return (true_list, false_list)

class Quadtree:
    def __init__(self, bounds, capacity):
        self.bounds = bounds
        self.capacity = capacity
        self.points = []

        # either 0 or 4 children. If 4, they are ordered
        # by quadrant. See Rectangle.get_quadrant(point)
        self.children = []
    
    def contains(self, point):
        return self.bounds.contains(point.position)
    
    @property
    def is_leaf(self):
        return self.children.length == 0
    
    @property
    def is_empty(self):
        return self.points.length == 0
    
    def insert_point(self, point):
        if not self.contains(point):
            raise RuntimeError(f"Out of bounds: {point}")
        
        if self.is_leaf:
            point.quadtree_node = self
            self.points.push(point)

            if self.points.length > self.capacity:
                self.subdivide()
        else:
            quadrant = self.bounds.get_quadrant(point.position)
            self.children[quadrant].insert_point(point)
    
    def subdivide(self):
        children_bounds = self.bounds.subdivide()
        self.children = [
            Quadtree(bounds, self.capacity) 
            for bounds in children_bounds]
        
        for point in self.points:
            quadrant = self.bounds.get_quadrant(point.position)
            self.children[quadrant].insert_point(point)
        
        self.points = []

    def redistribute_dirty_points(self):
        if self.is_leaf:
            [dirty_points, clean_points] = partition(
                self.points, lambda x: x.is_dirty)
            self.points = clean_points
            return dirty_points
        
        empty_count = 0
        child_dirty_list = []
        for child in self.children:
            child_dirty_points = child.redistribute_dirty_points()
            child_dirty_list.extend(child_dirty_points)

            if child.is_empty:
                empty_count += 1

        outside_parent_list = []
        for point in child_dirty_list:
            if self.bounds.contains(point.position):
                point.is_dirty = False
                self.insert_point(point)
            else:
                outside_parent_list.append(point)

        # If all the points moved out of the parent, remove the child
        # cells
        if empty_count == 4:
            self.children = []
        
        # propagate points we weren't able to redistribute
        return outside_parent_list

    def circle_query(self, circle):
        square = circle.get_bounding_square()
        points = self.rectangle_query(square)
        return [p for p in points if circle.contains(p.position)]
    
    def rectangle_query(self, rectangle):
        if self.is_leaf:
            return [p for p in self.points if rectangle.contains(p.position)]
        
        child_points = []
        for child in self.children:
            if rectangle.intersects(child.bounds):
                quadrant_points = child.rectangle_query(rectangle)
                child_points.extend(quadrant_points)
        
        return child_points