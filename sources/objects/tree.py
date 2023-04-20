from math import floor
import OpenGL.GL as GL
import numpy as np
import numpy.typing as npt

from .terrain import Terrain
from ..time import Chronograph
from ..wrapper import Shader, Mesh, Textured, Node
from ..heat import Heat
from ..utils import MeshedNode, lerp, straight_angle_rotor, translate, identity


_COLOR_MAP = np.array((.666, .333, 0), dtype=np.float64)


def _normalize(vector: npt.NDArray[np.float64]):
    return vector / np.linalg.norm(vector)


class EmptyTree(MeshedNode):
    def __init__(self, shader: Shader, x: int, z: int, terrain: Terrain, chrono: Chronograph, height: float, radius: float = 1., color_map: npt.NDArray[np.float64] = _COLOR_MAP, transform=identity(), **_):
        self.chrono = chrono
        self.base = terrain.get_position(x, z)
        self.direction = _normalize(terrain.get_normal(x, z))

        self.rotor = straight_angle_rotor(self.direction)
        self.normals = [self.direction] + self.rotor
        self.position = [self.base + self.direction * height] + [(self.base + normal * radius) for normal in self.rotor]
        self.index = [0, 4, 1, 0, 1, 2, 0, 2, 3, 0, 3, 4]

        self._a = np.array([(1,) for _ in range(len(self.position))], dtype=np.float32)
        self._k_a = np.array([(0, 0, 0) for _ in range(len(self.position))], dtype=np.float32)
        self._k_d = np.array([color_map for _ in range(len(self.position))], dtype=np.float32)

        attributes = dict(position=self.position, normal=self.normals, k_a=self._k_a, k_d=self._k_d, a=self._a)
        super().__init__(shader, tuple(), transform, attributes=attributes, index=self.index)

    @property
    def top(self) -> npt.NDArray[np.float64]:
        return self.position[0]

    def draw(self, primitives=GL.GL_TRIANGLES, attributes=None, **uniforms):
        attributes = dict() if attributes is None else attributes
        attributes = dict(**attributes, k_a=self._k_a, k_d=self._k_d, a=self._a)
        super().draw(primitives, attributes, **uniforms)


class ColdTree(EmptyTree):
    def __init__(self, shader: Shader, x: int, z: int, terrain: Terrain, chrono: Chronograph, height: float, radius: float = 1., color_map: npt.NDArray[np.float64] = _COLOR_MAP, transform=identity(), **_):
        super().__init__(shader, x, z, terrain, chrono, height, radius, color_map, transform)

        for rot in self.rotor:
            # TODO: transpose (transpose tree and ice)
            twig = EmptyTree(shader, 10, 10, terrain, chrono, height, radius, color_map)  # , transform=translate(rot + self.base + self.direction)
            self.add(twig)


class MediumTree(MeshedNode):
    _TREE_TOP_STEPS = 4  # TODO: implement with sphere
    _TREE_TOP_COLOR = np.array([(.0, 1., .0, 1.), (.0, .4, .0, 1.), (1., .4, .0, 1.), (.0, .0, .0, .0)], dtype=np.float64)

    def __init__(self, shader: Shader, x: int, z: int, terrain: Terrain, chrono: Chronograph, height: float, radius: float = 1., circle: float = 3., color_map: npt.NDArray[np.float64] = _COLOR_MAP, transform=identity(), **_):
        parent = EmptyTree(shader, x, z, terrain, chrono, height, radius, color_map)
        self._parent = parent

        circle_positions = [(parent.top + normal * circle) for normal in parent.rotor]
        upper_positions = [pos + parent.direction * circle for pos in circle_positions]
        lower_positions = [pos - parent.direction * circle for pos in circle_positions]
        normals = [_normalize(pos - parent.base - parent.direction) for pos in upper_positions + lower_positions]
        position = upper_positions + lower_positions
        index = [
            3, 0, 2, 2, 0, 1,
            5, 4, 6, 6, 4, 7,
            7, 4, 3, 3, 4, 0,
            4, 5, 0, 0, 5, 1,
            5, 6, 1, 1, 6, 2,
            6, 7, 2, 2, 7, 3
        ]

        self._a = np.array([(1,) for _ in range(len(position))], dtype=np.float32)
        self._k_a = np.array([(0, 0, 0) for _ in range(len(position))], dtype=np.float32)
        self._k_d = np.array([color_map for _ in range(len(position))], dtype=np.float32)

        attributes = dict(position=position, normal=normals, k_a=self._k_a, k_d=self._k_d, a=self._a)
        super().__init__(shader, tuple(), transform, attributes=attributes, index=index)
        # TODO: transpose
        self.add(parent)

    def draw(self, primitives=GL.GL_TRIANGLES, attributes=None, **uniforms):
        attributes = dict() if attributes is None else attributes
        current_season = (self._parent.chrono.season - .5) if self._parent.chrono.season - .5 > 0 else (3 + self._parent.chrono.season - .5)
        next_season = (self._parent.chrono.season + .5) if self._parent.chrono.season + .5 < 3 else (3 - self._parent.chrono.season - .5)
        fraction = current_season - floor(current_season)

        previous_color = self._TREE_TOP_COLOR[floor(current_season)][:-1]
        next_color = self._TREE_TOP_COLOR[floor(next_season)][:-1]
        season_color = lerp(previous_color, next_color, fraction)

        previous_alpha = self._TREE_TOP_COLOR[floor(current_season)][-1]
        next_alpha = self._TREE_TOP_COLOR[floor(next_season)][-1]
        season_alpha = lerp(previous_alpha, next_alpha, fraction)

        for i in range(len(self._k_a)):
            self._k_d[i] = season_color
            self._a[i] = (season_alpha,)

        attributes = dict(**attributes, k_a=self._k_a, k_d=self._k_d, a=self._a)
        super().draw(primitives, attributes, **uniforms)



def Tree(*args, heat_state: float, **kwargs):
    if round(heat_state) == Heat.TEMPERATURES[0]:
        return ColdTree(*args, **kwargs)
    elif round(heat_state) == Heat.TEMPERATURES[1]:
        return MediumTree(*args, **kwargs)
    elif round(heat_state) == Heat.TEMPERATURES[2]:
        pass
    else:
        return EmptyTree(*args, **kwargs)
