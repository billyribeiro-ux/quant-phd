"""Alternative: stores the values and computes the mean and the sum of squared deviations with math.fsum."""
from __future__ import annotations

import math


class WelfordAccumulator:
    def __init__(self) -> None:
        self._values: list[float] = []

    def update(self, x: float) -> None:
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
        if ddof == 0:
            denom = len(self._values)
        elif ddof == 1:
            if len(self._values) < 2:
                raise ValueError("the sample variance needs at least two values")
            denom = len(self._values) - 1
        else:
            raise TypeError("ddof must be 0 or 1")
        m = self.mean()
        return math.fsum((v - m) ** 2 for v in self._values) / denom


class RollingMinMax:
    def __init__(self, window: int) -> None:
        if window < 1:
            raise ValueError("the window must hold at least one value")
        if window != int(window):
            raise ValueError("the window must be a whole number of values")
        self._window = int(window)
        self._vals: list[float] = []

    def push(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be pushed")
        self._vals.append(float(x))

    def minimum(self) -> float:
        if not self._vals:
            raise ValueError("no value has been pushed, so there is no minimum")
        return min(self._vals[-self._window:])

    def maximum(self) -> float:
        if not self._vals:
            raise ValueError("no value has been pushed, so there is no maximum")
        return max(self._vals[-self._window:])


class QuantileSketch:
    def __init__(self, epsilon: float) -> None:
        if not (0.0 < epsilon < 1.0):
            raise ValueError("epsilon must be a number strictly between 0 and 1")
        from fractions import Fraction
        self._eps = Fraction(epsilon)
        self._values: list[float] = []

    def add(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be added")
        import bisect
        bisect.insort(self._values, float(x))

    def quantile(self, q: float) -> float:
        from fractions import Fraction
        if not (0.0 <= q <= 1.0):
            raise ValueError("q must lie in the closed interval [0, 1]")
        n = len(self._values)
        if n == 0:
            raise ValueError("the sketch is empty, so it has no quantiles")
        k = max(1, math.ceil(Fraction(q) * n - self._eps * n))
        return self._values[k - 1]
