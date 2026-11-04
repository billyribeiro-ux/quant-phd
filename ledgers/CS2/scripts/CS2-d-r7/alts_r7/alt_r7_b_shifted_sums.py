"""Correct alternative B: Welford replaced by sums of deviations from the first value (shifted data)."""
from __future__ import annotations

import math
from bisect import bisect_right
from collections import deque


class WelfordAccumulator:
    def __init__(self) -> None:
        self._n = 0
        self._shift = 0.0
        self._s = 0.0
        self._ss = 0.0

    def update(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("nan")
        if self._n == 0:
            self._shift = float(x)
        self._n += 1
        d = float(x) - self._shift
        self._s += d
        self._ss += d * d

    @property
    def count(self) -> int:
        return self._n

    def mean(self) -> float:
        if self._n == 0:
            raise ValueError("no value")
        return self._shift + self._s / self._n

    def variance(self, ddof: int = 1) -> float:
        if self._n == 0:
            raise ValueError("no value")
        if ddof == 1 and self._n < 2:
            raise ValueError("two values")
        if ddof not in (0, 1):
            raise TypeError("ddof")
        return (self._ss - self._s * self._s / self._n) / (self._n - ddof)


class RollingMinMax:
    def __init__(self, window: int) -> None:
        if window < 1 or window != int(window):
            raise ValueError("window")
        self._w = int(window)
        self._i = -1
        self._dq_min: deque[tuple[int, float]] = deque()
        self._dq_max: deque[tuple[int, float]] = deque()

    def push(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("nan")
        self._i += 1
        i = self._i
        while self._dq_min and self._dq_min[-1][1] > x:
            self._dq_min.pop()
        self._dq_min.append((i, x))
        while self._dq_max and self._dq_max[-1][1] < x:
            self._dq_max.pop()
        self._dq_max.append((i, x))
        while self._dq_min[0][0] <= i - self._w:
            self._dq_min.popleft()
        while self._dq_max[0][0] <= i - self._w:
            self._dq_max.popleft()

    def minimum(self) -> float:
        if self._i < 0:
            raise ValueError("empty")
        return self._dq_min[0][1]

    def maximum(self) -> float:
        if self._i < 0:
            raise ValueError("empty")
        return self._dq_max[0][1]


class QuantileSketch:
    """Keeps every value in a sorted list with the rank of each stored value (no compression)."""

    def __init__(self, epsilon: float) -> None:
        if not (0.0 < epsilon < 1.0):
            raise ValueError("epsilon")
        self._eps = epsilon
        self._vals: list[float] = []

    def add(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("nan")
        self._vals.insert(bisect_right(self._vals, float(x)), float(x))

    def quantile(self, q: float) -> float:
        if not (0.0 <= q <= 1.0):
            raise ValueError("q")
        n = len(self._vals)
        if n == 0:
            raise ValueError("empty")
        from fractions import Fraction

        target = max(1, math.ceil(Fraction(q) * n - Fraction(self._eps) * n))
        return self._vals[target - 1]
