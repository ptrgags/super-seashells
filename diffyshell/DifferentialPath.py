import math
import numpy
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

class DifferentialPath():
    def __init__(self):
        # Current arc length
        self.arc_length = 0
        # Arc length per iteration
        self.delta_arc_length = 0.1
        # Iterations per row
        self.iters_per_row = 10
        # Total length of the path
        self.max_length = 1000

        # compute the number of rows we'll need for the simulation
        rows = math.ceil(
            self.max_length / self.delta_arc_length / self.iters_per_row)
        self.rows = rows

        # Computed position vectors. This is the
        self.positions = numpy.zeros((rows, 3))

        # Computed Frenet-Serret frame at the start of each row
        self.tangents = numpy.zeros((rows, 3))
        self.normals = numpy.zeros((rows, 3))
        self.binormals = numpy.zeros((rows, 3))

        # Computed curvature and torsion values at the start of each row
        self.curvature = numpy.zeros(rows)
        self.torsion = numpy.zeros(rows)

        # curvature and torsion callbacks
        self.curvature_func = lambda s: 0.01
        self.torsion_func = lambda s: 0.01

    def compute(self):
        """
        Compute a simulation of the differential curve
        """
        self.init_simulation()
        for i in range(1, self.rows):
            self.compute_row(i)

        self.show_path()

    def show_path(self):
        x = self.positions[:, 0]
        y = self.positions[:, 1]
        z = self.positions[:, 2]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(x, y, z)
        plt.show()

    def init_simulation(self):
        """
        Initialize the first row of the simulation to initial
        values
        """
        self.positions[0] = [1, 0, 0]
        self.tangents[0] = [1, 0, 0]
        self.normals[0] = [0, 1, 0]
        self.binormals[0] = [0, 0, 1]

        self.curvature[0] = self.curvature_func(0.0)
        self.torsion[0] = self.torsion_func(0.0)
            
    def compute_row(self, row):
        """
        Update the simulation, populating the next
        row of each variable

        preconditions:
        - variables[row - 1] are populated

        postcondition:
        - variables[row] are populated
    
        :param int row: the index of the new row
        """
        prev_row = row - 1

        # first copy values into the new row. Curvature and
        # torsion are not copied as those are computed directly
        # from the callback functions.
        self.positions[row] = self.positions[prev_row]
        self.tangents[row] = self.tangents[prev_row]
        self.normals[row] = self.normals[prev_row]
        self.binormals[row] = self.binormals[prev_row]

        # currently we are at row i.
        # iterate a number of times and populate row i + 1
        # then set the row to i + 1
        for i in range(self.iters_per_row):
            self.compute_iter(row)
    
    def compute_iter(self, row):
        """
        Perform one iteration of the simulation. This
        works in place on the new row, as we only keep the
        last iteration (see update_row())

        preconditions:
        - variables[row] have valid values for just before this
            iteration

        postconditions:
        - self.arc_length is incremented by self.delta_arc_length
        - variables[row] are updated in place
        """
        # increment the arc length first to be the arc length
        # at this iteration.
        self.arc_length += self.delta_arc_length

        # compute the current curvature and torsion values
        s = self.arc_length
        curvature = self.curvature_func(s)
        torsion = self.torsion_func(s)
        self.curvature[row] = curvature
        self.torsion[row] = torsion

        # get the current values since we'll be overwriting them
        position = self.positions[row]
        tangent = self.tangents[row]
        normal = self.normals[row]
        binormal = self.binormals[row]

        # compute the changes in the Frenet-Serret frame directions given
        # the Frenet-Serret formulas
        delta_tangent = curvature * normal
        delta_normal = -curvature * tangent + torsion * binormal
        delta_binormal = -torsion * normal

        # use Euler integration to update the Frenet-Serret frame.
        self.tangents[row] = tangent + self.delta_arc_length * delta_tangent
        self.normals[row] = normal + self.delta_arc_length * delta_normal
        self.binormals[row] = binormal + self.delta_arc_length * delta_binormal

        # position is computed by integrating the tangent
        self.positions[row] = position + self.delta_arc_length * self.tangents[row]