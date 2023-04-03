#!/usr/bin/env python3
import sys
from typing import Callable

import numpy as np
from perlin_noise import PerlinNoise

from sources.objects import Terrain
from sources.wrapper import Shader, Viewer
from sources.utils import empty_grid, laplacian_of_gaussian


def terrain_generator(carrier_func: Callable[[float, float], float], noise_func: Callable[[float, float], float], size_x: int, size_z: int, carrier_value: float = 5., noise_value: float = 1.):
    carrier = empty_grid(size_x, size_z)
    noise = empty_grid(size_x, size_z)

    for x in range(-size_x // 2, size_x // 2):
        for z in range(-size_z // 2, size_z // 2):
            idx = (x + size_x // 2) * size_x + (z + size_z // 2)
            carrier[idx] = carrier_func(x, z)
            noise[idx] = noise_func(x / size_x, z / size_z)

    height_matrix = carrier_value * np.array(carrier, dtype=np.float64) + noise_value * np.array(noise, dtype=np.float64)

    def generator(xc: int, zc: int) -> float:
        return height_matrix[xc * size_x + zc]

    return generator


# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer(distance=150)
    shader = Shader("shaders/phong.vert", "shaders/phong.frag")

    noise = PerlinNoise(octaves=15, seed=1)
    laplacian_sigma = 5
    xpix, ypix, zpix = 100, 10, 100

    generator = terrain_generator(
        lambda x, z: laplacian_of_gaussian(x, z, laplacian_sigma),
        lambda x, z: noise([x, z]),
        xpix,
        zpix,
        50.,
        1.
    )
    viewer.add(Terrain(shader, xpix, ypix, zpix, generator=generator))

    if len(sys.argv) != 2:
        print('Usage:\n\t%s [3dfile]*\n\n3dfile\t\t the filename of a model in format supported by assimp.' % (sys.argv[0],))

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped
