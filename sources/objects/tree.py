from math import floor
import OpenGL.GL as GL
import numpy as np
import numpy.typing as npt

from .terrain import Terrain
from ..time import Chronograph
from ..wrapper import Shader, Mesh, Textured
from ..heat import Heat
from ..utils import empty_grid, lerp


_COLOR_MAP = np.array((.666, .333, 0), dtype=np.float64)


def _normalize(v):
    return v / np.linalg.norm(v)


class Tree(Mesh, Textured):
    _TREE_TOP_STEPS = 4  # TODO: implement with sphere
    _TREE_TOP_COLOR = np.array([(.0, 1., .0, 1.), (.0, .4, .0, 1.), (1., .4, .0, 1.), (.0, .0, .0, .0)], dtype=np.float64)

    def __init__(self, shader: Shader, x: int, z: int, terrain: Terrain, heat_state: float, chrono: Chronograph, height: float, radius: float = .3, color_map: npt.NDArray[np.float64] = _COLOR_MAP):
        self._chrono = chrono
        crone = np.array([1, 1, 1], dtype=np.uint64)
        
        direction = _normalize(terrain.get_normal(x, z))
        base = terrain.get_height(x, z)

        normals = [(1, 0, 1), (1, 0, -1), (-1, 0, 1), (-1, 0, -1)]
        position = [base + direction * height] + [base - (direction + normal) * radius * height / 3 for normal in normals]
        index = [0, 4, 3, 0, 3, 1, 0, 1, 2, 0, 2, 4]

        self._top_vertexes = 0
        if round(heat_state) == Heat.TEMPERATURES[0]:
            pass
        elif round(heat_state) == Heat.TEMPERATURES[1]:
            upper_normals = [(nx, 1, nz) for nx, _, nz in normals]
            lower_normals = [(nx, -1, nz) for nx, _, nz in normals]
            upper_vertexes = [position[0] + crone * un for un in upper_normals]
            lower_vertexes = [position[0] + crone * ln for ln in lower_normals]
            self._top_vertexes = len(upper_vertexes) + len(lower_vertexes)
            tops_indexes = [
                0, 1, 2, 2, 1, 3,
                4, 6, 5, 6, 7, 5,
                0, 4, 1, 1, 4, 5,
                5, 3, 1, 3, 5, 7,
                2, 3, 6, 6, 3, 7,
                2, 6, 0, 0, 6, 4,
            ]
            index += [x + len(position) for x in tops_indexes]
            normals += lower_normals + upper_normals
            position += upper_vertexes + lower_vertexes
        elif round(heat_state) == Heat.TEMPERATURES[2]:
            pass

        self._a = np.array(empty_grid(len(position), init=lambda: (1,)), dtype=np.float32)
        #self._k_a = np.array([_normalize(n) for n in normals], dtype=np.float32)
        #self._k_d = np.array(empty_grid(len(position), init=lambda: (0,)), dtype=np.float32)
        self._k_a = np.array(empty_grid(len(position), init=lambda: (0, 0, 0)), dtype=np.float32)
        self._k_d = np.array(empty_grid(len(position), init=lambda: color_map), dtype=np.float32)

        index = np.array(index, dtype=np.uint64)
        position = np.array(position, dtype=np.float64)
        normals = direction + np.array(normals, dtype=np.float64)

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
