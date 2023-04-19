from math import floor
import OpenGL.GL as GL
import numpy as np
import numpy.typing as npt

from .terrain import Terrain
from ..time import Chronograph
from ..wrapper import Shader, Mesh, Textured
from ..heat import Heat
from ..utils import lerp, straight_angle_rotor


_COLOR_MAP = np.array((.666, .333, 0), dtype=np.float64)


def _normalize(vector: npt.NDArray[np.float64]):
    return vector / np.linalg.norm(vector)


class Tree(Mesh, Textured):
    _TREE_TOP_STEPS = 4  # TODO: implement with sphere
    _TREE_TOP_COLOR = np.array([(.0, 1., .0, 1.), (.0, .4, .0, 1.), (1., .4, .0, 1.), (.0, .0, .0, .0)], dtype=np.float64)

    def __init__(self, shader: Shader, x: int, z: int, terrain: Terrain, heat_state: float, chrono: Chronograph, height: float, radius: float = 1., circle: float = 3., color_map: npt.NDArray[np.float64] = _COLOR_MAP, **_):
        self._chrono = chrono
        base = terrain.get_position(x, z)
        direction = _normalize(terrain.get_normal(x, z))

        normals = straight_angle_rotor(direction)
        position = [base + direction * height] + [(base + normal * radius) for normal in normals]
        index = [0, 4, 1, 0, 1, 2, 0, 2, 3, 0, 3, 4]

        self._top_vertexes = 0
        if round(heat_state) == Heat.TEMPERATURES[0]:
            pass
        elif round(heat_state) == Heat.TEMPERATURES[1]:
            crone_positions = [(position[0] + normal * circle) for normal in normals]
            upper_positions = [pos + direction * circle for pos in crone_positions]
            lower_positions = [pos - direction * circle for pos in crone_positions]
            self._top_vertexes = len(upper_positions) + len(lower_positions)
            tops_indexes = [
                3, 0, 2, 2, 0, 1,
                5, 4, 6, 6, 4, 7,
                7, 4, 3, 3, 4, 0,
                4, 5, 0, 0, 5, 1,
                5, 6, 1, 1, 6, 2,
                6, 7, 2, 2, 7, 3
            ]
            index += [x + len(position) for x in tops_indexes]
            normals += [_normalize(pos - base - direction) for pos in upper_positions + lower_positions]
            position += upper_positions + lower_positions
        elif round(heat_state) == Heat.TEMPERATURES[2]:
            pass

        index = np.array(index, dtype=np.uint64)
        position = np.array(position, dtype=np.float64)
        normals = np.append([direction], normals, axis=0)

        self._a = np.array([(1,) for _ in range(len(position))], dtype=np.float32)
        self._k_a = np.array([(0, 0, 0) for _ in range(len(position))], dtype=np.float32)
        self._k_d = np.array([color_map for _ in range(len(position))], dtype=np.float32)

        attributes = dict(position=position, normal=normals, k_a=self._k_a, k_d=self._k_d, a=self._a)
        Mesh.__init__(self, shader, index=index, attributes=attributes)
        # Textured.__init__(self, mesh, surface=Texture(texture_file), normal=Texture(normal_file))

    def draw(self, primitives=GL.GL_TRIANGLES, attributes=None, **uniforms):
        attributes = dict() if attributes is None else attributes
        current_season = (self._chrono.season - .5) if self._chrono.season - .5 > 0 else (3 + self._chrono.season - .5)
        next_season = (self._chrono.season + .5) if self._chrono.season + .5 < 3 else (3 - self._chrono.season - .5)
        fraction = current_season - floor(current_season)

        previous_color = self._TREE_TOP_COLOR[floor(current_season)][:-1]
        next_color = self._TREE_TOP_COLOR[floor(next_season)][:-1]
        season_color = lerp(previous_color, next_color, fraction)

        previous_alpha = self._TREE_TOP_COLOR[floor(current_season)][-1]
        next_alpha = self._TREE_TOP_COLOR[floor(next_season)][-1]
        season_alpha = lerp(previous_alpha, next_alpha, fraction)

        for i in range(len(self._k_a) - self._top_vertexes, len(self._k_a)):
            self._k_d[i] = season_color
            self._a[i] = (season_alpha,)

        attributes = dict(**attributes, k_a=self._k_a, k_d=self._k_d, a=self._a)
        Mesh.draw(self, primitives, attributes, **uniforms)
