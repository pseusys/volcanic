from typing import Tuple, Callable, Optional

import numpy as np

from ..wrapper import Shader, Mesh
from ..utils import triangle_normal, empty_grid


def _flat_gen(_: int, __: int) -> float:
    return 0.0


class Terrain(Mesh):
    """ Class for drawing a terrain object """

    _MIDDLE_EDGE = 0.3
    _LOWER_COLOR = (0, 0.666, 0)
    _MIDDLE_COLOR = (0.333, 0.333, 0)
    _UPPER_COLOR = (0.999, 0.999, 0.666)
    _FLUCTUATIONS = 0.001

    def __init__(self, shader: Shader, size_x: int, size_z: int, center: Tuple[int, int, int] = (0, 0, 0), generator: Optional[Callable[[int, int], float]] = None):
        if size_x <= 1 or size_z <= 1:
            raise Exception(f"Both terrain length ({size_x}) and width ({size_z}) should be greater than one!")

        self._x = size_x
        self._z = size_z

        generator = _flat_gen if generator is None else generator
        start_x = center[0] - size_x // 2
        start_z = center[2] - size_z // 2

        # Calculate vertex positions:

        self._position = empty_grid(x=size_x, z=size_z)
        for x in range(size_x):
            for z in range(size_z):
                self._position[x * size_x + z] = (start_x + x, generator(x, z), start_z + z)
        self._position = np.array(self._position, dtype=np.float64)

        # Calculate triangle indexes together with normals:

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

        # Calculate average normal for every vertex

        index = np.array(index, dtype=np.uint32)
        for idx in range(len(self._normals)):
            self._normals[idx] = np.average(self._normals[idx], axis=0)

        # Calculate lower and higher height maps

        minimal = self._position.min(axis=0)[1]
        maximal = self._position.max(axis=0)[1]
        edge = (maximal - minimal) * self._MIDDLE_EDGE + minimal
        lower_diff = np.array(self._MIDDLE_COLOR, dtype=np.float64) - np.array(self._LOWER_COLOR, dtype=np.float64)
        upper_diff = np.array(self._UPPER_COLOR, dtype=np.float64) - np.array(self._MIDDLE_COLOR, dtype=np.float64)

        # Calculate material color depending on height

        k_d = empty_grid(x=size_x, z=size_z)
        s = empty_grid(x=size_x, z=size_z, init=lambda: (64.,))
        for idx in range(len(self._position)):
            if self._position[idx][1] <= edge:
                height = (self._position[idx][1] - minimal) / (edge - minimal)
                k_d[idx] = np.array(self._LOWER_COLOR, dtype=np.float64) + lower_diff * height
            else:
                height = (self._position[idx][1] - edge) / (maximal - edge)
                k_d[idx] = np.array(self._MIDDLE_COLOR, dtype=np.float64) + upper_diff * height
                s[idx] = np.array((64.,), dtype=np.float64) * (1 - height)

        k_a = empty_grid(x=size_x, z=size_z, init=lambda: (0, 0, 0))
        k_s = empty_grid(x=size_x, z=size_z, init=lambda: (1, 1, 1))

        # Set variables

        colors = dict(k_a=np.array(k_a, dtype=np.float64), k_d=np.array(k_d, dtype=np.float64), k_s=np.array(k_s, dtype=np.float64), s=np.array(s, dtype=np.float64))
        attributes = dict(position=self._position, normal=self._normals, **colors)
        super().__init__(shader, index=index, attributes=attributes)

    def get_normal(self, x: int, z: int):
        return self._normals[x * self._x + z]

    def get_height(self, x: int, z: int):
        return self._position[x * self._x + z]
