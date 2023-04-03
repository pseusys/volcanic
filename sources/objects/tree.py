import numpy as np

from .terrain import Terrain
from ..wrapper import Shader, Mesh
from ..utils import empty_grid


class Tree(Mesh):
    def __init__(self, shader: Shader, x: int, z: int, terrain: Terrain, height: float, radius: float = 0.3):
        direction = terrain.get_normal(x, z)
        base = terrain.get_height(x, z)

        position_normals = [(radius, 0, radius), (radius, 0, -radius), (-radius, 0, radius), (-radius, 0, -radius)]
        position = [base + direction * height] + [base - (direction + normal) * height / 3 for normal in position_normals]
        position_normals = [direction] + position_normals

        index = np.array([0, 4, 3, 0, 3, 1, 0, 1, 2, 0, 2, 4], dtype=np.uint64)
        normals = np.array([position_normals[index[idx]] for idx in range(len(index))], dtype=np.float64)

        uniforms = dict(k_d=(0, 1, 0), k_s=(1, 1, 1), k_a=(0, 0, 0), s=16.)
        attributes = dict(position=position, normals=normals)
        super().__init__(shader, index=index, attributes=attributes, **uniforms)
