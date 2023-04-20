#!/usr/bin/env python3

# Python built-in modules
import sys

# External, non built-in modules
import numpy as np                  # all matrix manipulations & OpenGL args
from sources.utils import identity,sincos, quaternion_from_euler, quaternion, quaternion_slerp, quaternion_matrix, translate, scale
from sources.wrapper import KeyFrameControlNode, Skinned, Shader, Mesh, Viewer, load



# -------------- Deformable Cylinder Mesh  ------------------------------------
class SkinnedCylinder(KeyFrameControlNode):
    """ Deformable cylinder """
    def __init__(self, shader, sections=11, quarters=20, trans=(0,0,0), transform=identity()):
        forearm = KeyFrameControlNode(
            {0: (0, 0, 0)},
            {0: quaternion(), 2: quaternion_from_euler(90), 4: quaternion()},
            {0: 1}, transform=translate(10, 0, 0))
        
        hand = KeyFrameControlNode(
            {0: (sections/2 - 1, 0, 0)},    # translation to the forearm extremity
            {0: quaternion(), 2: quaternion_from_euler(45), 4: quaternion()},
            {0: 1}, transform=translate(-10, 0, 0))   
            
        # this "arm" node and its transform serves as control node for bone 0
        # we give it the default identity keyframe transform, doesn't move
        super().__init__({0: trans}, {0: quaternion()}, {0: 1}, transform=transform)
        self.add(forearm)
        forearm.add(hand)
    
        # there are three bones in this animation corresponding to above noes
        bone_nodes = [self, self.children[0],  self.children[0].children[0]]

        # these bones have no particular offset transform
        bone_offsets = [identity(), identity(), identity()]

        # vertices, per vertex bone_ids and weights
       
        vertices, faces, bone_id, bone_weights = [], [], [], []
        for x_c in range(sections+1):
            for angle in range(quarters):
                # compute vertex coordinates sampled on a cylinder
                z_c, y_c = sincos(360 * angle / quarters)
                if x_c <= sections:
                    vertices.append((x_c - sections/2, y_c, z_c))
                else:
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
