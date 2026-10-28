"""Alternative C: shifted-sum variance (sums of x minus the first value), sorted-window rolling min and max, exact sketch with target ceil(qn) clamped to n."""

from __future__ import annotations

import math
from bisect import insort
from collections import deque
from fractions import Fraction


class WelfordAccumulator:
    def __init__(self) -> None:
        self._n = 0
        self._shift = 0.0
        self._s1 = 0.0
        self._s2 = 0.0

    def update(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("nan")
        x = float(x)
        if self._n == 0:
            self._shift = x
        self._n += 1
        d = x - self._shift
        self._s1 += d
        self._s2 += d * d

    @property
    def count(self) -> int:
        return self._n

    def mean(self) -> float:
        if self._n == 0:
            raise ValueError("no values")
        return self._shift + self._s1 / self._n

    def variance(self, ddof: int = 1) -> float:
        if self._n == 0:
            raise ValueError("no values")
        if ddof not in (0, 1):
            raise ValueError("ddof")
        if ddof == 1 and self._n < 2:
            raise ValueError("need two values")
        ss = max(0.0, self._s2 - self._s1 * self._s1 / self._n)
        return ss / (self._n - ddof)


class RollingMinMax:
    def __init__(self, window: int) -> None:
        if window < 1:
            raise ValueError("window")
        self._w = window
        self._fifo: deque[float] = deque()
        self._sorted: list[float] = []

    def push(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("nan")
        x = float(x)
        self._fifo.append(x)
        insort(self._sorted, x)
        if len(self._fifo) > self._w:
            old = self._fifo.popleft()
            del self._sorted[self._sorted.index(old)]

    def minimum(self) -> float:
        if not self._fifo:
            raise ValueError("empty")
        return self._sorted[0]

    def maximum(self) -> float:
        if not self._fifo:
            raise ValueError("empty")
        return self._sorted[-1]


class QuantileSketch:
    def __init__(self, epsilon: float) -> None:
        if not (0.0 < epsilon < 1.0):
            raise ValueError("epsilon")
        self._eps = Fraction(epsilon)
        self._xs: list[float] = []

    def add(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("nan")
        insort(self._xs, float(x))

    def quantile(self, q: float) -> float:
        if not (0.0 <= q <= 1.0):
            raise ValueError("q")
        n = len(self._xs)
        if n == 0:
            raise ValueError("empty")
        k = min(n, max(1, math.ceil(Fraction(q) * n)))
        return self._xs[k - 1]
