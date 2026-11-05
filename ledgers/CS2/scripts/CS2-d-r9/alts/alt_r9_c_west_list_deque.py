"""Alternative C (round 9): Welford in the (n-1)/n delta-squared form; monotonic deque in a list with a head pointer; sketch answers by binary search on exact counts."""

from __future__ import annotations

import bisect
import math
from fractions import Fraction


class WelfordAccumulator:
    def __init__(self) -> None:
        self._n = 0
        self._mean = 0.0
        self._m2 = 0.0

    def update(self, x: float) -> None:
        if isinstance(x, float) and math.isnan(x):
            raise ValueError("NaN")
        x = float(x)
        self._n += 1
        delta = x - self._mean
        self._m2 += (self._n - 1) / self._n * delta * delta
        self._mean += delta / self._n

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
        if ddof == 1 and self._n < 2:
            raise ValueError("needs two values")
        if ddof == 0:
            return self._m2 / self._n
        if ddof == 1:
            return self._m2 / (self._n - 1)
        raise TypeError("ddof")


class RollingMinMax:
    def __init__(self, window: int) -> None:
        if isinstance(window, str) or window is None or window < 1 or window != int(window):
            raise ValueError("window")
        self._w = int(window)
        self._i = -1
        self._mins: list[tuple[int, float]] = []
        self._hm = 0
        self._maxs: list[tuple[int, float]] = []
        self._hx = 0

    def push(self, x: float) -> None:
        if isinstance(x, str) or x is None or math.isnan(x):
            raise ValueError("bad value")
        x = float(x)
        self._i += 1
        while len(self._mins) > self._hm and self._mins[-1][1] >= x:
            self._mins.pop()
        self._mins.append((self._i, x))
        while len(self._maxs) > self._hx and self._maxs[-1][1] <= x:
            self._maxs.pop()
        self._maxs.append((self._i, x))
        while self._mins[self._hm][0] <= self._i - self._w:
            self._hm += 1
        while self._maxs[self._hx][0] <= self._i - self._w:
            self._hx += 1

    def minimum(self) -> float:
        if self._i < 0:
            raise ValueError("nothing pushed")
        return self._mins[self._hm][1]

    def maximum(self) -> float:
        if self._i < 0:
            raise ValueError("nothing pushed")
        return self._maxs[self._hx][1]


class QuantileSketch:
    def __init__(self, epsilon: float) -> None:
        if isinstance(epsilon, str) or epsilon is None or not (0 < epsilon < 1):
            raise ValueError("epsilon")
        self._eps = Fraction(epsilon)
        self._vals: list[float] = []

    def add(self, x: float) -> None:
        if isinstance(x, str) or x is None or math.isnan(x):
            raise ValueError("bad value")
        bisect.insort(self._vals, float(x))

    def quantile(self, q: float) -> float:
        if not self._vals:
            raise ValueError("empty")
        if not (0 <= q <= 1):
            raise ValueError("q")
        n = len(self._vals)
        target = max(1, math.ceil(Fraction(q) * n - self._eps * n))
        lo, hi = 0, n - 1
        while lo < hi:  # smallest index whose value has at least `target` values at or below it
            mid = (lo + hi) // 2
            if bisect.bisect_right(self._vals, self._vals[mid]) >= target:
                hi = mid
            else:
                lo = mid + 1
        return self._vals[lo]
