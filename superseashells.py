import math
import cmath

from mesh import Mesh

def lerp(a, b, t):
    return (1.0 - t) * a + t * b

def loglerp(a, b, t):
    return a ** (1.0 - t) * b ** t

def add_vecs(v1, v2):
    (x1, y1, z1) = v1
    (x2, y2, z2) = v2

    return (x1 + x2, y1 + y2, z1 + z2)

def rotate(vec, angle):
    (x, y) = vec
    z = complex(x, y)
    result = cmath.exp(1j * angle) * z
    return (result.real, result.imag)

def scale(vec, r):
    (x, y) = vec
    return (r * x, r * y)

def sgn(x):
    if x > 0.0:
        return 1.0
    elif x < 0.0:
        return -1.0
    else:
        return 0.0

def supercos(theta, m):
    cos_theta = math.cos(theta)
    return sgn(cos_theta) * abs(cos_theta) ** (2.0 / m)

def supersin(theta, m):
    sin_theta = math.sin(theta)
    return sgn(sin_theta) * abs(sin_theta) ** (2.0 / m)

def superellipse(theta, m, n):
    return (supercos(theta, m), supersin(theta, n))

def empty_grid(rows, cols):
    return [[None for j in range(cols)] for i in range(rows)]

class SuperSeashell:
    def __init__(self, parameters):
        self.parameters = parameters
        self.u_res = parameters['cross_section_resolution']
        self.v_res = parameters['coil_resolution']
        self.topology = parameters['topology']
        self.rows = empty_grid(self.v_res + 1, self.u_res)
        self.start_cap = None
        self.end_cap = None
        self.mesh = Mesh()

    def generate_mesh(self):
        self.generate_vertices()
        self.generate_faces()
        return self.mesh

    def generate_vertices(self):
        if self.topology == 'torus':
            self.generate_torus_vertices()
        elif self.topology == 'cone':
            self.generate_cone_vertices()
        elif self.topology == 'reverse_cone':
            self.generate_reverse_cone_vertices()
        elif self.topology == 'cylinder':
            self.generate_cylinder_vertices()
        else:
            raise RuntimeError(f'Not a valid topology: {self.topology}')

    def generate_torus_vertices(self):
        for j in range(self.v_res):
            v = float(j) / (self.v_res)
            for i in range(self.u_res):
                u = float(i) / (self.u_res)
                vertex = self(u, v)
                idx = self.mesh.add_vertex(vertex)
                self.rows[j][i] = idx

    def generate_cone_vertices(self):
        start_cap = self.coil(0.0)
        self.start_cap = self.mesh.add_vertex(start_cap)

        for i in range(self.v_res):
            v = float(i) / (self.v_res)
            for j in range(self.u_res):
                u = float(j) / (self.u_res)
                vertex = self(u, v)
                idx = self.mesh.add_vertex(vertex)
                self.rows[i][j] = idx

        end_point = self(0.0, 1.0) 
        end_idx = self.mesh.add_vertex(end_point)
        self.rows[-1][0] = end_idx

    def generate_reverse_cone_vertices(self):
        start_point = self(0.0, 0.0) 
        start_idx = self.mesh.add_vertex(start_point)
        self.rows[0][0] = start_idx

        for i in range(1, self.v_res + 1):
            v = float(i) / (self.v_res)
            for j in range(self.u_res):
                u = float(j) / (self.u_res)
                vertex = self(u, v)
                idx = self.mesh.add_vertex(vertex)
                self.rows[i][j] = idx

        end_cap = self.coil(1.0)
        self.end_cap = self.mesh.add_vertex(end_cap)

    def generate_cylinder_vertices(self): 
        start_cap = self.coil(0.0)
        self.start_cap = self.mesh.add_vertex(start_cap)

        for i in range(self.v_res + 1):
            v = float(i) / (self.v_res)
            for j in range(self.u_res):
                u = float(j) / (self.u_res)
                vertex = self(u, v)
                idx = self.mesh.add_vertex(vertex)
                self.rows[i][j] = idx

        end_cap = self.coil(1.0)
        self.end_cap = self.mesh.add_vertex(end_cap)

    def generate_faces(self):
        if self.topology == 'torus':
            self.generate_torus_faces()
        elif self.topology == 'cone':
            self.generate_cone_faces()
        elif self.topology == 'reverse_cone':
            self.generate_reverse_cone_faces()
        elif self.topology == 'cylinder':
            self.generate_cylinder_faces()
        else:
            raise RuntimeError(f'Not a valid topology: {self.topology}')

    def generate_torus_faces(self):
        for i in range(self.v_res - 1):
            for j in range(self.u_res - 1):
                v1 = self.rows[i][j]
                v2 = self.rows[i][j + 1]
                v3 = self.rows[i + 1][j + 1]
                v4 = self.rows[i + 1][j]

                # This is intentionally clockwise to ensure normals are
                # pointing outwards
                self.mesh.add_face([v1, v4, v3])
                self.mesh.add_face([v1, v3, v2])

        # Fill the seam
        for i in range(self.v_res - 1):
            v1 = self.rows[i][-1]
            v2 = self.rows[i][0]
            v3 = self.rows[i + 1][0]
            v4 = self.rows[i + 1][-1]

            # This is intentionally clockwise to ensure normals are
            # pointing outwards
            self.mesh.add_face([v1, v4, v3])
            self.mesh.add_face([v1, v3, v2])

        # loop the end back to the start
        for j in range(self.u_res - 1):
            v1 = self.rows[-2][j]
            v2 = self.rows[-2][j + 1]
            v3 = self.rows[0][j + 1]
            v4 = self.rows[0][j]

            # This is intentionally clockwise to ensure normals are
            # pointing outwards
            self.mesh.add_face([v1, v4, v3])
            self.mesh.add_face([v1, v3, v2])

        # Add the last quad where the seam meets the loop row
        v1 = self.rows[-2][-1]
        v2 = self.rows[-2][0]
        v3 = self.rows[0][0]
        v4 = self.rows[0][-1]

        # This is intentionally clockwise to ensure normals are
        # pointing outwards
        self.mesh.add_face([v1, v4, v3])
        self.mesh.add_face([v1, v3, v2])

    def generate_cone_faces(self):
        for i in range(self.v_res - 1):
            for j in range(self.u_res - 1):
                v1 = self.rows[i][j]
                v2 = self.rows[i][j + 1]
                v3 = self.rows[i + 1][j + 1]
                v4 = self.rows[i + 1][j]

                # This is intentionally clockwise to ensure normals are
                # pointing outwards
                self.mesh.add_face([v1, v4, v3])
                self.mesh.add_face([v1, v3, v2])


        # Fill the seam
        for i in range(self.v_res - 1):
            v1 = self.rows[i][-1]
            v2 = self.rows[i][0]
            v3 = self.rows[i + 1][0]
            v4 = self.rows[i + 1][-1]

            # This is intentionally clockwise to ensure normals are
            # pointing outwards
            self.mesh.add_face([v1, v4, v3])
            self.mesh.add_face([v1, v3, v2])

        # Add cap at the start end
        for j in range(self.u_res - 1):
            v1 = self.rows[0][j]
            v2 = self.rows[0][j + 1]
            self.mesh.add_face([self.start_cap, v1, v2])

        # start cap seam
        v1 = self.rows[0][-1]
        v2 = self.rows[0][0]
        self.mesh.add_face([self.start_cap, v1, v2])

        # End comes to a point
        for j in range(self.u_res - 1):
            point = self.rows[-1][0]
            v1 = self.rows[-2][j]
            v2 = self.rows[-2][j + 1]
            self.mesh.add_face([point, v2, v1])

        # point seam
        point = self.rows[-1][0]
        v1 = self.rows[-2][-1]
        v2 = self.rows[-2][0]
        self.mesh.add_face([point, v2, v1])

    def generate_reverse_cone_faces(self):
        for i in range(1, self.v_res):
            for j in range(self.u_res - 1):
                v1 = self.rows[i][j]
                v2 = self.rows[i][j + 1]
                v3 = self.rows[i + 1][j + 1]
                v4 = self.rows[i + 1][j]

                # This is intentionally clockwise to ensure normals are
                # pointing outwards
                self.mesh.add_face([v1, v4, v3])
                self.mesh.add_face([v1, v3, v2])


        # Fill the seam
        for i in range(1, self.v_res):
            v1 = self.rows[i][-1]
            v2 = self.rows[i][0]
            v3 = self.rows[i + 1][0]
            v4 = self.rows[i + 1][-1]

            # This is intentionally clockwise to ensure normals are
            # pointing outwards
            self.mesh.add_face([v1, v4, v3])
            self.mesh.add_face([v1, v3, v2])

        # Add cap at the end
        for j in range(self.u_res - 1):
            v1 = self.rows[-1][j]
            v2 = self.rows[-1][j + 1]
            self.mesh.add_face([self.end_cap, v2, v1])

        # end cap seam
        v1 = self.rows[-1][-1]
        v2 = self.rows[-1][0]
        self.mesh.add_face([self.end_cap, v2, v1])

        # start comes to a point
        for j in range(self.u_res - 1):
            point = self.rows[0][0]
            v1 = self.rows[1][j]
            v2 = self.rows[1][j + 1]
            self.mesh.add_face([point, v1, v2])

        # point seam
        point = self.rows[0][0]
        v1 = self.rows[1][-1]
        v2 = self.rows[1][0]
        self.mesh.add_face([point, v1, v2])

    def generate_cylinder_faces(self):
        for i in range(self.v_res):
            for j in range(self.u_res - 1):
                v1 = self.rows[i][j]
                v2 = self.rows[i][j + 1]
                v3 = self.rows[i + 1][j + 1]
                v4 = self.rows[i + 1][j]

                # This is intentionally clockwise to ensure normals are
                # pointing outwards
                self.mesh.add_face([v1, v4, v3])
                self.mesh.add_face([v1, v3, v2])

        # Fill the seam
        for i in range(self.v_res):
            v1 = self.rows[i][-1]
            v2 = self.rows[i][0]
            v3 = self.rows[i + 1][0]
            v4 = self.rows[i + 1][-1]

            # This is intentionally clockwise to ensure normals are
            # pointing outwards
            self.mesh.add_face([v1, v4, v3])
            self.mesh.add_face([v1, v3, v2])

        # Add cap at the start end
        for j in range(self.u_res - 1):
            v1 = self.rows[0][j]
            v2 = self.rows[0][j + 1]
            self.mesh.add_face([self.start_cap, v1, v2])

        # start cap seam
        v1 = self.rows[0][-1]
        v2 = self.rows[0][0]
        self.mesh.add_face([self.start_cap, v1, v2])

        # end cap
        for j in range(self.u_res - 1):
            v1 = self.rows[-1][j]
            v2 = self.rows[-1][j + 1]
            self.mesh.add_face([self.end_cap, v2, v1])

        # end cap seam
        v1 = self.rows[-1][-1]
        v2 = self.rows[-1][0]
        self.mesh.add_face([self.end_cap, v2, v1])

    def __call__(self, u, v):
        return add_vecs(self.coil(v), self.cross_section(u, v))

    def lerp_params(self, param_name, t):
        [a, b] = self.parameters[param_name]
        return lerp(a, b, t)

    def loglerp_params(self, param_name, t):
        [a, b] = self.parameters[param_name]
        return loglerp(a, b, t)

    def coil_shape(self, v):
        phi = self.lerp_params('coil_angle', v) * 2.0 * math.pi
        p = self.loglerp_params('coil_p', v)
        q = self.loglerp_params('coil_q', v)

        return superellipse(phi, p, q)

    def coil(self, v):
        z = self.lerp_params('coil_z', v)
        b = self.loglerp_params('coil_logarithm', v)
        R = self.lerp_params('coil_radius', v)
        radius = R * math.exp(b * v)

        (shape_x, shape_y) = self.coil_shape(v)  
        return (radius * shape_x, radius * shape_y, z)

    def cross_section(self, u, v):
        (shape_x, shape_y) = self.coil_shape(v)
        (twist_s, twist_z) = self.twisted(u, v)
        return (twist_s * shape_x, twist_s * shape_y, twist_z)

    def twisted(self, u, v): 
        m = self.loglerp_params('cross_section_m', v)
        n = self.loglerp_params('cross_section_n', v)
        delta = self.lerp_params('cross_section_twist', v)
        r = self.lerp_params('cross_section_radius', v)
        theta = 2 * math.pi * u

        shape = superellipse(theta, m, n)
        return scale(rotate(shape, delta), r)
