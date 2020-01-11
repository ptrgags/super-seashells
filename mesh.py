class Mesh:
    def __init__(self):
        self.vertices = []

    def add_vertex(self, vert):
        vert_id = len(self.vertices)
        self.vertices.append(vert)
        return vert_id 

    def write_obj(self, file):
        for (x, y, z) in self.vertices:
            file.write(f'v {x} {y} {z}\n')
