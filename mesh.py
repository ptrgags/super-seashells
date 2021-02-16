import struct
import json

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

    def write_obj(self, obj_file):
        for (x, y, z) in self.vertices:
            obj_file.write(f'v {x} {y} {z}\n'.encode('utf-8'))

        for (nx, ny, nz) in self.normals:
            obj_file.write(f'vn {nx} {ny} {nz}\n'.encode('utf-8'))

        for [v1, v2, v3, n] in self.faces:
            v1_idx = v1 + 1
            v2_idx = v2 + 1
            v3_idx = v3 + 1
            n_idx = n + 1
            line = f'f {v1_idx}//{n_idx} {v2_idx}//{n_idx} {v3_idx}//{n_idx}\n' 
            obj_file.write(line.encode('utf-8'))

    def make_glb_buffer_views(self):
        vertex_bv = b''
        normal_bv = b''

        min_x = float('inf')
        min_y = float('inf')
        min_z = float('inf')
        max_x = -float('inf')
        max_y = -float('inf')
        max_z = -float('inf')

        for [v1, v2, v3, n] in self.faces:
            (x, y, z) = self.vertices[v1]
            vertex_bv += pack_vec3(x, y, z)
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            min_z = min(min_z, z)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
            max_z = max(max_z, z)

            (x, y, z) = self.vertices[v2]
            vertex_bv += pack_vec3(x, y, z)
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            min_z = min(min_z, z)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
            max_z = max(max_z, z)

            (x, y, z) = self.vertices[v2]
            vertex_bv += pack_vec3(x, y, z)
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            min_z = min(min_z, z)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
            max_z = max(max_z, z)

            (nx, ny, nz) = self.normals[n]
            normal_bv += pack_vec3(x, y, z)

        min_pos = [min_x, min_y, min_z]
        max_pos = [max_x, max_y, max_z]
        return vertex_bv, normal_bv, min_pos, max_pos

    def write_glb(self, glb_file):
        GLB_ALIGNMENT = 4
        GLB_MAGIC = b'glTF'
        GLB_LEN_HEADER = 12
        GLB_CHUNK_BIN = b'BIN\x00'
        GLB_CHUNK_JSON = b'JSON'
        GLB_VERSION = pack_u32(2)
        GLB_FLOAT = 5126

        vertex_bv, normal_bv, min_pos, max_pos = self.make_glb_buffer_views()
        
        vert_offset = 0
        vert_len = len(vertex_bv)
        vertex_bv = pad_binary(vertex_bv, GLB_ALIGNMENT)
        
        normal_offset = len(vertex_bv)
        normal_len = len(normal_bv)
        normal_bv = pad_binary(normal_bv, GLB_ALIGNMENT)

        buf = vertex_bv + normal_bv
        
        gltf_json = {
            "asset": {
                "version": "2.0"
            },
            "scenes": [
                {
                    "nodes": [0]
                }
            ],
            "nodes": [
                {
                    "mesh": 0
                }
            ],
            "meshes": [
                {
                    "name": "Super Seashell",
                    "primitives": [
                        {
                            "attributes": {
                                "POSITION": 0,
                                "NORMAL": 1
                            },
                            #"mode": GLB_MODE_TRIANGLES
                        }
                    ]
                }
            ],
            "buffers": [
                {
                    "byteLength": len(buf)
                }
            ],
            "bufferViews": [
                {
                    "name": "Vertices",
                    "buffer": 0,
                    "byteLength": vert_len,
                    "byteOffset": vert_offset
                },
                {
                    "name": "Normals",
                    "buffer": 0,
                    "byteLength": normal_len,
                    "byteOffset": normal_offset
                }
            ],
            "accessors": [
                {
                    "name": "Vertices",
                    "bufferView": 0,
                    "byteOffset": 0,
                    "componentType": GLB_FLOAT, 
                    "type": "VEC3",
                    "count": len(self.faces),
                    "min": min_pos,
                    "max": max_pos
                },
                {
                    "name": "Normals",
                    "bufferView": 1,
                    "byteOffset": 0,
                    "componentType": GLB_FLOAT,
                    "type": "VEC3",
                    "count": len(self.faces)
                }
            ]
        }

        gltf_json_str = json.dumps(gltf_json)
        gltf_json_bytes = bytes(gltf_json_str, 'utf-8')
        gltf_json_bytes = pad_json(gltf_json_bytes, GLB_ALIGNMENT)

        json_length = len(gltf_json_bytes)
        json_chunk = pack_u32(json_length) + GLB_CHUNK_JSON + gltf_json_bytes

        bin_len = len(buf)
        bin_chunk = pack_u32(bin_len) + GLB_CHUNK_BIN + buf

        total_length = GLB_LEN_HEADER + len(json_chunk) + len(bin_chunk)
        header = GLB_MAGIC + GLB_VERSION + pack_u32(total_length)

        glb = header + json_chunk + bin_chunk
        glb_file.write(glb)
        

def pad_json(binary, alignment):
    if len(binary) % alignment == 0:
        return binary

    padding = alignment - (len(binary) % alignment)
    return binary + b' ' * padding

def pad_binary(binary, alignment):
    if len(binary) % alignment == 0:
        return binary

    padding = alignment - (len(binary) % alignment)
    return binary + b'\x00' * padding

def pack_u32(value):
    return struct.pack('<I', value)

def pack_vec3(x, y, z):
    return struct.pack('<fff', x, y, z)
