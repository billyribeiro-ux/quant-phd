"""Alternative B: Welford with the M2 increment written as (n-1)delta^2/n, deque with a head pointer, exact sketch with target floor(qn)+1 clamped to n."""

from __future__ import annotations

import math
from bisect import insort
from fractions import Fraction


class WelfordAccumulator:
    def __init__(self) -> None:
        self._n = 0
        self._mean = 0.0
        self._m2 = 0.0

    def update(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("nan")
        x = float(x)
        self._n += 1
        delta = x - self._mean
        self._mean += delta / self._n
        self._m2 += (self._n - 1) * delta * delta / self._n

    @property
    def count(self) -> int:
        return self._n

    def mean(self) -> float:
        if self._n == 0:
            raise ValueError("no values")
        return self._mean

    def variance(self, ddof: int = 1) -> float:
        if self._n == 0:
            raise ValueError("no values")
        if ddof == 0:
            return self._m2 / self._n
        if ddof == 1:
            if self._n < 2:
                raise ValueError("need two values")
            return self._m2 / (self._n - 1)
        raise ValueError("ddof must be 0 or 1")


class RollingMinMax:
    def __init__(self, window: int) -> None:
        if window < 1:
            raise ValueError("window")
        self._w = window
        self._i = -1
        self._mins: list[tuple[int, float]] = []
        self._maxs: list[tuple[int, float]] = []
        self._mh = 0
        self._xh = 0

    def push(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("nan")
        x = float(x)
        self._i += 1
        while len(self._mins) > self._mh and self._mins[-1][1] >= x:
            self._mins.pop()
        self._mins.append((self._i, x))
        while len(self._maxs) > self._xh and self._maxs[-1][1] <= x:
            self._maxs.pop()
        self._maxs.append((self._i, x))
        while self._mins[self._mh][0] <= self._i - self._w:
            self._mh += 1
        while self._maxs[self._xh][0] <= self._i - self._w:
            self._xh += 1

    def minimum(self) -> float:
        if self._i < 0:
            raise ValueError("empty")
        return self._mins[self._mh][1]

    def maximum(self) -> float:
        if self._i < 0:
            raise ValueError("empty")
        return self._maxs[self._xh][1]


class QuantileSketch:
    def __init__(self, epsilon: float) -> None:
        if not (0.0 < epsilon < 1.0):
            raise ValueError("epsilon")
        self._eps = Fraction(epsilon)
        self._xs: list[float] = []

    def add(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("nan")
        insort(self._xs, float(x))

    def quantile(self, q: float) -> float:
        if not (0.0 <= q <= 1.0):
            raise ValueError("q")
        n = len(self._xs)
        if n == 0:
            raise ValueError("empty")
        k = min(n, math.floor(Fraction(q) * n) + 1)
        return self._xs[k - 1]
