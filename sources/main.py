#!/usr/bin/env python3
import sys

from sources.wrapper import Shader, Viewer, load
from sources.objects.cube import Cube
# import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise


# -------------- main program and scene setup --------------------------------
def main():
    noise = PerlinNoise(octaves=2, seed=1)
    xpix, zpix = 10, 10
    pic = [[noise([i/xpix, j/zpix]) for j in range(xpix)] for i in range(zpix)]
    print(pic)

    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()
    color_shader = Shader("shaders/color.vert", "shaders/color.frag")
    shader = Shader("shaders/phong.vert", "shaders/phong.frag")

    # viewer.add(*[mesh for file in sys.argv[1:] for mesh in load(file, shader)])
    for z in range(zpix):
        for x in range(xpix):
            viewer.add(Cube(color_shader, (x, noise([x/xpix, z/zpix]), z)))

    if len(sys.argv) != 2:
        print('Usage:\n\t%s [3dfile]*\n\n3dfile\t\t the filename of a model in'
              ' format supported by assimp.' % (sys.argv[0],))

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped
