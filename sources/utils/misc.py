from random import randint
from typing import Callable, List, Tuple


def empty_grid(total: int = -1, x: int = -1, z: int = -1, init: Callable = lambda: None) -> List:
    if total == x == z == -1:
        raise Exception("All parameters of grid shouldn't be equal -1!")
    return [init() for _ in range(total if total != -1 else x * z)]


def conditional_random_points(size: int, condition: Callable[[int, int], bool], ux: int = 0, uz: int = 0, lx: int = 10, lz: int = 10) -> List[Tuple[int, int]]:
    result = list()
    while len(result) < size:
        newcomer_x, newcomer_z = randint(lx, ux), randint(lz, uz)
        if condition(newcomer_x, newcomer_z):
            result += [(newcomer_x, newcomer_z)]
    return result
