"""Alternative: Welford in exact Fraction arithmetic returned as float; sketch identical to the reference but the cap is computed exactly with Fraction."""
from __future__ import annotations
import math
from bisect import bisect_right
from collections import deque
from fractions import Fraction
class WelfordAccumulator:
    def __init__(self) -> None:
        self._vals: list[Fraction] = []
    def update(self, x: float) -> None:
        if x is None or math.isnan(x):
            raise ValueError("nan")
        self._vals.append(Fraction(x))
    @property
    def count(self) -> int:
        return len(self._vals)
    def mean(self) -> float:
        if not self._vals:
            raise ValueError("empty")
        return float(sum(self._vals) / len(self._vals))
    def variance(self, ddof: int = 1) -> float:
        if not self._vals:
            raise ValueError("empty")
        n = len(self._vals)
        mu = sum(self._vals) / n
        m2 = sum((v - mu) ** 2 for v in self._vals)
        if ddof == 0:
            return float(m2 / n)
        if ddof == 1:
            if n < 2:
                raise ValueError("two")
            return float(m2 / (n - 1))
        raise TypeError("ddof")
class RollingMinMax:
    def __init__(self, window: int) -> None:
        if window < 1:
            raise ValueError("window")
        if window != int(window):
            raise ValueError("whole")
        self._w = window; self._i = -1
        self._mn: deque[tuple[int, float]] = deque(); self._mx: deque[tuple[int, float]] = deque()
    def push(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("nan")
        self._i += 1
        while self._mn and self._mn[-1][1] > x:
            self._mn.pop()
        self._mn.append((self._i, x))
        while self._mx and self._mx[-1][1] < x:
            self._mx.pop()
        self._mx.append((self._i, x))
        while self._mn[0][0] <= self._i - self._w:
            self._mn.popleft()
        while self._mx[0][0] <= self._i - self._w:
            self._mx.popleft()
    def minimum(self) -> float:
        if self._i < 0:
            raise ValueError("empty")
        return self._mn[0][1]
    def maximum(self) -> float:
        if self._i < 0:
            raise ValueError("empty")
        return self._mx[0][1]
class QuantileSketch:
    def __init__(self, epsilon: float) -> None:
        if not (0.0 < epsilon < 1.0):
            raise ValueError("eps")
        self._e = Fraction(epsilon); self._n = 0; self._v: list[float] = []; self._g: list[int] = []; self._d: list[int] = []
    def add(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("nan")
        p = bisect_right(self._v, x)
        d = 0 if p == 0 or p == len(self._v) else self._g[p] + self._d[p] - 1
        self._v.insert(p, float(x)); self._g.insert(p, 1); self._d.insert(p, d); self._n += 1
        cap = math.floor(2 * self._e * self._n) + 1
        for i in range(len(self._v) - 2, 0, -1):
            if self._g[i] + self._g[i + 1] + self._d[i + 1] <= cap:
                self._g[i + 1] += self._g[i]
                del self._v[i]; del self._g[i]; del self._d[i]
    def quantile(self, q: float) -> float:
        if not (0.0 <= q <= 1.0):
            raise ValueError("q")
        if self._n == 0:
            raise ValueError("empty")
        t = max(1, math.ceil(Fraction(q) * self._n - self._e * self._n))
        r = 0
        for v, g in zip(self._v, self._g):
            r += g
            if r >= t:
                return v
        return self._v[-1]
