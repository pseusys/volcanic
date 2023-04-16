import glfw
import numpy as np
from OpenGL import GL

from ..wrapper import Shader, Mesh
from ..wrapper.texture import Texture, Textured


class Liquid(Textured):
    def __init__(self, shader: Shader, tex_file):
        base_coords = ((0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0))
        scaled = 100 * np.array(base_coords, np.float32)
        indices = np.array((0, 1, 2, 0, 2, 3), np.uint32)

        uniforms = dict(resolution=np.array([128, 128], dtype=np.uint32))
        mesh = Mesh(shader, attributes=dict(position=scaled), index=indices, **uniforms)

        texture = Texture(tex_file)
        super().__init__(mesh, diffuse_map=texture)

    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        super().draw(primitives, **uniforms, time=glfw.get_time())
