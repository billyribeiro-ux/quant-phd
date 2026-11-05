"""Alternative D (round 9): Welford with the standard two-line update and a float-free exact rank target; rolling min/max by a sorted window list; sketch keeps a Greenwald-Khanna style list with a left-to-right compress."""

from __future__ import annotations

import bisect
import math
from fractions import Fraction


class WelfordAccumulator:
    def __init__(self) -> None:
        self.n = 0
        self.m = 0.0
        self.s = 0.0

    def update(self, x: float) -> None:
        if isinstance(x, float) and math.isnan(x):
            raise ValueError("NaN")
        x = float(x)
        self.n += 1
        old = self.m
        self.m = old + (x - old) / self.n
        self.s = self.s + (x - old) * (x - self.m)

    @property
    def count(self) -> int:
        return self.n

    def mean(self) -> float:
        if self.n == 0:
            raise ValueError("no values")
        return self.m

    def variance(self, ddof: int = 1) -> float:
        if self.n == 0:
            raise ValueError("no values")
        if ddof not in (0, 1):
            raise TypeError("ddof")
        if ddof == 1 and self.n < 2:
            raise ValueError("needs two values")
        return self.s / (self.n - ddof)


class RollingMinMax:
    def __init__(self, window: int) -> None:
        if isinstance(window, str) or window is None or window < 1 or window != int(window):
            raise ValueError("window")
        self._w = int(window)
        self._seq: list[float] = []
        self._win: list[float] = []

    def push(self, x: float) -> None:
        if isinstance(x, str) or x is None or math.isnan(x):
            raise ValueError("bad value")
        v = float(x)
        self._seq.append(v)
        bisect.insort(self._win, v)
        if len(self._seq) > self._w:
            gone = self._seq[-self._w - 1]
            del self._win[bisect.bisect_left(self._win, gone)]

    def minimum(self) -> float:
        if not self._seq:
            raise ValueError("nothing pushed")
        return self._win[0]

    def maximum(self) -> float:
        if not self._seq:
            raise ValueError("nothing pushed")
        return self._win[-1]


class QuantileSketch:
    """Keeps (value, g, delta) tuples; compresses left to right after each add."""

    def __init__(self, epsilon: float) -> None:
        if isinstance(epsilon, str) or epsilon is None or not (0 < epsilon < 1):
            raise ValueError("epsilon")
        self._e = Fraction(epsilon)
        self._n = 0
        self._t: list[list] = []  # [value, g, delta]

    def add(self, x: float) -> None:
        if isinstance(x, str) or x is None or math.isnan(x):
            raise ValueError("bad value")
        v = float(x)
        keys = [t[0] for t in self._t]
        p = bisect.bisect_right(keys, v)
        d = 0 if p == 0 or p == len(self._t) else self._t[p][1] + self._t[p][2] - 1
        self._t.insert(p, [v, 1, d])
        self._n += 1
        cap = math.floor(2 * self._e * self._n) + 1
        i = 0
        while i < len(self._t) - 2:
            if i >= 1 and self._t[i][1] + self._t[i + 1][1] + self._t[i + 1][2] <= cap:
                self._t[i + 1][1] += self._t[i][1]
                del self._t[i]
            else:
                i += 1

    def quantile(self, q: float) -> float:
        if self._n == 0:
            raise ValueError("empty")
        if not (0 <= q <= 1):
            raise ValueError("q")
        target = max(1, math.ceil(Fraction(q) * self._n - self._e * self._n))
        r = 0
        for v, g, _ in self._t:
            r += g
            if r >= target:
                return v
        return self._t[-1][0]
