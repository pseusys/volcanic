from math import sin, pi, cos

import numpy as np

from sources.heat import Heat


class Chronograph:
    SEASON_LENGTH = 91
    YEAR_LENGTH = 364

    def __init__(self, heat_state: float, sun_bias: float = 1., init_day: float = SEASON_LENGTH, day_length: float = 10):
        self._day_length = day_length
        self._global_time = init_day
        self._winter_bias = (Heat.TEMPERATURES[-1] - heat_state) * sun_bias

    @property
    def time(self):
        return self._global_time % self._day_length

    @property
    def day(self):
        return self._global_time // self._day_length

    @property
    def season(self):
        return self._global_time // (self.SEASON_LENGTH * self._day_length)

    @property
    def year(self):
        return self._global_time // (self.YEAR_LENGTH * self._day_length)

    @property
    def sun_position(self):
        fraction = sin(pi * self._global_time / (self.YEAR_LENGTH * self._day_length))
        bias = abs(fraction) * self._winter_bias
        escalation = pi * self._global_time / self._day_length
        return np.array([bias, cos(escalation), sin(escalation)], dtype=np.float64)

    @staticmethod
    def _tri_saw(fraction: float, maximum: float = 1.) -> float:
        if fraction < maximum / 2:
            return fraction / (maximum / 2)
        else:
            return (maximum - fraction) / (maximum / 2)

    def update(self, global_time: float):
        self._global_time = global_time
