import numpy

class Node:
    def __init__(self, position):
        self.position = position
        self.velocity = numpy.array([0, 0])
        self.acceleration = numpy.array([0, 0])
        self.mass = 1.0
        self.quadtree_node = None
        self.is_dirty = False
    
    def apply_forces(self, net_force, delta_time):
        # From Newton's Second Law
        # a = F / m
        self.acceleration = net_force / self.mass

        # Velocity is the integral of acceleration
        # dv = da * dt
        self.velocity = self.acceleration * delta_time

        # Position is the integral of velocity
        # dx = dv * dt
        self.position = self.velocity * delta_time
    
    def check_if_dirty(self):
        self.is_dirty = not self.quadtree_node.bounds.contains(self.position)