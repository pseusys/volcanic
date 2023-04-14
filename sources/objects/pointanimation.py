#!/usr/bin/env python3
import OpenGL.GL as GL                  # standard Python OpenGL wrapper
import glfw                             # lean window system wrapper for OpenGL
import numpy as np   
from ..wrapper import Shader, Mesh                   # all matrix manipulations & OpenGL args
from math import sin                    # sinusoidal function used to animate
import random
import math


# -------------- Simple demo of a point animation -----------------------------
class PointAnimation(Mesh):
    """ Simple animated particle set """
    def __init__(self, shader):

        r = 5
        n = 10000
        # render points with wide size to be seen
        GL.glPointSize(1)

        self.coords = []

        for x in range(n): 
            z = random.uniform(-1,1)
            phi = random.uniform(0,0.999999)*2*np.pi
            x = np.sqrt(1 - z**2)*np.cos(phi)
            y = np.sqrt(1 - z**2)*np.sin(phi)
            self.coords.append([2* r* x,r* y + 28,r* 2 * z])

        # send as position attribute to GPU, set uniform variable global_color.
        # GL_STREAM_DRAW tells OpenGL that attributes of this object
        # will change on a per-frame basis (as opposed to GL_STATIC_DRAW)
        uniforms = dict(k_a=(0, 0, 0), k_d=(1, 1, 1), k_s=(0, 0, 0), s=42.)
      
        super().__init__(shader, attributes=dict(position=self.coords),
                         usage=GL.GL_STREAM_DRAW, global_color=(1, 1, 1), **uniforms)

    def draw(self, primitives=GL.GL_POINTS, attributes=None, **uniforms):

        # for index, x in enumerate(self.lifetime):
        #     if x <= 0.0: 
        #         x = random.uniform(1.0, 2.0)
        #         self.coords[index] = (0, 0, 0)

		# moving parameters for the particles
        dp = [[random.uniform(-10,10)* sin(0.3*(random.uniform(-5,5) + glfw.get_time())), 0.5* sin(0.3*(random.uniform(-5,5) + glfw.get_time())), random.uniform(-10,10)*sin(0.3*(random.uniform(-5,5)+ glfw.get_time()))] for i in range(len(self.coords))]
       # delta_time = [(-0.1) for _ in range(len(self.coords))]
        # update position buffer on CPU, send to GPU attribute to draw with it
       # self.lifetime = np.array(self.lifetime, 'f') +  np.array(delta_time, 'f')
        coords = np.array(self.coords, 'f') + np.array(dp, 'f')

        super().draw(primitives, attributes=dict(position=coords), **uniforms)

