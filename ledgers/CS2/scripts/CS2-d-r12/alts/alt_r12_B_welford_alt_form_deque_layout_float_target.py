"""Alternative B: Welford with the (count-1)/count delta-squared form; list-with-head deques; float rank target plus 1e-9."""

from __future__ import annotations

import math
from bisect import insort


class WelfordAccumulator:
    def __init__(self) -> None:
        self._count = 0
        self._mean = 0.0
        self._m2 = 0.0

    def update(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("NaN")
        self._count += 1
        delta = x - self._mean
        self._m2 += delta * delta * (self._count - 1) / self._count
        self._mean += delta / self._count

    @property
    def count(self) -> int:
        return self._count

    def mean(self) -> float:
        if self._count == 0:
            raise ValueError("no values")
        return self._mean

    def variance(self, ddof: int = 1) -> float:
        if self._count == 0:
            raise ValueError("no values")
        if ddof == 1:
            if self._count < 2:
                raise ValueError("needs two values")
            return self._m2 / (self._count - 1)
        if ddof == 0:
            return self._m2 / self._count
        raise TypeError("ddof 0 or 1")


class RollingMinMax:
    def __init__(self, window: int) -> None:
        if window < 1:
            raise ValueError("window below one")
        if window != int(window):
            raise ValueError("window not whole")
        self._w = int(window)
        self._idx = 0
        self._mins: list[tuple[int, float]] = []
        self._head_min = 0
        self._maxs: list[tuple[int, float]] = []
        self._head_max = 0

    def push(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("NaN")
        i = self._idx
        self._idx += 1
        while len(self._mins) > self._head_min and self._mins[-1][1] >= x:
            self._mins.pop()
        self._mins.append((i, x))
        while len(self._maxs) > self._head_max and self._maxs[-1][1] <= x:
            self._maxs.pop()
        self._maxs.append((i, x))
        cut = i - self._w + 1
        while self._mins[self._head_min][0] < cut:
            self._head_min += 1
        while self._maxs[self._head_max][0] < cut:
            self._head_max += 1

    def minimum(self) -> float:
        if self._idx == 0:
            raise ValueError("nothing pushed")
        return self._mins[self._head_min][1]

    def maximum(self) -> float:
        if self._idx == 0:
            raise ValueError("nothing pushed")
        return self._maxs[self._head_max][1]


class QuantileSketch:
    def __init__(self, epsilon: float) -> None:
        if not (0.0 < epsilon < 1.0):
            raise ValueError("epsilon")
        self._eps = float(epsilon)
        self._xs: list[float] = []

    def add(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("NaN")
        insort(self._xs, float(x))

    def quantile(self, q: float) -> float:
        if not (0.0 <= q <= 1.0):
            raise ValueError("q")
        n = len(self._xs)
        if n == 0:
            raise ValueError("empty")
        target = max(1, math.ceil(q * n - self._eps * n + 1e-9))
        return self._xs[min(target, n) - 1]
