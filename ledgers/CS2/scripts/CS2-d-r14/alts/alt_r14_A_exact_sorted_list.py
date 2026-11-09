"""Alternative A (correct): every value kept in a sorted list, exact Fraction target, brute-force window."""

from __future__ import annotations

import math
from bisect import bisect_right, insort
from fractions import Fraction


class WelfordAccumulator:
    def __init__(self) -> None:
        self._count = 0
        self._sum = Fraction(0)
        self._sumsq = Fraction(0)
        self._xs: list[Fraction] = []

    def update(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be added")
        fx = Fraction(x)
        self._count += 1
        self._sum += fx
        self._xs.append(fx)

    @property
    def count(self) -> int:
        return self._count

    def mean(self) -> float:
        if self._count == 0:
            raise ValueError("the mean is undefined before the first value")
        return float(self._sum / self._count)

    def variance(self, ddof: int = 1) -> float:
        if self._count == 0:
            raise ValueError("the variance is undefined before the first value")
        if ddof not in (0, 1):
            raise TypeError("ddof must be 0 or 1")
        if ddof == 1 and self._count < 2:
            raise ValueError("the sample variance needs at least two values")
        mean = self._sum / self._count
        m2 = sum(((x - mean) ** 2 for x in self._xs), Fraction(0))
        return float(m2 / (self._count - ddof))


class RollingMinMax:
    def __init__(self, window: int) -> None:
        if window < 1:
            raise ValueError("the window must hold at least one value")
        if window != int(window):
            raise ValueError("the window must be a whole number of values")
        self._window = int(window)
        self._recent: list[float] = []

    def push(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be pushed")
        self._recent.append(float(x))
        if len(self._recent) > self._window:
            del self._recent[0]

    def minimum(self) -> float:
        if not self._recent:
            raise ValueError("no value has been pushed, so there is no minimum")
        return min(self._recent)

    def maximum(self) -> float:
        if not self._recent:
            raise ValueError("no value has been pushed, so there is no maximum")
        return max(self._recent)


class QuantileSketch:
    def __init__(self, epsilon: float) -> None:
        if not (0.0 < epsilon < 1.0):
            raise ValueError("epsilon must be a number strictly between 0 and 1")
        self._eps = Fraction(epsilon)
        self._sorted: list[float] = []

    def add(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be added")
        insort(self._sorted, float(x), key=None)

    def quantile(self, q: float) -> float:
        if not (0.0 <= q <= 1.0):
            raise ValueError("q must lie in the closed interval [0, 1]")
        n = len(self._sorted)
        if n == 0:
            raise ValueError("the sketch is empty, so it has no quantiles")
        target = max(1, math.ceil(Fraction(q) * n - self._eps * n))
        return self._sorted[min(target, n) - 1]
