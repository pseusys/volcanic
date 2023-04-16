#!/usr/bin/env python3
from math import sqrt
from typing import Dict

from perlin_noise import PerlinNoise

from sources.config import read_config
from sources.custom import terrain_generator
from sources.objects import Terrain, Tree, Liquid
from sources.wrapper import Shader, Viewer
from sources.utils import laplacian_of_gaussian, conditional_random_points


def main(configs: Dict[str, Dict[str, int]]):
    viewer = Viewer(distance=configs["general"]["distance"])
    shader = Shader("shaders/phong.vert", "shaders/phong.frag")
    shader_map = Shader("shaders/phong_map.vert", "shaders/phong_map.frag")
    shader_water = Shader("shaders/liquid.vert", "shaders/liquid.frag")

    xpix = configs["general"]["size_x"]
    zpix = configs["general"]["size_z"]

    noise = PerlinNoise(octaves=configs["terrain"]["perlin_octaves"])
    laplacian_sigma = configs["terrain"]["laplacian_sigma"]
    sigma_radius = configs["terrain"]["sigma_radius"]

    xav = xpix / 2
    zav = zpix / 2
    tree_number = configs["trees"]["tree_number"]
    tree_margin = configs["trees"]["tree_margin"]
    tree_height = configs["trees"]["tree_height"]

    if sqrt((xav - tree_margin) ** 2 + (zav - tree_margin) ** 2) <= laplacian_sigma * sigma_radius and tree_number > 0:
        print(f"Configuration incorrect! No place for {tree_number} trees!")
        exit(1)

    generator = terrain_generator(
        lambda x, z: laplacian_of_gaussian(x, z, laplacian_sigma),
        lambda x, z: noise([x, z]),
        xpix,
        zpix,
        configs["terrain"]["carrier_weight"],
        configs["terrain"]["perlin_weight"]
    )
    terrain = Terrain(shader_map, xpix, zpix, generator=generator)
    viewer.add(terrain)

    liquid = Liquid(shader_water, "assets/lava.png")
    viewer.add(liquid)

    def inside_volcano(x: int, z: int) -> bool:
        return sqrt((x - xav) ** 2 + (z - zav) ** 2) > laplacian_sigma * sigma_radius

    trees = conditional_random_points(tree_number, inside_volcano, xpix - tree_margin, zpix - tree_margin, tree_margin, tree_margin)
    for tx, tz in trees:
        viewer.add(Tree(shader, tx, tz, terrain, tree_height))

    viewer.run()


if __name__ == '__main__':
    main(read_config())
