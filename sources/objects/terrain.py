from typing import Tuple, Callable, Optional

import numpy as np

from ..wrapper import Shader, Mesh
from ..utils import triangle_normal, empty_grid


def _flat_gen(_: int, __: int) -> float:
    return 0.0


class Terrain(Mesh):
    """ Class for drawing a terrain object """

    def __init__(self, shader: Shader, size_x: int, size_z: int, center: Tuple[int, int, int] = (0, 0, 0), generator: Optional[Callable[[int, int], float]] = None):
        if size_x <= 1 or size_z <= 1:
            raise Exception(f"Both terrain length ({size_x}) and width ({size_z}) should be greater than one!")

        self._x = size_x
        self._z = size_z

        generator = _flat_gen if generator is None else generator
        start_x = center[0] - size_x // 2
        start_z = center[2] - size_z // 2

        self._position = empty_grid(x=size_x, z=size_z)
        for x in range(size_x):
            for z in range(size_z):
                self._position[x * size_x + z] = (start_x + x, generator(x, z), start_z + z)
        self._position = np.array(self._position, dtype=np.float64)

        index = list()
        self._normals = empty_grid(x=size_x, z=size_z, init=list)
        for x in range(size_x - 1):
            for z in range(size_z - 1):
                vci = x * size_x + z  # Vertex current index
                vbi = x * size_x + (z + 1)  # Vertex below index
                vri = (x + 1) * size_x + z  # Vertex right index
                voi = (x + 1) * size_x + (z + 1)  # Vertex opposite index

                odd_triangle = (vci, vbi, voi)
                even_triangle = (voi, vri, vci)
                index += odd_triangle + even_triangle

                odd_normal = triangle_normal(*[self._position[i] for i in odd_triangle])
                even_normal = triangle_normal(*[self._position[i] for i in even_triangle])

                for vertex in odd_triangle:
                    self._normals[vertex] += [odd_normal]
                for vertex in even_triangle:
                    self._normals[vertex] += [even_normal]

        index = np.array(index, dtype=np.uint32)
        for idx in range(len(self._normals)):
            self._normals[idx] = np.average(self._normals[idx], axis=0)

        uniforms = dict(k_d=(1, 1, 1), k_s=(1, 1, 1), k_a=(0, 0, 0), s=16.)
        attributes = dict(position=self._position, normal=self._normals)
        super().__init__(shader, index=index, attributes=attributes, **uniforms)

    def get_normal(self, x: int, z: int):
        return self._normals[x * self._x + z]

    def get_height(self, x: int, z: int):
        return self._position[x * self._x + z]
