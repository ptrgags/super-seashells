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