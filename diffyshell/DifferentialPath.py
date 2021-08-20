import math
import numpy
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

numpy.set_printoptions(suppress=True)

class DifferentialPath():
    def __init__(self):
        # Current arc length
        self.arc_length = 0
        # Arc length per iteration
        self.delta_arc_length = 0.01
        # Iterations per row
        self.iters_per_row = 100
        # Total length of the path
        self.max_length = 100

        # compute the number of rows we'll need for the simulation
        rows = math.ceil(
            self.max_length / self.delta_arc_length / self.iters_per_row)
        self.rows = rows

        # Computed position vectors. This is the
        self.positions = numpy.zeros((rows, 3))

        # Computed Frenet-Serret frame at the start of each row
        self.tangents = numpy.zeros((rows, 3), dtype=numpy.float64)
        self.normals = numpy.zeros((rows, 3), dtype=numpy.float64)
        self.binormals = numpy.zeros((rows, 3), dtype=numpy.float64)

        # Computed curvature and torsion values at the start of each row
        self.curvature = numpy.zeros(rows, dtype=numpy.float64)
        self.torsion = numpy.zeros(rows, dtype=numpy.float64)

        # curvature and torsion callbacks
        HELIX_A = 4
        HELIX_B = 3
        HELIX_DENOM = 25
        HELIX_DENOM_LEN = 5
        self.initial_position = [HELIX_A, 0, 0]
        self.initial_tangent = [0, HELIX_A / HELIX_DENOM_LEN, HELIX_B / HELIX_DENOM_LEN]
        self.initial_normal = [-1, 0, 0]
        self.initial_binormal = [0, -HELIX_B / HELIX_DENOM_LEN, HELIX_A / HELIX_DENOM_LEN]
        self.curvature_func = lambda s: HELIX_A / HELIX_DENOM
        self.torsion_func = lambda s: HELIX_B / HELIX_DENOM

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
        self.positions[0] = self.initial_position
        self.tangents[0] = self.initial_tangent
        self.normals[0] = self.initial_normal
        self.binormals[0] = self.initial_binormal

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

        # iterate a number of times, updating the current row in place
        for _ in range(self.iters_per_row):
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

        # compute the current curvature and torsion values
        s = self.arc_length
        curvature = self.curvature_func(s)
        torsion = self.torsion_func(s)
        self.curvature[row] = curvature
        self.torsion[row] = torsion

        # increment the arc length
        self.arc_length += self.delta_arc_length

        # get the current values since we'll be overwriting them
        position = self.positions[row]
        tangent = self.tangents[row]
        normal = self.normals[row]
        binormal = self.binormals[row]

        '''
        print("iter")
        print(position, tangent, normal, binormal)
        print(curvature, torsion)
        '''

        # compute the changes in the Frenet-Serret frame directions given
        # the Frenet-Serret formulas
        delta_tangent = curvature * normal
        delta_normal = -curvature * tangent + torsion * binormal
        delta_binormal = -torsion * normal

        '''
        print("deltas")
        print(delta_tangent, delta_normal, delta_binormal)
        '''

        # use Euler integration to update the Frenet-Serret frame.
        self.tangents[row] = tangent + self.delta_arc_length * delta_tangent
        self.normals[row] = normal + self.delta_arc_length * delta_normal
        self.binormals[row] = binormal + self.delta_arc_length * delta_binormal

        # position is computed by integrating the tangent
        self.positions[row] = position + self.delta_arc_length * self.tangents[row]