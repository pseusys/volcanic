import numpy as np
from ..wrapper.mesh import Mesh


class Cube(Mesh):
    """ Class for drawing a cube object """

    def __init__(self, shader, c):
        # TODO: this is still a triangle, new values needed for Cube
        vertexes = ((c[0] - .5, c[1] + .5, c[2] - .5), (c[0] + .5, c[1] + .5, c[2] - .5), (c[0] + .5, c[1] + .5, c[2] + .5), (c[0] - .5, c[1] + .5, c[2] + .5), (c[0] - .5, c[1] - .5, c[2] - .5), (c[0] + .5, c[1] - .5, c[2] - .5), (c[0] + .5, c[1] - .5, c[2] + .5), (c[0] - .5, c[1] - .5, c[2] + .5))
        top_pane = (0, 3, 2, 2, 1, 0)
        front_pane = (0, 1, 5, 5, 4, 0)
        right_pane = (1, 2, 6, 6, 5, 1)
        back_pane = (3, 7, 6, 6, 2, 3)
        left_pane = (0, 4, 7, 7, 3, 0)
        bottom_pane = (4, 5, 6, 6, 7, 4)
        position = np.array(vertexes, 'f')
        color = np.array(((1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1)), 'f')

        index = np.array(top_pane + front_pane + right_pane + back_pane + left_pane + bottom_pane, np.uint32)
        attributes = dict(position=position, color=color)

        super().__init__(shader, index=index, attributes=attributes)
