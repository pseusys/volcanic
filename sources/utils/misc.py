from typing import Callable, List


def empty_grid(x: int, z: int, init: Callable = lambda: None) -> List:
    return [init() for _ in range(x * z)]
