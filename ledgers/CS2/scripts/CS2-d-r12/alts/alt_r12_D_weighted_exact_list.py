"""Alternative D: exact weighted list of distinct values with counts; Welford reference; rolling reference; rank by counts."""

from __future__ import annotations

import importlib.util
import math
from bisect import bisect_left
from fractions import Fraction
from pathlib import Path

_REF = Path("/Users/billyribeiro/.fanout/wt/verifyD12-CS2-d/course/modules/CS/CS2/grader/reference.py")
_spec = importlib.util.spec_from_file_location("ref_for_alt_d", _REF)
assert _spec is not None and _spec.loader is not None
_ref = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ref)

WelfordAccumulator = _ref.WelfordAccumulator
RollingMinMax = _ref.RollingMinMax


class QuantileSketch:
    def __init__(self, epsilon: float) -> None:
        if not (0.0 < epsilon < 1.0):
            raise ValueError("epsilon outside (0, 1)")
        self._eps = Fraction(epsilon)
        self._vals: list[float] = []
        self._cnt: list[int] = []
        self._n = 0

    def add(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("NaN")
        x = float(x)
        i = bisect_left(self._vals, x)
        if i < len(self._vals) and self._vals[i] == x:
            self._cnt[i] += 1
        else:
            self._vals.insert(i, x)
            self._cnt.insert(i, 1)
        self._n += 1

    def quantile(self, q: float) -> float:
        if not (0.0 <= q <= 1.0):
            raise ValueError("q outside [0, 1]")
        if self._n == 0:
            raise ValueError("empty sketch")
        target = max(1, math.ceil(Fraction(q) * self._n - self._eps * self._n))
        running = 0
        for v, c in zip(self._vals, self._cnt):
            running += c
            if running >= target:
                return v
        return self._vals[-1]
