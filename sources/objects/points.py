import random
from math import pi, sin, cos
from typing import Tuple

import glfw
import numpy as np
from OpenGL import GL

from ..utils import lerp
from ..wrapper import Mesh, Shader


class PointAnimation(Mesh):
    _WIDESPREAD = .6

    def __init__(self, shader: Shader, lower: int, higher: int, number: int = 2, size: int = 1, thin: float = .1, thick: float = 2.):
        GL.glPointSize(size)
        self.lower = lower
        self.higher = higher
        self.number = number

        self.coords = list()
        self.rotors = list()

        for x in range(number):
            rotor = random.uniform(thin, thick)
            y = random.uniform(lower, higher)
            x, z = self._fog_position(y, rotor)
            self.coords += [(x, y, z)]
            self.rotors += [rotor]

        uniforms = dict(k_a=(0, 0, 0), k_d=(1, 1, 1), k_s=(0, 0, 0), s=42.) 
        super().__init__(shader, attributes=dict(position=self.coords), usage=GL.GL_STREAM_DRAW, **uniforms)

    def draw(self, primitives=GL.GL_POINTS, attributes=None, **uniforms):
        attributes = dict() if attributes is None else attributes

        differences = list()
        for idx, (_, y, __) in enumerate(self.coords):
            ny = y + idx / self.number * 10
            nx, nz = self._fog_position(ny, self.rotors[idx])
            differences += [nx, ny, nz]

        self.coords = differences
        super().draw(primitives, attributes=dict(position=self.coords), **uniforms)

    def _fog_position(self, y: float, rotor: float) -> Tuple[float, float]:
        height = lerp(0, 100, (y - self.lower) / (self.higher - self.lower))
        #print(y, height, (y - self.lower) / (self.higher - self.lower))
        plain = rotor * sin(height) * height ** self._WIDESPREAD
        #print(plain, cos(plain), sin(plain))
        return plain, plain

