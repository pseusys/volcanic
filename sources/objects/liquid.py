import glfw
import numpy as np
from OpenGL import GL

from ..wrapper import Shader, Mesh
from ..wrapper.texture import Texture, Textured


class Liquid(Textured):
    def __init__(self, shader: Shader, tex_file: str, radius: int, height: int, amplitude=.01, center_shift=0, speed=4., distortion=6., transparency=1., glowing=False, shininess=.1):
        positions = [(-radius, height, -radius), (radius, height, -radius), (radius, height, radius), (-radius, height, radius)]
        normals = [(0, 1, 0) for _ in positions]
        resolution = np.array([radius, radius], dtype=np.uint32)
        indices = np.array((0, 2, 1, 0, 3, 2), dtype=np.uint32)

        colors = dict(k_a=(0, 0, 0), k_d=(0, 0, 0), k_s=(1, 1, 1), s=shininess)
        uniforms = dict(resolution=resolution, amplitude=amplitude, center_shift=center_shift, speed=speed, distortion=distortion, transparency=transparency, glowing=glowing)
        attributes = dict(position=positions, normal=normals)
        mesh = Mesh(shader, attributes=attributes, index=indices, **uniforms, **colors)

        texture = Texture(tex_file)
        super().__init__(mesh, diffuse_map=texture)

    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        super().draw(primitives, **uniforms, time=glfw.get_time())
