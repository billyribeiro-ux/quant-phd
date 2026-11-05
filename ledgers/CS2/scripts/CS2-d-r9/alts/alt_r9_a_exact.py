"""Alternative A (round 9): exact Fraction running sums; brute-force rolling window; exact sorted-list sketch."""

from __future__ import annotations

import bisect
import math
from fractions import Fraction


def _check_real(x: float) -> float:
    if isinstance(x, str) or x is None:
        raise TypeError("not a real number")
    if math.isnan(x):
        raise ValueError("NaN")
    return x


class WelfordAccumulator:
    def __init__(self) -> None:
        self._n = 0
        self._s = Fraction(0)
        self._q = Fraction(0)

    def update(self, x: float) -> None:
        if isinstance(x, float) and math.isnan(x):
            raise ValueError("NaN")
        f = Fraction(x)  # raises OverflowError/ValueError on inf; a raise is allowed for an infinite value
        self._n += 1
        self._s += f
        self._q += f * f

    @property
    def count(self) -> int:
        return self._n

    def mean(self) -> float:
        if self._n == 0:
            raise ValueError("no values")
        return float(self._s / self._n)

    def variance(self, ddof: int = 1) -> float:
        if self._n == 0:
            raise ValueError("no values")
        if ddof not in (0, 1):
            raise TypeError("ddof must be 0 or 1")
        if ddof == 1 and self._n < 2:
            raise ValueError("needs two values")
        m2 = self._q - self._s * self._s / self._n
        return float(m2 / (self._n - ddof))


class RollingMinMax:
    def __init__(self, window: int) -> None:
        if window is None or isinstance(window, str):
            raise TypeError("window must be a number")
        if window < 1:
            raise ValueError("window below one")
        if window != int(window):
            raise ValueError("window must be whole")
        self._w = int(window)
        self._vals: list[float] = []

    def push(self, x: float) -> None:
        if x is None or isinstance(x, str):
            raise TypeError("not a number")
        if math.isnan(x):
            raise ValueError("NaN")
        self._vals.append(float(x))

    def minimum(self) -> float:
        if not self._vals:
            raise ValueError("nothing pushed")
        return min(self._vals[-self._w :])

    def maximum(self) -> float:
        if not self._vals:
            raise ValueError("nothing pushed")
        return max(self._vals[-self._w :])


class QuantileSketch:
    def __init__(self, epsilon: float) -> None:
        if isinstance(epsilon, str) or epsilon is None or math.isnan(epsilon):
            raise ValueError("epsilon")
        if not (0 < epsilon < 1):
            raise ValueError("epsilon must lie strictly in (0, 1)")
        self._eps = Fraction(epsilon)
        self._sorted: list[float] = []

    def add(self, x: float) -> None:
        if x is None or isinstance(x, str):
            raise TypeError("not a number")
        if math.isnan(x):
            raise ValueError("NaN")
        bisect.insort(self._sorted, float(x))

    def quantile(self, q: float) -> float:
        if not self._sorted:
            raise ValueError("empty sketch")
        if not (0 <= q <= 1):
            raise ValueError("q outside [0, 1]")
        n = len(self._sorted)
        target = max(1, math.ceil(Fraction(q) * n - self._eps * n))
        return self._sorted[target - 1]
