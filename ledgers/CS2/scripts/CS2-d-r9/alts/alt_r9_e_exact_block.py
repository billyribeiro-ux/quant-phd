"""Alternative E (round 9): Welford in exact integer-scaled Fractions per update; rolling by slicing the stored values; sketch as sorted blocks of at most 64 values."""

from __future__ import annotations

import bisect
import math
from fractions import Fraction


class WelfordAccumulator:
    def __init__(self) -> None:
        self._values: list[Fraction] = []

    def update(self, x: float) -> None:
        if isinstance(x, float) and math.isnan(x):
            raise ValueError("NaN")
        self._values.append(Fraction(float(x)))

    @property
    def count(self) -> int:
        return len(self._values)

    def mean(self) -> float:
        if not self._values:
            raise ValueError("no values")
        return float(sum(self._values, Fraction(0)) / len(self._values))

    def variance(self, ddof: int = 1) -> float:
        n = len(self._values)
        if n == 0:
            raise ValueError("no values")
        if ddof == 1 and n < 2:
            raise ValueError("needs two values")
        if ddof not in (0, 1):
            raise TypeError("ddof")
        mu = sum(self._values, Fraction(0)) / n
        return float(sum(((x - mu) ** 2 for x in self._values), Fraction(0)) / (n - ddof))


class RollingMinMax:
    def __init__(self, window: int) -> None:
        if isinstance(window, str) or window is None or window < 1 or window != int(window):
            raise ValueError("window")
        self._w = int(window)
        self._vals: list[float] = []

    def push(self, x: float) -> None:
        if isinstance(x, str) or x is None or math.isnan(x):
            raise ValueError("bad value")
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
    """Sorted blocks of at most 64 values; the rank target is computed exactly."""

    def __init__(self, epsilon: float) -> None:
        if isinstance(epsilon, str) or epsilon is None or not (0 < epsilon < 1):
            raise ValueError("epsilon")
        self._eps = Fraction(epsilon)
        self._blocks: list[list[float]] = []
        self._n = 0

    def add(self, x: float) -> None:
        if isinstance(x, str) or x is None or math.isnan(x):
            raise ValueError("bad value")
        v = float(x)
        self._n += 1
        if not self._blocks:
            self._blocks.append([v])
            return
        bi = 0
        while bi < len(self._blocks) - 1 and self._blocks[bi][-1] < v:
            bi += 1
        blk = self._blocks[bi]
        bisect.insort(blk, v)
        if len(blk) > 64:
            self._blocks[bi : bi + 1] = [blk[:32], blk[32:]]

    def quantile(self, q: float) -> float:
        if self._n == 0:
            raise ValueError("empty")
        if not (0 <= q <= 1):
            raise ValueError("q")
        target = max(1, math.ceil(Fraction(q) * self._n - self._eps * self._n))
        seen = 0
        for blk in self._blocks:
            if seen + len(blk) >= target:
                return blk[target - seen - 1]
            seen += len(blk)
        return self._blocks[-1][-1]
