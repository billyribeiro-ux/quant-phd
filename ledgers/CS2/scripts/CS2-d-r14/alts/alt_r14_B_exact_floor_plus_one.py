"""Alternative B (correct): exact sorted list with rank target floor(qn - eps n) + 1, fsum two-pass Welford."""

from __future__ import annotations

import math
from bisect import insort
from fractions import Fraction


class WelfordAccumulator:
    def __init__(self) -> None:
        self._xs: list[float] = []

    def update(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be added")
        self._xs.append(float(x))

    @property
    def count(self) -> int:
        return len(self._xs)

    def mean(self) -> float:
        if not self._xs:
            raise ValueError("the mean is undefined before the first value")
        return math.fsum(self._xs) / len(self._xs)

    def variance(self, ddof: int = 1) -> float:
        if not self._xs:
            raise ValueError("the variance is undefined before the first value")
        if ddof == 0:
            denom = len(self._xs)
        elif ddof == 1:
            if len(self._xs) < 2:
                raise ValueError("the sample variance needs at least two values")
            denom = len(self._xs) - 1
        else:
            raise TypeError("ddof must be 0 or 1")
        m = self.mean()
        return math.fsum((x - m) ** 2 for x in self._xs) / denom


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
        self._recent = self._recent[-self._window :]

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
        insort(self._sorted, float(x))

    def quantile(self, q: float) -> float:
        if not (0.0 <= q <= 1.0):
            raise ValueError("q must lie in the closed interval [0, 1]")
        n = len(self._sorted)
        if n == 0:
            raise ValueError("the sketch is empty, so it has no quantiles")
        slack = Fraction(q) * n - self._eps * n
        target = max(1, math.floor(slack) + 1)
        return self._sorted[min(target, n) - 1]
