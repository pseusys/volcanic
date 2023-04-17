from math import exp, pi, sqrt

import numpy as np


def triangle_normal(v1, v2, v3):
    v1 = np.array(v1, dtype=np.float64)
    norm = np.cross(np.array(v2, dtype=np.float64) - v1, np.array(v3, dtype=np.float64) - v1)
    return norm / np.linalg.norm(norm)


def laplacian_of_gaussian(x: float, z: float, sigma: float = 1., width: float = .3, height: float = 20., flatness: float = 100.) -> float:
    term = -width * (x ** 2 + z ** 2) / (2 * sigma ** 2)
    return -(1 + term * height) * exp(term) / (pi * sigma ** 4) * flatness


def sign(x: float):
    return 1 if x > 0 else -1


def square_extended(x: float, z: float, shore_size: int = 40., dive: int = 50.) -> float:
    dist = sqrt(x ** 2 + z ** 2)
    return sqrt(max(dist - shore_size, 0)) / dive
