"""Alternative: Welford update with the identity M2 += delta * delta * (n - 1) / n, which equals the usual increment."""
from __future__ import annotations

import math


class WelfordAccumulator:
    def __init__(self) -> None:
        self._n = 0
        self._mean = 0.0
        self._m2 = 0.0

    def update(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be added")
        self._n += 1
        d = x - self._mean
        self._m2 += d * d * (self._n - 1) / self._n
        self._mean += d / self._n

    @property
    def count(self) -> int:
        return self._n

    def mean(self) -> float:
        if self._n == 0:
            raise ValueError("the mean is undefined before the first value")
        return self._mean

    def variance(self, ddof: int = 1) -> float:
        if self._n == 0:
            raise ValueError("the variance is undefined before the first value")
        if ddof == 0:
            return self._m2 / self._n
        if ddof == 1:
            if self._n < 2:
                raise ValueError("the sample variance needs at least two values")
            return self._m2 / (self._n - 1)
        raise TypeError("ddof must be 0 or 1")
