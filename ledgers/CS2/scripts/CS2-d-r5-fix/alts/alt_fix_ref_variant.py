"""Alternative correct implementation: the reference structure with a different update order and string handling."""

from __future__ import annotations

import math
from bisect import bisect_right
from collections import deque
from fractions import Fraction


class WelfordAccumulator:
    def __init__(self) -> None:
        self._n = 0
        self._mean = 0.0
        self._m2 = 0.0

    def update(self, x: float) -> None:
        x = float(x)
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be added")
        self._n += 1
        new_mean = self._mean + (x - self._mean) / self._n
        self._m2 += (x - self._mean) * (x - new_mean)
        self._mean = new_mean

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
        d = Fraction(ddof)
        if d == 0:
            return self._m2 / self._n
        if d == 1:
            if self._n < 2:
                raise ValueError("the sample variance needs at least two values")
            return self._m2 / (self._n - 1)
        raise TypeError("ddof must denote 0 or 1")


class RollingMinMax:
    def __init__(self, window: int) -> None:
        w = Fraction(window)
        if w < 1:
            raise ValueError("the window must hold at least one value")
        if w.denominator != 1:
            raise ValueError("the window must be a whole number of values")
        self._w = int(w)
        self._i = -1
        self._mins: deque[tuple[int, float]] = deque()
        self._maxs: deque[tuple[int, float]] = deque()

    def push(self, x: float) -> None:
        x = float(x)
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be pushed")
        self._i += 1
        while self._mins and self._mins[-1][1] > x:
            self._mins.pop()
        self._mins.append((self._i, x))
        while self._maxs and self._maxs[-1][1] < x:
            self._maxs.pop()
        self._maxs.append((self._i, x))
        while self._mins[0][0] <= self._i - self._w:
            self._mins.popleft()
        while self._maxs[0][0] <= self._i - self._w:
            self._maxs.popleft()

    def minimum(self) -> float:
        if self._i < 0:
            raise ValueError("no value has been pushed, so there is no minimum")
        return self._mins[0][1]

    def maximum(self) -> float:
        if self._i < 0:
            raise ValueError("no value has been pushed, so there is no maximum")
        return self._maxs[0][1]


class QuantileSketch:
    def __init__(self, epsilon: float) -> None:
        if isinstance(epsilon, bool) or not (0.0 < epsilon < 1.0):
            raise ValueError("epsilon must be a number strictly between 0 and 1")
        self._eps = Fraction(epsilon)
        self._xs: list[float] = []

    def add(self, x: float) -> None:
        x = float(x)
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be added")
        self._xs.insert(bisect_right(self._xs, x), x)

    def quantile(self, q: float) -> float:
        if not (0.0 <= q <= 1.0):
            raise ValueError("q must lie in the closed interval [0, 1]")
        if not self._xs:
            raise ValueError("the sketch is empty, so it has no quantiles")
        n = len(self._xs)
        k = max(1, math.ceil(Fraction(q) * n - self._eps * n))
        return self._xs[k - 1]
