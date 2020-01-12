def subtract(a, b):
    (ax, ay, az) = a
    (bx, by, bz) = b
    return (ax - bx, ay - by, az - bz)

def cross(a, b):
    (ax, ay, az) = a
    (bx, by, bz) = b
    x = ay * bz - az * by
    y = az * bx - ax * bz
    z = ax * by - ay * bx
    return (x, y, z)

def compute_normal(a, b, c):
    ab = subtract(b, a)
    ac = subtract(c, a)
    return cross(ab, ac)

class Mesh:
    def __init__(self):
        self.vertices = []
        self.normals = []
        self.faces = []

    def add_vertex(self, vert):
        vert_id = len(self.vertices)
        self.vertices.append(vert)
        return vert_id 

    def add_face(self, indices):
        [v1, v2, v3] = [self.vertices[idx] for idx in indices]
        normal = compute_normal(v1, v2, v3)
        normal_idx = len(self.normals)
        self.normals.append(normal)
        self.faces.append(indices + [normal_idx])

    def write_obj(self, file):
        for (x, y, z) in self.vertices:
            file.write(f'v {x} {y} {z}\n')

        for (nx, ny, nz) in self.normals:
            file.write(f'vn {nx} {ny} {nz}\n')

        for [v1, v2, v3, n] in self.faces:
            v1_idx = v1 + 1
            v2_idx = v2 + 1
            v3_idx = v3 + 1
            n_idx = n + 1
            file.write(
                f'f {v1_idx}//{n_idx} {v2_idx}//{n_idx} {v3_idx}//{n_idx}\n')
