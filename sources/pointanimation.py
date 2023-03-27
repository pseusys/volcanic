#!/usr/bin/env python3
import OpenGL.GL as GL                  # standard Python OpenGL wrapper
import glfw                             # lean window system wrapper for OpenGL
import numpy as np                      # all matrix manipulations & OpenGL args
from core import Shader, Viewer, Mesh   # import core classes
from math import sin                    # sinusoidal function used to animate


# -------------- Simple demo of a point animation -----------------------------
class PointAnimation(Mesh):
    """ Simple animated particle set """
    def __init__(self, shader):
        # render points with wide size to be seen
        GL.glPointSize(10)

        # instantiate and store 4 points to animate
        self.coords = ((-1, -1, -5), (1, -1, -5), (1, 1, -5), (-1, 1, -5))

        # send as position attribute to GPU, set uniform variable global_color.
        # GL_STREAM_DRAW tells OpenGL that attributes of this object
        # will change on a per-frame basis (as opposed to GL_STATIC_DRAW)
        super().__init__(shader, attributes=dict(position=self.coords),
                         usage=GL.GL_STREAM_DRAW, global_color=(0.5, 0.5, 0.8))

    def draw(self, primitives=GL.GL_POINTS, attributes=None, **uniforms):
        # compute a sinusoidal x-coord displacement, different for each point.
        # this could be any per-point function: build your own particle system!
        dp = [[sin(i + glfw.get_time()), 0, 0] for i in range(len(self.coords))]

        # update position buffer on CPU, send to GPU attribute to draw with it
        coords = np.array(self.coords, 'f') + np.array(dp, 'f')
        super().draw(primitives, attributes=dict(position=coords), **uniforms)

