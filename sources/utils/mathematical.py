import numpy as np


def triangle_normal(v1, v2, v3):
    v1 = np.array(v1, dtype=np.float64)
    norm = np.cross(np.array(v2, dtype=np.float64) - v1, np.array(v3, dtype=np.float64) - v1)
    return norm / np.linalg.norm(norm)
