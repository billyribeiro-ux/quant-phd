"""Alternative B (round 8): reflection_tail by Simpson quadrature of the normal density only (no erfc); rest as the reference."""
from __future__ import annotations

import importlib.util
import math
from typing import Any

_spec = importlib.util.spec_from_file_location("ref_r8", "/Users/billyribeiro/.fanout/wt/verifyE9-SC1-d/course/modules/SC/SC1/grader/reference.py")
_ref = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_ref)


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("a must be positive")
    if t <= 0:
        raise ValueError("t must be positive")
    top = a + 14.0 * math.sqrt(t)
    n = 20000
    h = (top - a) / n

    def dens(x: float) -> float:
        return math.exp(-x * x / (2.0 * t)) / math.sqrt(2.0 * math.pi * t)

    s = dens(a) + dens(top)
    for k in range(1, n):
        s += (4.0 if k % 2 else 2.0) * dens(a + k * h)
    return 2.0 * s * h / 3.0


discrete_max_exceedance = _ref.discrete_max_exceedance
nested_grid_counts = _ref.nested_grid_counts
srw_max_count = _ref.srw_max_count
srw_terminal_count = _ref.srw_terminal_count
