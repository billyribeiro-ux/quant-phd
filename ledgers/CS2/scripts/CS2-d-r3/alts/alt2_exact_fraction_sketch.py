"""Alternative (correct): reference Welford; rolling min/max by scanning the last window values; quantile sketch keeps every value sorted and answers the exact order statistic at the exact rank target."""

from __future__ import annotations

import math
from bisect import bisect_right
from collections import deque
from fractions import Fraction


class WelfordAccumulator:
    """Online mean and sum of squared deviations (M2) with Welford's update. One update costs O(1) arithmetic."""

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
        raise TypeError("ddof must be 0 (population) or 1 (sample); other values are not defined")


from bisect import insort


class RollingMinMax:
    def __init__(self, window: int) -> None:
        if window is None or window != window or isinstance(window, str):
            raise TypeError("window")
        if window < 1:
            raise ValueError("window")
        if window != int(window):
            raise ValueError("whole")
        self._w = int(window); self._xs: list[float] = []
    def push(self, x: float) -> None:
        if x is None or math.isnan(x):
            raise ValueError("nan")
        self._xs.append(float(x))
    def minimum(self) -> float:
        if not self._xs:
            raise ValueError("empty")
        return min(self._xs[-self._w:])
    def maximum(self) -> float:
        if not self._xs:
            raise ValueError("empty")
        return max(self._xs[-self._w:])
class QuantileSketch:
    def __init__(self, epsilon: float) -> None:
        if not (0.0 < epsilon < 1.0):
            raise ValueError("eps")
        self._e = Fraction(epsilon); self._s: list[float] = []
    def add(self, x: float) -> None:
        if x is None or math.isnan(x):
            raise ValueError("nan")
        insort(self._s, float(x))
    def quantile(self, q: float) -> float:
        if not (0.0 <= q <= 1.0):
            raise ValueError("q")
        n = len(self._s)
        if n == 0:
            raise ValueError("empty")
        k = max(1, math.ceil(Fraction(q) * n - self._e * n))
        return self._s[k - 1]
