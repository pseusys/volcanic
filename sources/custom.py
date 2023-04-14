from typing import Callable

import numpy as np

from sources.utils import empty_grid


def terrain_generator(carrier_func: Callable[[float, float], float], noise_func: Callable[[float, float], float], size_x: int, size_z: int, carrier_value: float = 5., noise_value: float = 1.):
    carrier = empty_grid(x=size_x, z=size_z)
    noise = empty_grid(x=size_x, z=size_z)

    for x in range(-size_x // 2, size_x // 2):
        for z in range(-size_z // 2, size_z // 2):
            idx = (x + size_x // 2) * size_x + (z + size_z // 2)
            carrier[idx] = carrier_func(x, z)
            noise[idx] = noise_func(x / size_x, z / size_z)

    height_matrix = carrier_value * np.array(carrier, dtype=np.float64) + noise_value * np.array(noise, dtype=np.float64)

    def generator(xc: int, zc: int) -> float:
        return height_matrix[xc * size_x + zc]

    return generator
