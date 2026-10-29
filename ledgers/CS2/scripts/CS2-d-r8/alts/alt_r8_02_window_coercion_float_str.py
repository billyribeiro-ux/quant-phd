"""Alternative: coerces the window through float, refuses non-whole and None windows, and uses the reference deques."""
from __future__ import annotations

import math
from collections import deque


class WelfordAccumulator:
    def __init__(self) -> None:
        self._n = 0
        self._mean = 0.0
        self._m2 = 0.0

    def update(self, x: float) -> None:
        x = float(x)
        if math.isnan(x):
            raise ValueError("NaN")
        self._n += 1
        d = x - self._mean
        self._mean += d / self._n
        self._m2 += d * (x - self._mean)

    @property
    def count(self) -> int:
        return self._n

    def mean(self) -> float:
        if self._n == 0:
            raise ValueError("no values")
        return self._mean

    def variance(self, ddof: int = 1) -> float:
        if self._n == 0:
            raise ValueError("no values")
        d = float(ddof)
        if d == 0.0:
            return self._m2 / self._n
        if d == 1.0:
            if self._n < 2:
                raise ValueError("needs two values")
            return self._m2 / (self._n - 1)
        raise ValueError("ddof")


class RollingMinMax:
    def __init__(self, window) -> None:
        w = float(window)
        if w < 1:
            raise ValueError("window below one")
        if w != math.floor(w):
            raise ValueError("window is not whole")
        self._w = int(w)
        self._i = -1
        self._mins: deque = deque()
        self._maxs: deque = deque()

    def push(self, x) -> None:
        x = float(x)
        if math.isnan(x):
            raise ValueError("NaN")
        self._i += 1
        while self._mins and self._mins[-1][1] >= x:
            self._mins.pop()
        self._mins.append((self._i, x))
        while self._maxs and self._maxs[-1][1] <= x:
            self._maxs.pop()
        self._maxs.append((self._i, x))
        lo = self._i - self._w + 1
        while self._mins[0][0] < lo:
            self._mins.popleft()
        while self._maxs[0][0] < lo:
            self._maxs.popleft()

    def minimum(self) -> float:
        if self._i < 0:
            raise ValueError("no value")
        return self._mins[0][1]

    def maximum(self) -> float:
        if self._i < 0:
            raise ValueError("no value")
        return self._maxs[0][1]


class QuantileSketch:
    def __init__(self, epsilon: float) -> None:
        if isinstance(epsilon, bool) or not (0.0 < float(epsilon) < 1.0):
            raise ValueError("epsilon")
        self._exact = __import__("fractions").Fraction(float(epsilon))
        self._vals: list[float] = []

    def add(self, x) -> None:
        x = float(x)
        if math.isnan(x):
            raise ValueError("NaN")
        import bisect
        bisect.insort(self._vals, x)

    def quantile(self, q) -> float:
        from fractions import Fraction
        q = float(q)
        if not (0.0 <= q <= 1.0):
            raise ValueError("q")
        if not self._vals:
            raise ValueError("empty")
        n = len(self._vals)
        k = max(1, math.ceil(Fraction(q) * n - self._exact * n))
        return self._vals[k - 1]
