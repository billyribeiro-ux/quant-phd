"""Alternative correct implementation: store everything, exact rank target, brute-force rolling."""
from __future__ import annotations
import math
from fractions import Fraction


class WelfordAccumulator:
    def __init__(self) -> None:
        self._xs: list[float] = []

    def update(self, x: float) -> None:
        if isinstance(x, float) and math.isnan(x):
            raise ValueError("NaN")
        self._xs.append(float(x) if not isinstance(x, bool) else float(x))

    @property
    def count(self) -> int:
        return len(self._xs)

    def mean(self) -> float:
        if not self._xs:
            raise ValueError("no values")
        return float(sum(Fraction(x) for x in self._xs) / len(self._xs))

    def variance(self, ddof: int = 1) -> float:
        if not self._xs:
            raise ValueError("no values")
        if ddof not in (0, 1):
            raise TypeError("ddof")
        n = len(self._xs)
        if ddof == 1 and n < 2:
            raise ValueError("need two")
        m = sum(Fraction(x) for x in self._xs) / n
        ss = sum((Fraction(x) - m) ** 2 for x in self._xs)
        return float(ss / (n if ddof == 0 else n - 1))


class RollingMinMax:
    def __init__(self, window: int) -> None:
        if window < 1:
            raise ValueError("window")
        if window != int(window):
            raise ValueError("window")
        self._w = int(window)
        self._xs: list[float] = []

    def push(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("nan")
        self._xs.append(float(x))

    def minimum(self) -> float:
        if not self._xs:
            raise ValueError("empty")
        return min(self._xs[-self._w:])

    def maximum(self) -> float:
        if not self._xs:
            raise ValueError("empty")
        return max(self._xs[-self._w:])


class QuantileSketch:
    def __init__(self, epsilon: float) -> None:
        if not (0.0 < epsilon < 1.0):
            raise ValueError("epsilon")
        self._eps = Fraction(epsilon)
        self._xs: list[float] = []

    def add(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("nan")
        self._xs.append(float(x))

    def quantile(self, q: float) -> float:
        if not (0.0 <= q <= 1.0):
            raise ValueError("q")
        if not self._xs:
            raise ValueError("empty")
        n = len(self._xs)
        target = max(1, math.ceil(Fraction(q) * n - self._eps * n))
        return sorted(self._xs)[target - 1]
