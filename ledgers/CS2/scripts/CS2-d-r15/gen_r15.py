"""Generate round-15 student-error mutants and correct alternatives from the grader's reference.py.

Each edit replaces one unique string of the reference; the generator asserts the string occurs exactly once.
"""

import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD15-CS2-d")
REF = (ROOT / "course/modules/CS/CS2/grader/reference.py").read_text(encoding="utf-8")
SCRIPT = ROOT / "ledgers/CS2/scripts/CS2-d-r15"
MUT = ROOT / "ledgers/CS2/mutants"
ALT = SCRIPT / "alts"


def edit(pairs: list[tuple[str, str]]) -> str:
    text = REF
    for old, new in pairs:
        n = text.count(old)
        assert n == 1, f"expected one occurrence, found {n}: {old[:60]!r}"
        text = text.replace(old, new)
    return text


MUTANTS = {
    "r15_04_sketch_interior_delta_without_minus_one.py": (
        "Sketch: a new interior tuple takes delta = g + delta of its successor (the rule has - 1).",
        [("self._g[position] + self._delta[position] - 1", "self._g[position] + self._delta[position]")],
    ),
    "r15_05_sample_variance_one_value_zero_division.py": (
        "Welford variance(1): the guard tests count < 1, so one value reaches a division by zero (ZeroDivisionError, not ValueError).",
        [("        if self._count < 2:\n", "        if self._count < 1:\n")],
    ),
    "r15_06_sketch_interior_delta_is_floor_2en.py": (
        "Sketch: a new interior tuple takes delta = floor(2 * epsilon * n) (the cap) instead of the successor rule.",
        [
            (
                "else self._g[position] + self._delta[position] - 1",
                "else math.floor(2 * self._exact_epsilon * (self._n + 1))",
            )
        ],
    ),
    "r15_07_welford_nan_checked_after_state_change.py": (
        "Welford update: the NaN check runs after count and M2 have changed, so a rejected NaN leaves count incremented.",
        [
            (
                '        if math.isnan(x):\n            raise ValueError("a NaN value is not a number and cannot be added")\n        self._count += 1\n',
                "        self._count += 1\n",
            ),
            (
                "        self._m2 += delta * (x - self._mean)\n",
                '        self._m2 += delta * (x - self._mean)\n        if math.isnan(x):\n            raise ValueError("a NaN value is not a number and cannot be added")\n',
            ),
        ],
    ),
    "r15_08_quantile_target_float_q_times_n.py": (
        "Sketch quantile: the rank target is computed as q * n - epsilon * n in floats (q is a float, not a Fraction).",
        [
            (
                "target = max(1, math.ceil(Fraction(q) * self._n - self._exact_epsilon * self._n))",
                "target = max(1, math.ceil(q * self._n - self._exact_epsilon * self._n))",
            )
        ],
    ),
}

ALTERNATIVES = {
    "alt_r15_A_exact_sorted_storage.py": (
        "Exact storage (no sketch): keeps every value sorted; quantile returns the value at the exact rank max(1, ceil(qn - eps n)).",
        None,
    ),
    "alt_r15_B_decimal_exact_target.py": (
        "Reference sketch, rank target computed with decimal.Decimal at 200 digits (exact for every float).",
        [
            (
                "target = max(1, math.ceil(Fraction(q) * self._n - self._exact_epsilon * self._n))",
                "from decimal import Decimal, localcontext\n"
                "        with localcontext() as ctx:\n"
                "            ctx.prec = 200\n"
                "            diff = Decimal(q) * self._n - Decimal(float(self._exact_epsilon)) * self._n\n"
                "        target = max(1, math.ceil(diff))",
            )
        ],
    ),
    "alt_r15_C_float_cutoff_no_floor.py": (
        "Reference sketch, compression cutoff as a float comparison g + g + delta <= 2 * eps * n (no floor, no +1).",
        [
            (
                "if self._g[i] + self._g[i + 1] + self._delta[i + 1] <= cap:",
                "if self._g[i] + self._g[i + 1] + self._delta[i + 1] <= 2 * float(self._exact_epsilon) * self._n:",
            )
        ],
    ),
    "alt_r15_D_welford_alt_arithmetic.py": (
        "Welford with the mean update delta / n and M2 increment delta * delta * (n - 1) / n (algebraically equal, different rounding).",
        [
            (
                "        self._m2 += delta * (x - self._mean)\n",
                "        self._m2 += delta * delta * (self._count - 1) / self._count\n",
            )
        ],
    ),
    "alt_r15_E_rolling_list_bruteforce.py": (
        "RollingMinMax by brute force over the last window values kept in a plain list.",
        None,
    ),
}

