import numpy
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

from diffyshell.growth.DifferentialPolygon import DifferentialPolygon
from diffyshell.growth.Quadtree import Quadtree
from diffyshell.growth.Rectangle import Rectangle

class DifferentialGrowth():
    def __init__(self):
        rows = 100
        max_nodes = 500

        self.positions = numpy.zeros((rows, max_nodes, 2), dtype=numpy.float64)
        self.slice_lengths = numpy.zeros(rows, dtype=int)
        self.growth_indices = [None for x in range(rows)]

        self.rows = rows
        self.max_nodes = 500
        self.delta_time = 0.1
        self.iters_per_row = 50

        self.width = 500
        self.height = 700

        self.quadtree_node_capacity = 10

        # make a quadtree
        position = numpy.array([0, 0])
        dimensions = numpy.array([self.width, self.height])
        bounds = Rectangle(position, dimensions)
        self.quadtree = Quadtree(bounds, self.quadtree_node_capacity)

        self.polygon = None

    def compute(self):
        self.init_simulation()
        for i in range(1, self.rows):
            self.compute_row(i)

            if i % 10 == 0:
                print(f"computing row {i}")

        print("Displaying results...")
        self.display()
    
    def display(self):
        fig = plt.figure()

        # first plot: cross sections superimposed in 2D
        # second plot: cross sections arranged in 3D
        ax_cross_section = fig.add_subplot(2, 1, 1)
        ax_cross_section.set_aspect('equal', 'box')
        ax_slices = fig.add_subplot(2, 1, 2, projection='3d')
        for i in range(self.rows):
            count = self.slice_lengths[i]
            x = self.positions[i, :count, 0]
            y = self.positions[i, :count, 1]
            z = numpy.full(x.shape, i * 10)

            fraction = (i / (self.rows - 1))
            color = (1, fraction, 0, 0.5 * fraction + 0.5)
            ax_cross_section.plot(x, y, color=color)
            ax_slices.plot(x, y, z, color=color)
        
        plt.show()

    def init_simulation(self):
        points = []
        INITIAL_POINTS = 20
        OFFSET = self.height / 12
        for i in range(INITIAL_POINTS):
            angle = 2.0 * numpy.pi * i / INITIAL_POINTS
            x = 0.5 * self.height + 50 * numpy.cos(angle)
            y = 0.5 * self.height + 50 * numpy.sin(angle)
            points.append(numpy.array([x, y - OFFSET]))
        
        self.polygon = DifferentialPolygon(points, self.quadtree)
        self.row_snapshot(0)

    def row_snapshot(self, row):
        nodes = self.polygon.nodes
        if len(nodes) > self.max_nodes:
            raise RuntimeError(f"Too many nodes at row {row}! Try slowing down the growth rates")

        self.slice_lengths[row] = len(nodes)
        for i, node in enumerate(nodes):
            self.positions[row][i] = node.position
        
        # store growth indices in the parent row, then reset the polygon's
        # growth tracking for the next row
        self.growth_indices[row] = self.polygon.growth_indices
        self.polygon.clear_growth_tracking()
    
    def compute_row(self, row):
        for _ in range(self.iters_per_row):
            self.compute_iter()
        
        self.row_snapshot(row)
    
    def compute_iter(self):
        self.polygon.update(self.delta_time)
        results = self.quadtree.redistribute_dirty_points()
        if len(results) > 0:
            print(f"warning: failed to redistribute points: {results}")
            #raise RuntimeError(f"Failed to redistribute points: {results}")