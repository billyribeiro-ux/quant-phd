"""Alternative A (correct): Welford class replaced by storing every value and a two-pass mean and sum of squares."""

from __future__ import annotations

import math
from bisect import bisect_right, insort
from collections import deque
from fractions import Fraction


class WelfordAccumulator:
    def __init__(self) -> None:
        self._values: list[float] = []

    def update(self, x: float) -> None:
        if isinstance(x, bool) or not isinstance(x, (int, float)):
            raise TypeError("value must be a real number")
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be added")
        self._values.append(float(x))

    @property
    def count(self) -> int:
        return len(self._values)

    def mean(self) -> float:
        if not self._values:
            raise ValueError("the mean is undefined before the first value")
        return math.fsum(self._values) / len(self._values)

    def variance(self, ddof: int = 1) -> float:
        if not self._values:
            raise ValueError("the variance is undefined before the first value")
        if ddof not in (0, 1) or isinstance(ddof, bool):
            raise TypeError("ddof must be 0 or 1")
        if ddof == 1 and len(self._values) < 2:
            raise ValueError("the sample variance needs at least two values")
        m = self.mean()
        ss = math.fsum((x - m) ** 2 for x in self._values)
        return ss / (len(self._values) - ddof)


class RollingMinMax:
    def __init__(self, window: int) -> None:
        if isinstance(window, bool) and window is False:
            raise ValueError("the window must hold at least one value")
        if not isinstance(window, (int, float)) or window < 1 or window != int(window):
            raise ValueError("the window must be a whole number of values, at least 1")
        self._w = int(window)
        self._buf: deque[float] = deque(maxlen=self._w)
        self._seen = 0

    def push(self, x: float) -> None:
        if isinstance(x, str) or x is None:
            raise TypeError("value must be a number")
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be pushed")
        self._buf.append(float(x))
        self._seen += 1

    def minimum(self) -> float:
        if not self._buf:
            raise ValueError("no value has been pushed, so there is no minimum")
        return min(self._buf)

    def maximum(self) -> float:
        if not self._buf:
            raise ValueError("no value has been pushed, so there is no maximum")
        return max(self._buf)


class QuantileSketch:
    """Alternative E style: keeps every value sorted and answers from the exact sorted list."""

    def __init__(self, epsilon: float) -> None:
        if isinstance(epsilon, bool) or not (0.0 < epsilon < 1.0):
            raise ValueError("epsilon must be strictly between 0 and 1")
        self._eps = Fraction(epsilon)
        self._sorted: list[float] = []

    def add(self, x: float) -> None:
        if isinstance(x, str) or x is None:
            raise TypeError("value must be a number")
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be added")
        insort(self._sorted, float(x))

    def quantile(self, q: float) -> float:
        if not (0.0 <= q <= 1.0):
            raise ValueError("q must lie in the closed interval [0, 1]")
        n = len(self._sorted)
        if n == 0:
            raise ValueError("the sketch is empty")
        k = max(1, math.ceil(Fraction(q) * n - self._eps * n))
        return self._sorted[min(k, n) - 1]
