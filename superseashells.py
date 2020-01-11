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
