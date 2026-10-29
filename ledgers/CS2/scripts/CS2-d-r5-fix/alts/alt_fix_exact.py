"""Alternative correct implementation: exact storage with Fraction arithmetic (no Welford, no deque, no sketch)."""

from __future__ import annotations

import math
from bisect import insort
from fractions import Fraction


class WelfordAccumulator:
    def __init__(self) -> None:
        self._values: list[Fraction] = []

    def update(self, x: float) -> None:
        value = Fraction(x)  # bool, padded string and str denote numbers; None raises TypeError
        if math.isnan(float(x)):
            raise ValueError("a NaN value is not a number and cannot be added")
        self._values.append(value)

    @property
    def count(self) -> int:
        return len(self._values)

    def mean(self) -> float:
        if not self._values:
            raise ValueError("the mean is undefined before the first value")
        return float(sum(self._values, Fraction(0)) / len(self._values))

    def variance(self, ddof: int = 1) -> float:
        if not self._values:
            raise ValueError("the variance is undefined before the first value")
        d = Fraction(ddof)  # None raises TypeError; "1" and 1.0 denote 1; "2" denotes 2
        if d not in (0, 1):
            raise TypeError("ddof must denote 0 or 1")
        if d == 1 and len(self._values) < 2:
            raise ValueError("the sample variance needs at least two values")
        n = len(self._values)
        mean = sum(self._values, Fraction(0)) / n
        m2 = sum(((v - mean) ** 2 for v in self._values), Fraction(0))
        return float(m2 / (n - 1 if d == 1 else n))


class RollingMinMax:
    def __init__(self, window: int) -> None:
        w = Fraction(window)  # None raises TypeError; False denotes 0
        if w < 1:
            raise ValueError("the window must hold at least one value")
        if w.denominator != 1:
            raise ValueError("the window must be a whole number of values")
        self._window = int(w)
        self._values: list[float] = []

    def push(self, x: float) -> None:
        v = float(x)  # None raises TypeError; padded and plain strings denote numbers
        if math.isnan(v):
            raise ValueError("a NaN value is not a number and cannot be pushed")
        self._values.append(v)

    def minimum(self) -> float:
        if not self._values:
            raise ValueError("no value has been pushed, so there is no minimum")
        return min(self._values[-self._window :])

    def maximum(self) -> float:
        if not self._values:
            raise ValueError("no value has been pushed, so there is no maximum")
        return max(self._values[-self._window :])


class QuantileSketch:
    def __init__(self, epsilon: float) -> None:
        if isinstance(epsilon, bool) or not (0.0 < epsilon < 1.0):
            raise ValueError("epsilon must be a number strictly between 0 and 1")
        self._eps = Fraction(epsilon)
        self._values: list[float] = []

    def add(self, x: float) -> None:
        v = float(x)
        if math.isnan(v):
            raise ValueError("a NaN value is not a number and cannot be added")
        insort(self._values, v)

    def quantile(self, q: float) -> float:
        if not (0.0 <= q <= 1.0):
            raise ValueError("q must lie in the closed interval [0, 1]")
        n = len(self._values)
        if n == 0:
            raise ValueError("the sketch is empty, so it has no quantiles")
        k = max(1, math.ceil(Fraction(q) * n - self._eps * n))
        return self._values[k - 1]
