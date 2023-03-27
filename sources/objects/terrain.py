from typing import Tuple, Callable, Optional, List

import numpy as np

from ..wrapper import Shader, Mesh
from ..utils import triangle_normal


def _flat_gen(_: int, __: int) -> float:
    return 0.0


def _empty_grid(x: int, z: int) -> List:
    return [None] * x * z


class Terrain(Mesh):
    """ Class for drawing a terrain object """

    def __init__(self, shader: Shader, size_x: int, size_y, size_z: int, center: Tuple[int, int, int] = (0, 0, 0), generator: Optional[Callable[[int, int], float]] = None):
        if size_x <= 1 or size_z <= 1:
            raise Exception(f"Both terrain length ({size_x}) and width ({size_z}) should be greater than one!")

        generator = _flat_gen if generator is None else generator
        start_x = center[0] - size_x // 2
        start_z = center[2] - size_z // 2

        position = _empty_grid(size_x, size_z)
        color = _empty_grid(size_x, size_z)
        for x in range(size_x):
            for z in range(size_z):
                idx = x * size_x + z
                height = generator(x, z)
                position[idx] = (start_x + x, height, start_z + z)
                color[idx] = (0, height / size_y, 0)
        position = np.array(position, dtype=np.float64)
        color = np.array(color, dtype=np.float64)

        index = list()
        normals = _empty_grid(size_x, size_z)
        for x in range(size_x - 1):
            for z in range(size_z - 1):
                vci = x * size_x + z  # Vertex current index
                vbi = x * size_x + (z + 1)  # Vertex below index
                vri = (x + 1) * size_x + z  # Vertex right index
                voi = (x + 1) * size_x + (z + 1)  # Vertex opposite index

                odd_triangle = (vci, vbi, voi)
                even_triangle = (voi, vri, vci)
                index += odd_triangle + even_triangle

                for vertex in odd_triangle:
                    normals[vertex] += triangle_normal(*[position[i] for i in odd_triangle])
                for vertex in even_triangle:
                    normals[vertex] += triangle_normal(*[position[i] for i in even_triangle])
        index = np.array(index, dtype=np.uint32)

        for index in range(len(normals)):
            normals[index] = np.average(normals[index])

        attributes = dict(position=position, color=color)
        super().__init__(shader, index=index, attributes=attributes)
