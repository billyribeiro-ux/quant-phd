"""Alternative B (round 9): store-all two-pass variance with math.fsum; sorted-window rolling; lazy-sorted sketch."""

from __future__ import annotations

import bisect
import math
from fractions import Fraction


class WelfordAccumulator:
    def __init__(self) -> None:
        self._xs: list[float] = []

    def update(self, x: float) -> None:
        if isinstance(x, float) and math.isnan(x):
            raise ValueError("NaN")
        if isinstance(x, float) and math.isinf(x):
            raise ValueError("infinite value")
        self._xs.append(float(x))

    @property
    def count(self) -> int:
        return len(self._xs)

    def mean(self) -> float:
        if not self._xs:
            raise ValueError("no values")
        return math.fsum(self._xs) / len(self._xs)

    def variance(self, ddof: int = 1) -> float:
        if not self._xs:
            raise ValueError("no values")
        if ddof == 1 and len(self._xs) < 2:
            raise ValueError("needs two values")
        if ddof not in (0, 1):
            raise TypeError("ddof must be 0 or 1")
        m = self.mean()
        return math.fsum((x - m) ** 2 for x in self._xs) / (len(self._xs) - ddof)


class RollingMinMax:
    def __init__(self, window: int) -> None:
        if isinstance(window, str) or window is None:
            raise TypeError("window")
        if window < 1:
            raise ValueError("window")
        if window != int(window):
            raise ValueError("window must be whole")
        self._w = int(window)
        self._order: list[float] = []
        self._sorted: list[float] = []

    def push(self, x: float) -> None:
        if isinstance(x, str) or x is None or math.isnan(x):
            raise ValueError("bad value")
        v = float(x)
        self._order.append(v)
        bisect.insort(self._sorted, v)
        if len(self._order) > self._w:
            old = self._order.pop(0)
            del self._sorted[bisect.bisect_left(self._sorted, old)]

    def minimum(self) -> float:
        if not self._order:
            raise ValueError("nothing pushed")
        return self._sorted[0]

    def maximum(self) -> float:
        if not self._order:
            raise ValueError("nothing pushed")
        return self._sorted[-1]


class QuantileSketch:
    def __init__(self, epsilon: float) -> None:
        if isinstance(epsilon, str) or epsilon is None or not (0 < epsilon < 1):
            raise ValueError("epsilon")
        self._eps = Fraction(epsilon)
        self._vals: list[float] = []
        self._dirty = False

    def add(self, x: float) -> None:
        if isinstance(x, str) or x is None or math.isnan(x):
            raise ValueError("bad value")
        self._vals.append(float(x))
        self._dirty = True

    def quantile(self, q: float) -> float:
        if not self._vals:
            raise ValueError("empty")
        if not (0 <= q <= 1):
            raise ValueError("q")
        if self._dirty:
            self._vals.sort()
            self._dirty = False
        n = len(self._vals)
        target = max(1, math.ceil(Fraction(q) * n - self._eps * n))
        for i, v in enumerate(self._vals):
            if i + 1 >= target:
                return v
        return self._vals[-1]
