from math import sqrt
from typing import Dict, Union

from perlin_noise import PerlinNoise

from sources.config import read_config
from sources.custom import terrain_generator
from sources.objects import Terrain, Tree, Liquid
from sources.wrapper import Shader, Viewer
from sources.utils import laplacian_of_gaussian, conditional_random_points, square_extended


def main(configs: Dict[str, Dict[str, Union[int, float]]]):
    viewer = Viewer(distance=configs["general"]["distance"])
    shader = Shader("shaders/phong.vert", "shaders/phong.frag")
    shader_map = Shader("shaders/phong_map.vert", "shaders/phong_map.frag")
    shader_water = Shader("shaders/liquid.vert", "shaders/liquid.frag")

    limit = configs["general"]["size_limit"]
    average = limit / 2

    noise = PerlinNoise(octaves=configs["terrain"]["perlin_octaves"])
    laplacian_sigma = configs["terrain"]["laplacian_sigma"]
    sigma_radius = configs["terrain"]["sigma_radius"]

    tree_number = configs["trees"]["tree_number"]
    tree_margin = configs["trees"]["tree_margin"]
    tree_height = configs["trees"]["tree_height"]

    if sqrt((average - tree_margin) ** 2) * 2 <= laplacian_sigma * sigma_radius and tree_number > 0:
        print(f"Configuration incorrect! No place for {tree_number} trees!")
        exit(1)

    generator = terrain_generator(
        lambda x, z: laplacian_of_gaussian(x, z, laplacian_sigma) - square_extended(x, z, weight=configs["terrain"]["carrier_weight"]),
        lambda x, z: noise([x, z]),
        limit,
        limit,
        configs["terrain"]["carrier_weight"],
        configs["terrain"]["perlin_weight"]
    )
    terrain = Terrain(shader_map, limit, limit, laplacian_sigma * sigma_radius, generator=generator)
    viewer.add(terrain)

    # TODO: correct radius, correct height, triangles maybe?
    lava = Liquid(shader_water, "assets/lava.png", laplacian_sigma * sigma_radius // 2, 10, center_shift=-1.)
    viewer.add(lava)

    # TODO: correct height
    water = Liquid(shader_water, "assets/water.jpg", round(average), -1, speed=5., transparency=.5, distortion=15.)
    viewer.add(water)

    def inside_volcano(x: int, z: int) -> bool:
        return sqrt((x - average) ** 2 + (z - average) ** 2) > laplacian_sigma * sigma_radius

    trees = conditional_random_points(tree_number, inside_volcano, limit - tree_margin, limit - tree_margin, tree_margin, tree_margin)
    for tx, tz in trees:
        viewer.add(Tree(shader, tx, tz, terrain, tree_height))

    viewer.run()


if __name__ == '__main__':
    main(read_config())
