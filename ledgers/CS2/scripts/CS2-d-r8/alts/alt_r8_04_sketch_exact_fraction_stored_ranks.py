"""Alternative: a sketch that keeps every value with its rank and answers with the smallest stored value meeting both inequalities."""
from __future__ import annotations

import bisect
import math
from fractions import Fraction


class QuantileSketch:
    def __init__(self, epsilon: float) -> None:
        if not (0.0 < epsilon < 1.0):
            raise ValueError("epsilon must be a number strictly between 0 and 1")
        self._eps = Fraction(epsilon)
        self._vals: list[float] = []

    def add(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be added")
        bisect.insort(self._vals, float(x))

    def quantile(self, q: float) -> float:
        if not (0.0 <= q <= 1.0):
            raise ValueError("q must lie in the closed interval [0, 1]")
        n = len(self._vals)
        if n == 0:
            raise ValueError("the sketch is empty, so it has no quantiles")
        qf = Fraction(q)
        lo, hi = qf * n - self._eps * n, qf * n + self._eps * n
        for v in sorted(set(self._vals)):
            below = bisect.bisect_left(self._vals, v)
            at_or_below = bisect.bisect_right(self._vals, v)
            if below <= hi and at_or_below >= lo:
                return v
        return self._vals[-1]
