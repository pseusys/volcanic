import glfw
import numpy as np
from OpenGL import GL

from .terrain import Terrain
from ..wrapper import Shader, Mesh
from ..wrapper.texture import Texture, Textured


class Liquid(Textured):
    def __init__(self, shader: Shader, tex_file: str, radius: int, height: int, terrain: Terrain = None):
        base_coords = ((-radius, height, -radius), (radius, height, -radius), (radius, height, radius), (-radius, height, radius))
        resolution = np.array([radius, radius], dtype=np.uint32)
        indices = np.array((0, 2, 1, 0, 3, 2), dtype=np.uint32)

        uniforms = dict(resolution=resolution, amplitude=.01, center_shift=-1., speed=4., distortion=6., transparency=1.)
        attributes = dict(position=base_coords)
        mesh = Mesh(shader, attributes=attributes, index=indices, **uniforms)

        texture = Texture(tex_file)
        super().__init__(mesh, diffuse_map=texture)

    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        super().draw(primitives, **uniforms, time=glfw.get_time())
