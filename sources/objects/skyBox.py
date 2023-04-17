import numpy as np
from ..wrapper import TexturedCubeMap, TextureCubeMap, Shader, Mesh

class SkyBox(TexturedCubeMap):
    def __init__(self, size, shader: Shader):
        front = ((-1, 1, -1), 
                 (1, 1, -1), 
                 (1, 1, 1), 
                 (1, 1, 1), 
                 (-1, 1, 1), 
                 (-1, 1, -1))
        back = ((-1, -1, -1), 
                (-1, -1, 1), 
                (1, -1, -1), 
                (1, -1, -1), 
                (-1, -1, 1), 
                (1, -1, 1))
        left = ((-1, 1, -1), 
                (-1, -1, -1), 
                (1, -1, -1), 
                (1, -1, -1), 
                (1, 1, -1), 
                (-1, 1, -1))
        right = ((-1, -1, 1), 
                 (-1, -1, -1), 
                 (-1, 1, -1), 
                 (-1, 1, -1), 
                 (-1, 1, 1), 
                 (-1, -1, 1))
        top = ((1, -1, -1), 
               (1, -1, 1), 
               (1, 1, 1), 
               (1, 1, 1), 
               (1, 1, -1), 
               (1, -1, -1))
        bottom = ((-1, -1, 1), 
                  (-1, 1, 1), 
                  (1, 1, 1), 
                  (1, 1, 1), 
                  (1, -1, 1), 
                  (-1, -1, 1))

        vertices = front + back + left + right + top + bottom
        scaled = size * np.array(vertices, np.float32)
        cube = Mesh(shader, attributes=dict(position=scaled))
        skyBox = TextureCubeMap()

        super().__init__(cube, skyBox=skyBox)
