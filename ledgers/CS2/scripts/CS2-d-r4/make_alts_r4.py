"""Build round-4 alternative correct implementations from the reference (verifier round 4).

Each alternative keeps the reference's Welford and rolling classes unless stated, and replaces the quantile sketch
with a different correct algorithm. Writes into ledgers/CS2/scripts/CS2-d-r4/alts/.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/CS/CS2/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/CS2/scripts/CS2-d-r4/alts"
HEAD, _, _ = REF.partition("class QuantileSketch:")

STORE_ALL_FLOOR = '''class QuantileSketch:
    """Alternative A (verifier round 4): exact sorted list; answer is the value of rank min(n, floor(q n) + 1)."""

    def __init__(self, epsilon: float) -> None:
        if not (0.0 < epsilon < 1.0):
            raise ValueError("epsilon must be a number strictly between 0 and 1")
        self._values: list[float] = []

    def add(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be added")
        bisect.insort(self._values, float(x))

    def quantile(self, q: float) -> float:
        if not (0.0 <= q <= 1.0):
            raise ValueError("q must lie in the closed interval [0, 1]")
        n = len(self._values)
        if n == 0:
            raise ValueError("the sketch is empty, so it has no quantiles")
        k = min(n, math.floor(Fraction(q) * n) + 1)
        return self._values[k - 1]
'''

STORE_ALL_CEIL = '''class QuantileSketch:
    """Alternative B (verifier round 4): exact sorted list with the exact rank target of the specification."""

    def __init__(self, epsilon: float) -> None:
        if not (0.0 < epsilon < 1.0):
            raise ValueError("epsilon must be a number strictly between 0 and 1")
        self._exact_epsilon = Fraction(epsilon)
        self._values: list[float] = []

    def add(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be added")
        bisect.insort(self._values, float(x))

    def quantile(self, q: float) -> float:
        if not (0.0 <= q <= 1.0):
            raise ValueError("q must lie in the closed interval [0, 1]")
        n = len(self._values)
        if n == 0:
            raise ValueError("the sketch is empty, so it has no quantiles")
        target = max(1, math.ceil(Fraction(q) * n - self._exact_epsilon * n))
        return self._values[target - 1]
'''

STORE_ALL_DECIMAL = '''class QuantileSketch:
    """Alternative D (verifier round 4): exact sorted list; the rank target is computed in Decimal from the exact floats."""

    def __init__(self, epsilon: float) -> None:
        if not (0.0 < epsilon < 1.0):
            raise ValueError("epsilon must be a number strictly between 0 and 1")
        self._epsilon = epsilon
        self._values: list[float] = []

    def add(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be added")
        bisect.insort(self._values, float(x))

    def quantile(self, q: float) -> float:
        if not (0.0 <= q <= 1.0):
            raise ValueError("q must lie in the closed interval [0, 1]")
        n = len(self._values)
        if n == 0:
            raise ValueError("the sketch is empty, so it has no quantiles")
        with localcontext() as ctx:
            ctx.prec = 80
            gap = Decimal(q) * n - Decimal(self._epsilon) * n
            target = max(1, int(gap.to_integral_value(rounding=ROUND_CEILING)))
        return self._values[target - 1]
'''

WELFORD_COERCE = '''class RollingMinMax:
    """Minimum and maximum of the last `window` values; string and float windows that denote a whole number are
    read as that number (alternative C, verifier round 4)."""

    def __init__(self, window: int) -> None:
        if window is None:
            raise TypeError("the window must be a number, not None")
        number = float(window)
        if math.isnan(number) or math.isinf(number):
            raise ValueError("the window must be a finite number")
        if number < 1:
            raise ValueError("the window must hold at least one value")
        if number != int(number):
            raise ValueError("the window must be a whole number of values")
        self._window = int(number)
        self._pushed = 0
        self._mins: deque[tuple[int, float]] = deque()
        self._maxs: deque[tuple[int, float]] = deque()
'''


def splice(body: str) -> str:
    head = HEAD.replace("from bisect import bisect_right\n", "import bisect\nfrom bisect import bisect_right\n", 1)
    head = head.replace(
        "from fractions import Fraction\n",
        "from decimal import ROUND_CEILING, Decimal, localcontext\nfrom fractions import Fraction\n",
        1,
    )
    return head + body


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "alt_r4_A_store_all_floor_plus_one.py").write_text(splice(STORE_ALL_FLOOR), encoding="utf-8")
    (OUT / "alt_r4_B_store_all_exact_ceiling.py").write_text(splice(STORE_ALL_CEIL), encoding="utf-8")
    (OUT / "alt_r4_D_store_all_decimal_target.py").write_text(splice(STORE_ALL_DECIMAL), encoding="utf-8")
    # C: the reference with its RollingMinMax __init__ replaced; the rest of the reference is kept.
    ref_rolling_start = REF.index("class RollingMinMax:")
    ref_rolling_init_end = REF.index("    def push(self, x: float) -> None:", ref_rolling_start)
    rolling_rest = REF[ref_rolling_init_end:]
    alt_c = REF[:ref_rolling_start] + WELFORD_COERCE + "\n" + rolling_rest
    alt_c = alt_c.replace("from bisect import bisect_right\n", "from bisect import bisect_right\n", 1)
    (OUT / "alt_r4_C_rolling_coerces_whole_window.py").write_text(alt_c, encoding="utf-8")


if __name__ == "__main__":
    main()
