"""Reference solution for the CS2 streaming statistics library (streamstats.py).

Standard library only. Values are floats in the caller's unit; counts and window lengths are ints; the
quantile sketch's epsilon and q are floats in [0, 1] (epsilon strictly inside (0, 1)). Nothing here prints,
warns or reads files. The grader copies this file into the workspace as streamstats.py.
"""

from __future__ import annotations

import math
from bisect import bisect_right
from collections import deque
from fractions import Fraction


class WelfordAccumulator:
    def __init__(self) -> None:
        self._values: list[float] = []

    def update(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be added")
        self._values.append(x)

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
        n = len(self._values)
        if ddof not in (0, 1):
            raise TypeError("ddof must be 0 or 1")
        if ddof == 1 and n < 2:
            raise ValueError("the sample variance needs at least two values")
        m = self.mean()
        ss = math.fsum((x - m) ** 2 for x in self._values)
        return ss / (n - ddof)


class RollingMinMax:
    """Minimum and maximum of the last `window` values, with two monotonic deques of (index, value) pairs."""

    def __init__(self, window: int) -> None:
        if window < 1:
            raise ValueError("the window must hold at least one value")
        if window != int(window):
            raise ValueError("the window must be a whole number of values")
        self._window = window
        self._pushed = 0
        self._mins: deque[tuple[int, float]] = deque()
        self._maxs: deque[tuple[int, float]] = deque()

    def push(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be pushed")
        index = self._pushed
        self._pushed += 1
        while self._mins and self._mins[-1][1] >= x:
            self._mins.pop()
        self._mins.append((index, x))
        while self._maxs and self._maxs[-1][1] <= x:
            self._maxs.pop()
        self._maxs.append((index, x))
        oldest = index - self._window + 1
        while self._mins[0][0] < oldest:
            self._mins.popleft()
        while self._maxs[0][0] < oldest:
            self._maxs.popleft()

    def minimum(self) -> float:
        if self._pushed == 0:
            raise ValueError("no value has been pushed, so there is no minimum")
        return self._mins[0][1]

    def maximum(self) -> float:
        if self._pushed == 0:
            raise ValueError("no value has been pushed, so there is no maximum")
        return self._maxs[0][1]


class QuantileSketch:
    """Deterministic rank-error sketch: a list of tuples (value, g, delta), with no published sketch cited.

    With n values added, the tuples hold the stored values in sorted order, the sum of the g values is n, and
    g + delta never exceeds floor(2 * epsilon * n) + 1. For each stored value, some copy of it has an exact rank
    between the running sum of g up to it and that sum plus its delta. The specification on the project page
    states the guarantee.
    """

    def __init__(self, epsilon: float) -> None:
        if not (0.0 < epsilon < 1.0):
            raise ValueError("epsilon must be a number strictly between 0 and 1")
        self._exact_epsilon = Fraction(epsilon)
        self._n = 0
        self._values: list[float] = []
        self._g: list[int] = []
        self._delta: list[int] = []

    def add(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be added")
        position = bisect_right(self._values, x)
        delta = 0 if position == 0 or position == len(self._values) else self._g[position] + self._delta[position] - 1
        self._values.insert(position, float(x))
        self._g.insert(position, 1)
        self._delta.insert(position, delta)
        self._n += 1
        self._compress()

    def _compress(self) -> None:
        cap = math.floor(2 * self._exact_epsilon * self._n) + 1
        for i in range(len(self._values) - 2, 0, -1):
            if self._g[i] + self._g[i + 1] + self._delta[i + 1] <= cap:
                self._g[i + 1] += self._g[i]
                del self._values[i]
                del self._g[i]
                del self._delta[i]

    def quantile(self, q: float) -> float:
        if not (0.0 <= q <= 1.0):
            raise ValueError("q must lie in the closed interval [0, 1]")
        if self._n == 0:
            raise ValueError("the sketch is empty, so it has no quantiles")
        target = max(1, math.ceil(Fraction(q) * self._n - self._exact_epsilon * self._n))
        rank = 0
        for value, g in zip(self._values, self._g, strict=True):
            rank += g
            if rank >= target:
                return value
        return self._values[-1]
