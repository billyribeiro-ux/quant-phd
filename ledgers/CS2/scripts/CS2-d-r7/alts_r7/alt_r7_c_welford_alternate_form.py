"""Correct alternative C: Welford with the mean as a convex combination and the M2 increment written as (n-1)/n times delta squared."""
from __future__ import annotations

import math
from collections import deque


class WelfordAccumulator:
    def __init__(self) -> None:
        self._n = 0
        self._mean = 0.0
        self._m2 = 0.0

    def update(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number")
        self._n += 1
        if self._n == 1:
            self._mean = float(x)
            return
        delta = float(x) - self._mean
        new_mean = self._mean + delta / self._n
        self._m2 += (self._n - 1) * delta * delta / self._n
        self._mean = new_mean

    @property
    def count(self) -> int:
        return self._n

    def mean(self) -> float:
        if self._n == 0:
            raise ValueError("no value")
        return self._mean

    def variance(self, ddof: int = 1) -> float:
        if self._n == 0:
            raise ValueError("no value")
        if ddof == 0:
            return self._m2 / self._n
        if ddof == 1:
            if self._n < 2:
                raise ValueError("two values")
            return self._m2 / (self._n - 1)
        raise TypeError("ddof")


class RollingMinMax:
    def __init__(self, window: int) -> None:
        if window < 1:
            raise ValueError("window")
        if window != int(window):
            raise ValueError("whole")
        self._w = int(window)
        self._buf: deque[float] = deque(maxlen=self._w)
        self._seen = 0

    def push(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("nan")
        self._buf.append(float(x))
        self._seen += 1

    def minimum(self) -> float:
        if self._seen == 0:
            raise ValueError("empty")
        return min(self._buf)

    def maximum(self) -> float:
        if self._seen == 0:
            raise ValueError("empty")
        return max(self._buf)


class QuantileSketch:
    """Fixed-width summary: values sorted, rank target by Fraction, answer by exact rank over the full sorted list."""

    def __init__(self, epsilon: float) -> None:
        if not (0.0 < epsilon < 1.0):
            raise ValueError("epsilon")
        self._eps = epsilon
        self._vals: list[float] = []

    def add(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("nan")
        self._vals.append(float(x))

    def quantile(self, q: float) -> float:
        if not (0.0 <= q <= 1.0):
            raise ValueError("q")
        if not self._vals:
            raise ValueError("empty")
        from decimal import Decimal

        n = len(self._vals)
        target = max(1, math.ceil(Decimal(q) * n - Decimal(self._eps) * n))
        return sorted(self._vals)[target - 1]