EXACT_SORTED = '''import math
from fractions import Fraction


class WelfordAccumulator:
    def __init__(self) -> None:
        self._count = 0
        self._mean = 0.0
        self._m2 = 0.0

    def update(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be added")
        self._count += 1
        delta = x - self._mean
        self._mean += delta / self._count
        self._m2 += delta * (x - self._mean)

    @property
    def count(self) -> int:
        return self._count

    def mean(self) -> float:
        if self._count == 0:
            raise ValueError("the mean is undefined before the first value")
        return self._mean

    def variance(self, ddof: int = 1) -> float:
        if self._count == 0:
            raise ValueError("the variance is undefined before the first value")
        if ddof == 0:
            return self._m2 / self._count
        if ddof == 1:
            if self._count < 2:
                raise ValueError("the sample variance needs at least two values")
            return self._m2 / (self._count - 1)
        raise TypeError("ddof must be 0 or 1")


class RollingMinMax:
    def __init__(self, window: int) -> None:
        if window < 1:
            raise ValueError("the window must hold at least one value")
        if window != int(window):
            raise ValueError("the window must be a whole number of values")
        self._window = int(window)
        self._last: list[float] = []

    def push(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be pushed")
        self._last.append(x)
        del self._last[: max(0, len(self._last) - self._window)]

    def minimum(self) -> float:
        if not self._last:
            raise ValueError("no value has been pushed, so there is no minimum")
        return min(self._last)

    def maximum(self) -> float:
        if not self._last:
            raise ValueError("no value has been pushed, so there is no maximum")
        return max(self._last)


class QuantileSketch:
    def __init__(self, epsilon: float) -> None:
        if not (0.0 < epsilon < 1.0):
            raise ValueError("epsilon must be a number strictly between 0 and 1")
        self._exact_epsilon = Fraction(epsilon)
        self._sorted: list[float] = []

    def add(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be added")
        lo, hi = 0, len(self._sorted)
        while lo < hi:
            mid = (lo + hi) // 2
            if self._sorted[mid] <= x:
                lo = mid + 1
            else:
                hi = mid
        self._sorted.insert(lo, float(x))

    def quantile(self, q: float) -> float:
        if not (0.0 <= q <= 1.0):
            raise ValueError("q must lie in the closed interval [0, 1]")
        n = len(self._sorted)
        if n == 0:
            raise ValueError("the sketch is empty, so it has no quantiles")
        target = max(1, math.ceil(Fraction(q) * n - self._exact_epsilon * n))
        return self._sorted[min(target, n) - 1]
'''

ROLLING_BRUTE = None  # built inside main from the exact-sorted file's classes is not needed: see below


def main() -> int:
    for name, (_, pairs) in MUTANTS.items():
        (MUT / name).write_text(edit(pairs), encoding="utf-8")
        print("mutant", name)
    ALT.mkdir(parents=True, exist_ok=True)
    for name, (_, pairs) in ALTERNATIVES.items():
        if name == "alt_r15_A_exact_sorted_storage.py":
            text = EXACT_SORTED
        elif name == "alt_r15_E_rolling_list_bruteforce.py":
            text = edit([])  # reference, with RollingMinMax replaced below
            start = text.index("class RollingMinMax:")
            end = text.index("class QuantileSketch:")
            roll = (
                "class RollingMinMax:\n"
                "    def __init__(self, window: int) -> None:\n"
                "        if window < 1:\n"
                '            raise ValueError("the window must hold at least one value")\n'
                "        if window != int(window):\n"
                '            raise ValueError("the window must be a whole number of values")\n'
                "        self._window = int(window)\n"
                "        self._last: list[float] = []\n"
                "        self._pushed = 0\n"
                "\n"
                "    def push(self, x: float) -> None:\n"
                "        if math.isnan(x):\n"
                '            raise ValueError("a NaN value is not a number and cannot be pushed")\n'
                "        self._pushed += 1\n"
                "        self._last.append(float(x))\n"
                "        if len(self._last) > self._window:\n"
                "            self._last.pop(0)\n"
                "\n"
                "    def minimum(self) -> float:\n"
                "        if self._pushed == 0:\n"
                '            raise ValueError("no value has been pushed, so there is no minimum")\n'
                "        return min(self._last)\n"
                "\n"
                "    def maximum(self) -> float:\n"
                "        if self._pushed == 0:\n"
                '            raise ValueError("no value has been pushed, so there is no maximum")\n'
                "        return max(self._last)\n"
                "\n\n"
            )
            text = text[:start] + roll + text[end:]
        else:
            text = edit(pairs)
        (ALT / name).write_text(text, encoding="utf-8")
        print("alternative", name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
