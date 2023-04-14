#!/usr/bin/env python3
from math import sqrt
from typing import Dict

from perlin_noise import PerlinNoise

from sources.config import read_config
from sources.custom import terrain_generator
from sources.objects import Terrain, Tree
from sources.wrapper import Shader, Viewer
from sources.utils import laplacian_of_gaussian, conditional_random_points


def main(configs: Dict[str, Dict[str, int]]):
    viewer = Viewer(distance=configs["general"]["distance"])
    shader = Shader("shaders/phong.vert", "shaders/phong.frag")

    xpix = configs["general"]["size_x"]
    zpix = configs["general"]["size_z"]

    noise = PerlinNoise(octaves=configs["terrain"]["perlin_octaves"], seed=1)
    laplacian_sigma = configs["terrain"]["laplacian_sigma"]
    sigma_radius = configs["terrain"]["sigma_radius"]

    xav = xpix / 2
    zav = zpix / 2
    tree_number = configs["trees"]["tree_number"]
    tree_margin = configs["trees"]["tree_margin"]
    tree_height = configs["trees"]["tree_height"]

    generator = terrain_generator(
        lambda x, z: laplacian_of_gaussian(x, z, laplacian_sigma),
        lambda x, z: noise([x, z]),
        xpix,
        zpix,
        configs["terrain"]["carrier_weight"],
        configs["terrain"]["perlin_weight"]
    )
    terrain = Terrain(shader, xpix, zpix, generator=generator)
    viewer.add(terrain)

    def inside_volcano(x: int, z: int) -> bool:
        return sqrt((x - xav) ** 2 + (z - zav) ** 2) > laplacian_sigma * sigma_radius

    trees = conditional_random_points(tree_number, inside_volcano, xpix - tree_margin, zpix - tree_margin, tree_margin, tree_margin)
    for tx, tz in trees:
        viewer.add(Tree(shader, tx, tz, terrain, tree_height))

    viewer.run()


if __name__ == '__main__':
    main(read_config())
