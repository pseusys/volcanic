from typing import Tuple, Callable, Optional

import numpy as np

from ..wrapper import Shader, Mesh


def _flat_gen(_: int, __: int) -> float:
    return 0.0


class Terrain(Mesh):
    """ Class for drawing a terrain object """

    def __init__(self, shader: Shader, size_x: int, size_y, size_z: int, center: Tuple[int, int, int] = (0, 0, 0), generator: Optional[Callable[[int, int], float]] = None):
        if size_x <= 1 or size_z <= 1:
            raise Exception(f"Both terrain length ({size_x}) and width ({size_z}) should be greater than one!")

        generator = _flat_gen if generator is None else generator
        start_x = center[0] - size_x // 2
        start_z = center[2] - size_z // 2

        position = list()
        color = list()
        for x in range(size_x):
            for z in range(size_z):
                height = generator(x, z)
                position += [(start_x + x, height, start_z + z)]
                color += [(0, height / size_y, 0)]
        position = np.array(position, dtype=np.float64)
        color = np.array(color, dtype=np.float64)

        index = list()
        for x in range(size_x - 1):
            for z in range(size_z - 1):
                index += [x * size_x + z, x * size_x + (z + 1), (x + 1) * size_x + (z + 1)]
                index += [(x + 1) * size_x + (z + 1), (x + 1) * size_x + z, x * size_x + z]
        index = np.array(index, dtype=np.uint32)

        attributes = dict(position=position, color=color)
        super().__init__(shader, index=index, attributes=attributes)
