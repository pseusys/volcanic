from typing import Callable, List


def empty_grid(total: int = -1, x: int = -1, z: int = -1, init: Callable = lambda: None) -> List:
    if total == x == z == -1:
        raise Exception("All parameters of grid shouldn't be equal -1!")
    return [init() for _ in range(total if total != -1 else x * z)]
