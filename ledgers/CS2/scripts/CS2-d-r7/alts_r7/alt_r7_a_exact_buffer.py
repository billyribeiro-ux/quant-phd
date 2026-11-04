"""Correct alternative A: every value is stored; statistics are recomputed exactly with Fraction at each query."""
from __future__ import annotations

import math
from fractions import Fraction


class WelfordAccumulator:
    def __init__(self) -> None:
        self._values: list[float] = []

    def update(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value cannot be added")
        self._values.append(float(x))

    @property
    def count(self) -> int:
        return len(self._values)

    def mean(self) -> float:
        if not self._values:
            raise ValueError("no value")
        return float(sum((Fraction(v) for v in self._values), Fraction(0)) / len(self._values))

    def variance(self, ddof: int = 1) -> float:
        if not self._values:
            raise ValueError("no value")
        n = len(self._values)
        if ddof == 1 and n < 2:
            raise ValueError("needs two values")
        if ddof not in (0, 1):
            raise TypeError("ddof 0 or 1")
        fr = [Fraction(v) for v in self._values]
        m = sum(fr, Fraction(0)) / n
        ss = sum(((x - m) ** 2 for x in fr), Fraction(0))
        return float(ss / (n - ddof))


class RollingMinMax:
    def __init__(self, window: int) -> None:
        if window < 1:
            raise ValueError("window")
        if window != int(window):
            raise ValueError("whole window")
        self._window = window
        self._vals: list[float] = []

    def push(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("nan")
        self._vals.append(x)

    def minimum(self) -> float:
        if not self._vals:
            raise ValueError("empty")
        return min(self._vals[-self._window :])

    def maximum(self) -> float:
        if not self._vals:
            raise ValueError("empty")
        return max(self._vals[-self._window :])


class QuantileSketch:
    def __init__(self, epsilon: float) -> None:
        if not (0.0 < epsilon < 1.0):
            raise ValueError("epsilon")
        self._eps = Fraction(epsilon)
        self._sorted: list[float] = []

    def add(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("nan")
        import bisect

        bisect.insort(self._sorted, float(x))

    def quantile(self, q: float) -> float:
        if not (0.0 <= q <= 1.0):
            raise ValueError("q")
        if not self._sorted:
            raise ValueError("empty")
        n = len(self._sorted)
        target = max(1, math.ceil(Fraction(q) * n - self._eps * n))
        return self._sorted[target - 1]
