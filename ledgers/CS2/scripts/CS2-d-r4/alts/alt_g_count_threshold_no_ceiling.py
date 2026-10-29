"""Alternative G (verifier CS2-d round 4): exact sorted list; the answer is the smallest stored value whose exact count of values at or below it reaches qn - eps n. No ceiling is computed."""

from __future__ import annotations

import math
from bisect import bisect_left, bisect_right, insort
from fractions import Fraction


class WelfordAccumulator:
    def __init__(self) -> None:
        self._count = 0
        self._mean = 0.0
        self._m2 = 0.0

    def update(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be added")
        self._count += 1
        delta = x - self._mean
        self._mean += delta / self._count
        self._m2 += delta * (x - self._mean)

    @property
    def count(self) -> int:
        return self._count

    def mean(self) -> float:
        if self._count == 0:
            raise ValueError("the mean is undefined before the first value")
        return self._mean

    def variance(self, ddof: int = 1) -> float:
        if self._count == 0:
            raise ValueError("the variance is undefined before the first value")
        if ddof == 0:
            return self._m2 / self._count
        if ddof == 1:
            if self._count < 2:
                raise ValueError("the sample variance needs at least two values")
            return self._m2 / (self._count - 1)
        raise TypeError("ddof must be 0 or 1")


class RollingMinMax:
    def __init__(self, window: int) -> None:
        if window < 1:
            raise ValueError("the window must hold at least one value")
        self._window = window
        self._values: list[float] = []

    def push(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be pushed")
        self._values.append(float(x))

    def _window_values(self) -> list[float]:
        if not self._values:
            raise ValueError("no value has been pushed")
        return self._values[-self._window :]

    def minimum(self) -> float:
        return min(self._window_values())

    def maximum(self) -> float:
        return max(self._window_values())


class QuantileSketch:
    def __init__(self, epsilon: float) -> None:
        if not (0.0 < epsilon < 1.0):
            raise ValueError("epsilon must be strictly between 0 and 1")
        self._eps = Fraction(epsilon)
        self._sorted: list[float] = []

    def add(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be added")
        insort(self._sorted, float(x))

    def quantile(self, q: float) -> float:
        if not (0.0 <= q <= 1.0):
            raise ValueError("q must lie in the closed interval [0, 1]")
        n = len(self._sorted)
        if n == 0:
            raise ValueError("the sketch is empty")
        lower_bound = Fraction(q) * n - self._eps * n  # no ceiling: compare counts with this exact bound
        for v in self._sorted:
            at_or_below = bisect_right(self._sorted, v)
            if at_or_below >= lower_bound:
                return v
        return self._sorted[-1]
