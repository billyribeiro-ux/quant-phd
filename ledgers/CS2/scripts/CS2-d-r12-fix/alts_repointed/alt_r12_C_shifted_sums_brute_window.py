"""Alternative C: sums of deviations from the first value (shifted sums); brute-force rolling over a kept list; reference sketch."""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path

_REF = Path("/Users/billyribeiro/dev/quant-phd/course/modules/CS/CS2/grader/reference.py")
_spec = importlib.util.spec_from_file_location("ref_for_alt_c", _REF)
assert _spec is not None and _spec.loader is not None
_ref = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ref)


class WelfordAccumulator:
    def __init__(self) -> None:
        self._shift: float | None = None
        self._n = 0
        self._s = 0.0
        self._ss = 0.0

    def update(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("NaN")
        if self._shift is None:
            self._shift = float(x)
        d = float(x) - self._shift
        self._n += 1
        self._s += d
        self._ss += d * d

    @property
    def count(self) -> int:
        return self._n

    def mean(self) -> float:
        if self._n == 0 or self._shift is None:
            raise ValueError("no values")
        return self._shift + self._s / self._n

    def variance(self, ddof: int = 1) -> float:
        if self._n == 0:
            raise ValueError("no values")
        if ddof not in (0, 1):
            raise TypeError("ddof 0 or 1")
        if ddof == 1 and self._n < 2:
            raise ValueError("needs two values")
        m2 = self._ss - self._s * self._s / self._n
        return m2 / self._n if ddof == 0 else m2 / (self._n - 1)


class RollingMinMax:
    def __init__(self, window: int) -> None:
        if window < 1:
            raise ValueError("window below one")
        if window != int(window):
            raise ValueError("window not whole")
        self._w = int(window)
        self._xs: list[float] = []

    def push(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("NaN")
        self._xs.append(float(x))

    def minimum(self) -> float:
        if not self._xs:
            raise ValueError("nothing pushed")
        return min(self._xs[-self._w :])

    def maximum(self) -> float:
        if not self._xs:
            raise ValueError("nothing pushed")
        return max(self._xs[-self._w :])


QuantileSketch = _ref.QuantileSketch
