from diffyshell.DifferentialGrowth import DifferentialGrowth
from diffyshell.DifferentialPath import DifferentialPath
from diffyshell.DifferentialTexture import DifferentialTexture

class DifferentialSeashell:
    def __init__(self):
        self.path = DifferentialPath()
        self.cross_section = DifferentialGrowth()
        self.texture = DifferentialTexture()
    
    def compute(self):
        self.path.compute()
        self.cross_section.compute()
    
    def generate_mesh(self):
        # path and unit directions, N x 3
        center = self.path.positions
        normal = self.path.normals
        binormal = self.path.binormals

        # cross section positions, N x M
        x = self.cross_section.positions[:, :, 0]
        y = self.cross_section.positions[:, :, 1]
        
        # vertices: N x M x 3
        vertices = (
            center[:, None, :] + 
            x[:, :, None] * normal[:, None, :] + 
            y[:, :, None] * binormal[:, None, :])
        
        
        #self.vertices = self.path.positions + self.path.normals * self.cross_section.positions[:, 0]