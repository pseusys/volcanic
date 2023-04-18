import random
from math import pi, sin, cos
from typing import Tuple

import glfw
import numpy as np
from OpenGL import GL

from ..utils import lerp
from ..wrapper import Mesh, Shader


class Smoke(Mesh):
    _WIDESPREAD = .6
    
    def __init__(self, shader: Shader, lower: int, higher: int, number: int = 1000, size: int = 2, thin: float = .5, thick: float = 1.):
        GL.glPointSize(size)
        self.lower = lower
        self.higher = higher
        self.number = number
        self.flight = 25

        self.coords = list()
        self.speeds = list()
        self.ascends = list()
        self.heights = list()
        self.rotors = list()

        for x in range(number): 
            rotor = random.uniform(thin, thick)
            height = 0
            ascend = random.uniform(1, 10) * 10
            speed = random.uniform(1, 5)
            x, z = self._fog_position(height, rotor, ascend)
            self.heights += [height]
            self.speeds += [speed]
            self.ascends += [ascend]
            self.coords += [(x * self.flight, lerp(lower, higher, height), z * self.flight)]
            self.rotors += [rotor]

        uniforms = dict(k_a=(0, 0, 0), k_d=(1, 1, 1), k_s=(0, 0, 0), s=42.) 
        attributes = dict(position=np.array(self.coords, dtype=np.float32))
        super().__init__(shader, attributes=attributes, usage=GL.GL_STREAM_DRAW, **uniforms)

    def draw(self, primitives=GL.GL_POINTS, attributes=None, **uniforms):
        attributes = dict() if attributes is None else attributes

        for i in range(self.number):
            self.heights[i] = (self.heights[i] + .001 * self.speeds[i]) % 1
            nx, nz = self._fog_position(self.heights[i], self.rotors[i], self.ascends[i])
            self.coords[i] = [(nx * self.flight, lerp(self.lower, self.higher, self.heights[i]), nz * self.flight)]

        attributes = dict(**attributes, position=np.array(self.coords, dtype=np.float32))
        super().draw(primitives, attributes=attributes, **uniforms)

    def _fog_position(self, height: float, rotor: float, ascend: float) -> Tuple[float, float]:
        multi = rotor * height ** self._WIDESPREAD
        return multi * sin(height * ascend), multi * cos(height * ascend)
