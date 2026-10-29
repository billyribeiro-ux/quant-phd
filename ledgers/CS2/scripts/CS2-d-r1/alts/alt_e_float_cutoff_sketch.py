"""Alternative E: as alternative A, but the sketch rank target ceil(q*n - eps*n) is computed in 64-bit floats, not exact fractions."""

from __future__ import annotations

import math
from bisect import insort
from fractions import Fraction


class WelfordAccumulator:
    def __init__(self) -> None:
        self._xs: list[float] = []

    def update(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("nan")
        self._xs.append(float(x))

    @property
    def count(self) -> int:
        return len(self._xs)

    def mean(self) -> float:
        if not self._xs:
            raise ValueError("no values")
        return math.fsum(self._xs) / len(self._xs)

    def variance(self, ddof: int = 1) -> float:
        if not self._xs:
            raise ValueError("no values")
        if ddof not in (0, 1):
            raise ValueError("ddof")
        if ddof == 1 and len(self._xs) < 2:
            raise ValueError("need two values")
        m = self.mean()
        ss = sum((x - m) * (x - m) for x in self._xs)
        return ss / (len(self._xs) - ddof)


class RollingMinMax:
    def __init__(self, window: int) -> None:
        if window < 1:
            raise ValueError("window")
        self._w = window
        self._xs: list[float] = []

    def push(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("nan")
        self._xs.append(float(x))

    def minimum(self) -> float:
        if not self._xs:
            raise ValueError("empty")
        return min(self._xs[-self._w :])

    def maximum(self) -> float:
        if not self._xs:
            raise ValueError("empty")
        return max(self._xs[-self._w :])


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
        k = max(1, math.ceil(q * n - float(self._eps) * n))
        return self._xs[min(k, n) - 1]
