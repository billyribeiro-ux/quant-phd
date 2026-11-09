"""Alternative A: stores every value in a sorted list; mean and variance by fsum; rank target floor(qn - eps n) + 1."""

from __future__ import annotations

import math
from bisect import insort
from fractions import Fraction


class WelfordAccumulator:
    def __init__(self) -> None:
        self._xs: list[float] = []

    def update(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number")
        self._xs.append(x)

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
            raise TypeError("ddof must be 0 or 1")
        if ddof == 1 and len(self._xs) < 2:
            raise ValueError("needs two values")
        m = self.mean()
        ss = math.fsum((x - m) ** 2 for x in self._xs)
        return ss / len(self._xs) if ddof == 0 else ss / (len(self._xs) - 1)


class RollingMinMax:
    def __init__(self, window: int) -> None:
        if window < 1:
            raise ValueError("window below one")
        if window != int(window):
            raise ValueError("window not whole")
        self._w = window
        self._xs: list[float] = []

    def push(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("NaN pushed")
        self._xs.append(x)

    def minimum(self) -> float:
        if not self._xs:
            raise ValueError("nothing pushed")
        return min(self._xs[-self._w :])

    def maximum(self) -> float:
        if not self._xs:
            raise ValueError("nothing pushed")
        return max(self._xs[-self._w :])


class QuantileSketch:
    def __init__(self, epsilon: float) -> None:
        if not (0.0 < epsilon < 1.0):
            raise ValueError("epsilon outside (0, 1)")
        self._eps = Fraction(epsilon)
        self._sorted: list[float] = []

    def add(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("NaN added")
        insort(self._sorted, float(x))

    def quantile(self, q: float) -> float:
        if not (0.0 <= q <= 1.0):
            raise ValueError("q outside [0, 1]")
        n = len(self._sorted)
        if n == 0:
            raise ValueError("empty sketch")
        target = max(1, math.floor(Fraction(q) * n - self._eps * n) + 1)
        return self._sorted[min(target, n) - 1]
