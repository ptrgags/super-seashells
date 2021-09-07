import random

import numpy

from diffyshell.growth.Node import Node
from diffyshell.growth.Circle import Circle

MAX_EDGE_LENGTH_SQR = 150 * 150
PINCH_THRESHOLD = numpy.cos(numpy.pi / 4)
ATTRACTION_MIN_DIST_SQR = 20 * 20
MAX_SPEED = 10
MAX_FORCE = 20
NEARBY_RADIUS = 20

def limit(vector, maximum):
    old_length = numpy.linalg.norm(vector)
    new_length = min(old_length, maximum)
    if old_length > 0:
        return vector * new_length / old_length
    return vector

def normalize(vector):
    length = numpy.linalg.norm(vector)
    if length > 0:
        return vector / length
    return vector

def set_magnitude(vector, magnitude):
    return normalize(vector) * magnitude

class DifferentialPolygon:
    def __init__(self, initial_positions, quadtree):
        self.nodes = [Node(position) for position in initial_positions]
        self.growth_indices = set()

        self.iters = 0

        # rates are measured in frames
        self.growth_rate = 200
        self.stretch_rate = 10
        self.pinch_rate = 100

        self.quadtree = quadtree
        for node in self.nodes:
            self.quadtree.insert_point(node)
    
    def clear_growth_tracking(self):
        self.growth_indices = set()
        
    def split_long_edges(self):
        n = len(self.nodes)
        for i in range(n):
            start = self.nodes[i]
            end = self.nodes[(i + 1) % n]
            diff = end.position - start.position
            edge_length_sqr = numpy.dot(diff, diff)
            if edge_length_sqr > MAX_EDGE_LENGTH_SQR:
                self.add_point(i)
        
    def split_pinched_angles(self):
        split_points = []
        n = len(self.nodes)
        for i in range(n):
            a = self.nodes[(i - 1) % n].position
            b = self.nodes[i].position
            c = self.nodes[(i + 1) % n].position

            ba = normalize(a - b)
            bc = normalize(c - b)

            cos_angle = numpy.dot(ba, bc)
            if cos_angle > PINCH_THRESHOLD:
                split_points.append(i)
        
        # add points in reverse order so we don't insert in the wrong
        # place
        for i in reversed(split_points):
            self.add_point(i)
    
    def add_random_point(self):
        n = len(self.nodes)
        index = random.randint(0, n - 1)
        self.add_point(index)
    
    def add_point(self, index):
        # TODO: How to avoid skipping?
        if index in self.growth_indices:
            print(f"Warning: repeated index {index}, skipping")
            return
        self.growth_indices.add(index)

        if not 0 <= index <= len(self.nodes):
            raise RuntimeError("growth index out of bounds")

        before = self.nodes[index]
        after = self.nodes[(index + 1) % len(self.nodes)]
        midpoint = 0.5 * (before.position + after.position)

        point = Node(midpoint)
        self.nodes = self.nodes[:index] + [point] + self.nodes[index + 1:]
        self.quadtree.insert_point(point)
    
    def compute_attraction(self, total_force, node, neighbor_index):
        start = node
        end = self.nodes[neighbor_index]

        diff = end.position - start.position

        # Only apply attraction if the points get far apart
        if numpy.dot(diff, diff) < ATTRACTION_MIN_DIST_SQR:
            return
        
        desired_velocity = limit(diff, MAX_SPEED)
        steering_force = limit(desired_velocity - node.velocity, MAX_FORCE)
        total_force += steering_force
    
    def compute_repulsion(self, total_force, node):
        circle = Circle(node.position, NEARBY_RADIUS)
        nearby_points = self.quadtree.circle_query(circle)

        count = 0
        desired_velocity = numpy.array([0, 0], dtype=numpy.float64)
        for nearby_point in nearby_points:
            if nearby_point == node:
                continue

            # r = point - nearby_point
            # we want r_dir = normalize(r)
            repulsion = normalize(node.position - nearby_point.position)
            desired_velocity += repulsion
        
        # We don't actually need to compute the average, as desired_velocity
        # is already pointing in the average direction. Just set the
        # magnitude to the max speed
        if count > 0:
            set_magnitude(desired_velocity, MAX_SPEED)
        
        steering_force = limit(desired_velocity - node.velocity, MAX_FORCE)
        total_force += steering_force
    
    def compute_forces(self, node, index, delta_time):
        total_force = numpy.array([0, 0], dtype=numpy.float64)

        n = len(self.nodes)
        self.compute_attraction(total_force, node, (index - 1) % n)
        self.compute_attraction(total_force, node, (index + 1) % n)
        self.compute_repulsion(total_force, node)
        # TODO: Keep within a circle. Radii should come from the
        # path simulation

        node.apply_forces(total_force, delta_time)
    
    def update(self, delta_time):
        for i, node in enumerate(self.nodes):
            self.compute_forces(node, i, delta_time)
            #node.clamp_to(self.quadtree.bounds)
            node.check_if_dirty()
        
        # increment the number of iterations first to ensure we don't
        # apply special rules the first frame
        self.iters += 1
        
        if self.iters % self.growth_rate == 0:
            self.add_random_point()

        if self.iters % self.stretch_rate == 0:
            self.split_long_edges()
        
        if self.iters % self.pinch_rate == 0:
            self.split_pinched_angles()
        
        