# ruff: noqa: E501
"""Round-5 verifier (CS2-d): two CORRECT alternative implementations derived from the reference by changing internals.

alt_r5_1: Welford in exact Fraction arithmetic (floats returned by mean and variance).
alt_r5_2: RollingMinMax by a naive scan of the last `window` (value, index) pairs, no monotonic deques.
Both keep the reference's named ValueError conditions and its public signatures. Each replacement must match once.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
REF = (ROOT / "course/modules/CS/CS2/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/CS2/scripts/CS2-d-r5/alts"
OUT.mkdir(parents=True, exist_ok=True)


def once(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, f"replacement target found {text.count(old)} times: {old[:60]!r}"
    return text.replace(old, new)


alt1 = REF
alt1 = once(
    alt1,
    "        self._mean = 0.0\n        self._m2 = 0.0\n",
    "        self._mean = 0.0\n        self._m2 = 0.0\n        self._mean_exact = Fraction(0)\n        self._m2_exact = Fraction(0)\n",
)
alt1 = once(
    alt1,
    "        self._count += 1\n        delta = x - self._mean\n        self._mean += delta / self._count\n        self._m2 += delta * (x - self._mean)\n",
    "        self._count += 1\n        xf = Fraction(x)\n        delta = xf - self._mean_exact\n        self._mean_exact += delta / self._count\n"
    "        self._m2_exact += delta * (xf - self._mean_exact)\n        self._mean = float(self._mean_exact)\n        self._m2 = float(self._m2_exact)\n",
)
(OUT / "alt_r5_1_welford_exact_fraction.py").write_text(alt1, encoding="utf-8")

rolling = '''class RollingMinMax:
    """Minimum and maximum of the last `window` values by a naive scan of the stored pairs (no deques)."""

    def __init__(self, window: int) -> None:
        if window < 1:
            raise ValueError("the window must hold at least one value")
        if window != int(window):
            raise ValueError("the window must be a whole number of values")
        self._window = window
        self._pushed = 0
        self._recent: list[float] = []

    def push(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be pushed")
        self._pushed += 1
        self._recent.append(x)
        if len(self._recent) > self._window:
            del self._recent[0]

    def minimum(self) -> float:
        if self._pushed == 0:
            raise ValueError("no value has been pushed, so there is no minimum")
        return min(self._recent)

    def maximum(self) -> float:
        if self._pushed == 0:
            raise ValueError("no value has been pushed, so there is no maximum")
        return max(self._recent)


'''
alt2 = re.sub(r"class RollingMinMax:.*?(?=class QuantileSketch:)", lambda _m: rolling, REF, count=1, flags=re.S)
assert alt2 != REF
(OUT / "alt_r5_2_rolling_naive_scan.py").write_text(alt2, encoding="utf-8")
print("wrote alt_r5_1_welford_exact_fraction.py and alt_r5_2_rolling_naive_scan.py")
