"""Write the round-5 fixer's student-error mutants from the current reference (one edit each)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
REF = ROOT / "course/modules/CS/CS2/grader/reference.py"
OUT = ROOT / "ledgers/CS2/mutants"

MUTANTS: list[tuple[str, str, list[tuple[str, str]]]] = [
    (
        "f5_01_welford_update_drops_false.py",
        "Welford update returns at once on a False value, so the boolean is neither counted nor averaged.",
        [
            (
                "        self._count += 1\n        delta = x - self._mean",
                "        if x is False:\n            return\n        self._count += 1\n        delta = x - self._mean",
            )
        ],
    ),
    (
        "f5_02_window_truncates_float.py",
        "RollingMinMax truncates a non-integral float window with int(), so the window 2.5 becomes 2.",
        [
            ("        if window != int(window):\n            raise ValueError(\"the window must be a whole number of values\")\n", ""),
            ("        self._window = window", "        self._window = int(window)"),
        ],
    ),
    (
        "f5_03_sketch_add_drops_false.py",
        "QuantileSketch.add returns without adding a False value, as if it were not a number.",
        [("        position = bisect_right(self._values, x)", "        if x is False:\n            return\n        position = bisect_right(self._values, x)")],
    ),
    (
        "f5_04_rolling_push_drops_true.py",
        "RollingMinMax.push ignores a True value, so a boolean never enters the window.",
        [("        index = self._pushed\n", "        if x is True:\n            return\n        index = self._pushed\n")],
    ),
    (
        "f5_05_variance_string_ddof_is_sample.py",
        "variance treats every string ddof as the sample divisor, so the string '2' is answered instead of refused.",
        [
            (
                "    def variance(self, ddof: int = 1) -> float:\n        if self._count == 0:",
                "    def variance(self, ddof: int = 1) -> float:\n        if isinstance(ddof, str):\n            ddof = 1\n        if self._count == 0:",
            )
        ],
    ),
    (
        "f5_06_variance_none_ddof_is_population.py",
        "variance reads a None ddof as 0 and answers the population variance instead of raising.",
        [
            (
                "    def variance(self, ddof: int = 1) -> float:\n        if self._count == 0:",
                "    def variance(self, ddof: int = 1) -> float:\n        if ddof is None:\n            ddof = 0\n        if self._count == 0:",
            )
        ],
    ),
    (
        "f5_07_rolling_none_window_is_one.py",
        "RollingMinMax reads a None window as a window of one, so the call answers instead of raising.",
        [("        if window < 1:", "        if window is None:\n            window = 1\n        if window < 1:")],
    ),
    (
        "f5_08_sketch_skips_padded_string.py",
        "QuantileSketch.add silently skips a whitespace-padded string instead of refusing it or reading it.",
        [
            (
                "    def add(self, x: float) -> None:\n        if math.isnan(x):",
                "    def add(self, x: float) -> None:\n        if isinstance(x, str) and x != x.strip():\n            return\n        if math.isnan(x):",
            )
        ],
    ),
    (
        "f5_09_variance_float_one_is_population.py",
        "variance answers a float ddof of 1.0 with the population variance, although 1.0 denotes the sample divisor.",
        [("        if ddof == 0:\n            return self._m2 / self._count", "        if isinstance(ddof, float) and ddof == 1.0:\n            return self._m2 / self._count\n        if ddof == 0:\n            return self._m2 / self._count")],
    ),
    (
        "f5_10_rolling_push_reads_padded_as_zero.py",
        "RollingMinMax.push reads a whitespace-padded string as 0.0 instead of refusing it or reading the number.",
        [
            (
                "    def push(self, x: float) -> None:\n        if math.isnan(x):",
                "    def push(self, x: float) -> None:\n        if isinstance(x, str) and x != x.strip():\n            x = 0.0\n        if math.isnan(x):",
            )
        ],
    ),
]


def main() -> None:
    base = REF.read_text(encoding="utf-8")
    base = re.sub(r'\A""".*?"""\n', "", base, count=1, flags=re.DOTALL)
    for name, description, edits in MUTANTS:
        text = base
        for old, new in edits:
            count = text.count(old)
            if count != 1:
                raise SystemExit(f"{name}: expected one match, found {count}: {old[:60]!r}")
            text = text.replace(old, new)
        header = f'"""{description}\n\nMutant of the reference solution (round-5 fixer, one student error).\n"""\n'
        (OUT / name).write_text(header + text, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
