import numpy as np

from .terrain import Terrain
from ..wrapper import Shader, Mesh


class Tree(Mesh):
    def __init__(self, shader: Shader, x: int, z: int, terrain: Terrain, height: float, radius: float = .3):
        direction = terrain.get_normal(x, z)
        base = terrain.get_height(x, z)

        normals = [(radius, 0, radius), (radius, 0, -radius), (-radius, 0, radius), (-radius, 0, -radius)]
        position = [base + direction * height] + [base - (direction + normal) * height / 3 for normal in normals]

        index = np.array([0, 4, 3, 0, 3, 1, 0, 1, 2, 0, 2, 4], dtype=np.uint64)
        normals = np.array([direction] + normals, dtype=np.float64)

        uniforms = dict(k_d=(0, .5, 0), k_s=(0, 0, 0), k_a=(0, 0, 0), s=16.)
        attributes = dict(position=position, normal=normals)
        super().__init__(shader, index=index, attributes=attributes, **uniforms)
