from math import floor


def noise(x: int, y: int, octaves: int = 15) -> float:
    coords = [x * octaves, y * octaves]
    bounds = [(floor(coord), floor(coord + 1)) for coord in coords]
    return ...
