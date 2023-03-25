#!/usr/bin/env python3

# Python built-in modules
import sys

# External, non built-in modules
import numpy as np                  # all matrix manipulations & OpenGL args

from transform import identity, sincos, quaternion, quaternion_from_euler
from core import Shader, Mesh, Viewer, load
from animation import KeyFrameControlNode, Skinned


# -------------- Deformable Cylinder Mesh  ------------------------------------
class SkinnedCylinder(KeyFrameControlNode):
    """ Deformable cylinder """
    def __init__(self, shader, sections=11, quarters=20):
        forearm = KeyFrameControlNode(
            {0: (0, 0, 0)},
            {0: quaternion(), 2: quaternion_from_euler(90), 4: quaternion()},
            {0: 1})
        hand = KeyFrameControlNode(
            {0: (sections/2 - 1, 0, 0)},    # translation to the forearm extremity
            {0: quaternion(),
            2: quaternion_from_euler(45),  # rotation around the origin
            4: quaternion()},
            {0: 1})                         # no scaling here

        # this "arm" node and its transform serves as control node for bone 0
        # we give it the default identity keyframe transform, doesn't move
        super().__init__({0: (0, 0, 0)}, {0: quaternion()}, {0: 1})

        # we add a son "forearm" node with animated rotation for the second
        # part of the cylinder
        self.add(forearm)

        # we add a son "arm" node with animated rotation for the third
        # part of the cylinder
        forearm.add(hand)
    

        # there are two bones in this animation corresponding to above noes
        bone_nodes = [self, self.children[0], forearm.children[0]]

        # these bones have no particular offset transform
        # TODO here we need to change something
        bone_offsets = [identity(), identity(), identity()]

        # vertices, per vertex bone_ids and weights
        vertices, faces, bone_id, bone_weights = [], [], [], []
        for x_c in range(sections+1):
            for angle in range(quarters):
                # compute vertex coordinates sampled on a cylinder
                z_c, y_c = sincos(360 * angle / quarters)
                if x_c < sections-1:
                    vertices.append((x_c - sections/2, y_c, z_c))
                else:
                # hand: last two x coords become 0, 1
                # (later translated by the KeyFrameControlNode)
                    vertices.append((x_c - sections + 1, y_c, z_c))
                

                # the index of the 4 prominent bones influencing this vertex.
                # since in this example there are only 2 bones, every vertex
                # is influenced by the two only bones 0 and 1
                bone_id.append((0, 1, 2, 0))

                # per-vertex weights for the 4 most influential bones given in
                # a vec4 vertex attribute. Not using indices 2 & 3 => 0 weight
                # vertex weight is currently a hard transition in the middle
                # of the cylinder
                #linear variation
                weight = np.clip(1-(2*x_c/sections-1/2), 0, 1)
                bone_weights.append((weight, 1 - weight, 0, 0))

        # face indices
        faces = []
        for x_c in range(sections):
            for angle in range(quarters):

                # indices of the 4 vertices of the current quad, % helps
                # wrapping to finish the circle sections
                ir0c0 = x_c * quarters + angle
                ir1c0 = (x_c + 1) * quarters + angle
                ir0c1 = x_c * quarters + (angle + 1) % quarters
                ir1c1 = (x_c + 1) * quarters + (angle + 1) % quarters

                # add the 2 corresponding triangles per quad on the cylinder
                faces.extend([(ir0c0, ir0c1, ir1c1), (ir0c0, ir1c1, ir1c0)])

        # the skinned mesh itself. it doesn't matter where in the hierarchy
        # this is added as long as it has the proper bone_node table
        attributes = dict(position=vertices, normal=bone_weights,
                          bone_ids=bone_id, bone_weights=bone_weights)
        mesh = Mesh(shader, attributes=attributes, index=faces)
        self.add(Skinned(mesh, bone_nodes, bone_offsets))


# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()
    shader = Shader("skinning.vert", "color.frag")

    if len(sys.argv) < 2:
        print('Cylinder skinning demo.')
        print('Note:\n\t%s [3dfile]*\n\n3dfile\t\t the filename of a model in'
              ' format supported by assimp.' % sys.argv[0])
        viewer.add(SkinnedCylinder(shader))
    else:
        viewer.add(*[m for file in sys.argv[1:] for m in load(file, shader)])

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped
