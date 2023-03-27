#!/usr/bin/env python3
import sys

import numpy as np

from sources.objects import Terrain
from sources.wrapper import Shader, Viewer
from perlin_noise import PerlinNoise


def terrain_generator(noise: PerlinNoise, size_x: int, size_y: int, size_z: int):
    # carrier = [-x ** 4 + 0.5 * x ** 3 + 3 * x ** 2 - x + 4 for x in range(size_x) for _ in range(size_z)]
    perlin = [noise([x / size_x, z / size_z]) for x in range(size_x) for z in range(size_z)]
    height_matrix = np.array(perlin, dtype=np.float64) # + 5 * np.array(carrier, dtype=np.float64)
    height_matrix = (height_matrix - np.min(height_matrix)) / (np.max(height_matrix) - np.min(height_matrix)) * size_y

    def perlin_generator(x: int, z: int) -> float:
        return height_matrix[x * size_x + z]

    return perlin_generator


# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()
    color_shader = Shader("shaders/color.vert", "shaders/color.frag")
    shader = Shader("shaders/phong.vert", "shaders/phong.frag")

    noise = PerlinNoise(octaves=50, seed=1)
    xpix, ypix, zpix = 100, 10, 100

    generator = terrain_generator(noise, xpix, ypix, zpix)
    # viewer.add(*[mesh for file in sys.argv[1:] for mesh in load(file, shader)])
    viewer.add(Terrain(color_shader, xpix, ypix, zpix, generator=generator))

    if len(sys.argv) != 2:
        print('Usage:\n\t%s [3dfile]*\n\n3dfile\t\t the filename of a model in'
              ' format supported by assimp.' % (sys.argv[0],))

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped
