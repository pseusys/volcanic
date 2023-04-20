from math import sqrt, floor
from typing import Dict, Union

from sources.config import read_config
from sources.custom import terrain_generator
from sources.heat import Heat
from sources.objects import Terrain, Tree, Liquid, Ice, SkyBox, SkinnedCylinder
from sources.time import Chronograph
from sources.wrapper import Shader, Viewer
from sources.utils import laplacian_of_gaussian, conditional_random_points, square_extended, noise, rotate


def main(configs: Dict[str, Dict[str, Union[int, float]]]):
    viewer = Viewer(distance=configs["general"]["distance"])
    shader = Shader("shaders/phong.vert", "shaders/phong.frag")
    shader_map = Shader("shaders/phong_map.vert", "shaders/phong_map.frag")
    shader_water = Shader("shaders/phong.vert", "shaders/liquid.frag")
    shader_cubemap = Shader("shaders/cubemap.vert", "shaders/cubemap.frag")

    limit = configs["general"]["size_limit"]
    heat_state = configs["general"]["heat"]
    average = limit / 2

    laplacian_sigma = configs["terrain"]["laplacian_sigma"]
    sigma_radius = configs["terrain"]["sigma_radius"]

    island_radius = configs["terrain"]["island_radius"]

    tree_number = configs["trees"]["tree_number"]
    tree_margin = configs["trees"]["tree_margin"]
    tree_height = configs["trees"]["tree_height"]

    if average - min(tree_margin, average - island_radius) <= laplacian_sigma * sigma_radius and tree_number > 0:
        print(f"Configuration incorrect! No place for {tree_number} trees!")
        exit(1)

    ice_number = configs["ice"]["ice_number"]
    ice_margin = configs["ice"]["ice_margin"]

    if average - ice_margin <= island_radius and ice_number > 0:
        print(f"Configuration incorrect! No place for {ice_number} icebergs!")
        exit(1)

    heat = Heat(heat_state)
    chrono = Chronograph(heat_state, **configs["time"])
    viewer.add(SkyBox(average, shader_cubemap, "assets/sky_box/day_sky/day_sky", "bmp", "assets/sky_box/night_sky/night_sky", "png", chrono))
    viewer.set_time(chrono)

    generator = terrain_generator(
        lambda x, z: laplacian_of_gaussian(x, z, laplacian_sigma) - square_extended(x, z, shore_size=island_radius),
        lambda x, z: noise(x, z, configs["terrain"]["perlin_octaves"], configs["terrain"]["perlin_seed"]),
        limit,
        limit,
        configs["terrain"]["carrier_weight"],
        configs["terrain"]["perlin_weight"]
    )
    terrain = Terrain(shader_map, limit, limit, laplacian_sigma * sigma_radius, heat.terrain_colors, heat.terrain_shininess, generator)
    viewer.add(terrain)

    # TODO: correct radius, triangles maybe, rising lava?
    lava = Liquid(shader_water, "assets/lava_tex.png", "assets/lava_norm.png", laplacian_sigma * sigma_radius // 2, **configs["lava"], glowing=True)
    viewer.add(lava)

    water = Liquid(shader_water, "assets/water_tex.jpg", "assets/water_norm.jpg", round(average), **configs["water"], glowing=False)
    viewer.add(water)

    # Birds
    shader_wing = Shader("shaders/skinning.vert", "shaders/color.frag")
    wing_left = SkinnedCylinder(shader_wing)
    wing_right = SkinnedCylinder(shader_wing, transform=rotate((0, 1, 0), 180))   
    viewer.add(wing_left, wing_right)

    def in_sea(x: int, z: int) -> bool:
        return sqrt((x - average) ** 2 + (z - average) ** 2) > island_radius + ice_margin

    if heat.generate_ice:
        icebergs = conditional_random_points(ice_number, in_sea, limit - ice_margin, limit - ice_margin, ice_margin, ice_margin)
        for tx, tz in icebergs:
            viewer.add(Ice(shader, floor(tx - average), floor(tz - average), configs["water"]["height"]))

    def in_island(x: int, z: int) -> bool:
        return island_radius >= sqrt((x - average) ** 2 + (z - average) ** 2) > laplacian_sigma * sigma_radius

    trees = conditional_random_points(tree_number, in_island, limit - tree_margin, limit - tree_margin, tree_margin, tree_margin)
    for tx, tz in trees:
        viewer.add(Tree(shader, tx, tz, terrain, tree_height, color_map=heat.tree_colors))

    viewer.run()


if __name__ == '__main__':
    main(read_config())
