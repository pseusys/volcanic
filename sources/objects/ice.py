import numpy as np

from ..wrapper import Shader, Mesh


class Ice(Mesh):
    def __init__(self, shader: Shader, x: int, z: int, height: float):
        normals = [(-1, 1, 1), (-1, 1, -1), (1, 1, 1), (1, 1, -1), (-1, -1, 1), (-1, -1, -1), (1, -1, 1), (1, -1, -1)]
        position = [
            (x - 1, height + .25, z + 1),
            (x - 1, height + .25, z - 1),
            (x + 1, height + .25, z + 1),
            (x + 1, height + .25, z - 1),
            (x - 1, height - .25, z + 1),
            (x - 1, height - .25, z - 1),
            (x + 1, height - .25, z + 1),
            (x + 1, height - .25, z - 1)
        ]
        index = [
            0, 2, 1,
            1, 2, 3,
            0, 4, 6,
            0, 6, 2,
            2, 6, 7,
            2, 7, 3,
            3, 7, 5,
            3, 5, 1,
            1, 5, 6,
            1, 6, 0
        ]

        index = np.array(index, dtype=np.uint64)
        position = np.array(position, dtype=np.float64)
        normals = np.array(normals, dtype=np.float64)

        uniforms = dict(k_a=(0, 0, 0), k_d=(.8, 1., 1.), k_s=(0, 0, 0), s=.2, a=.75)
        attributes = dict(position=position, normal=normals)
        super().__init__(shader, index=index, attributes=attributes, **uniforms)
