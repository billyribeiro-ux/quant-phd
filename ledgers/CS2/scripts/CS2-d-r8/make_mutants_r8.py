"""Round-8 verifier script: derive new student-error mutants of the reference solution (each replacement must match once)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyB8-CS2-d")
REF = (ROOT / "course/modules/CS/CS2/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/CS2/mutants"

MUTANTS = {
    "d8_01_sketch_cap_counts_previous_value.py": (
        "Quantile sketch compresses against the cap for n - 1 values, one value behind the count it must respect.",
        [("cap = math.floor(2 * self._exact_epsilon * self._n) + 1", "cap = math.floor(2 * self._exact_epsilon * (self._n - 1)) + 1")],
    ),
    "d8_02_sketch_insert_bisect_left.py": (
        "Quantile sketch inserts a new value before any equal stored values (bisect_left), so the delta is taken from the wrong neighbour.",
        [("position = bisect_right(self._values, x)", "position = bisect_left(self._values, x)"),
         ("from bisect import bisect_right", "from bisect import bisect_left, bisect_right")],
    ),
    "d8_03_variance_ddof_truncated_to_int.py": (
        "variance truncates ddof to an int before it is compared, so a float ddof of 0.5 is answered as the population variance.",
        [("        if self._count == 0:\n            raise ValueError(\"the variance is undefined before the first value\")\n        if ddof == 0:",
          "        if self._count == 0:\n            raise ValueError(\"the variance is undefined before the first value\")\n        ddof = int(ddof)\n        if ddof == 0:")],
    ),
    "d8_04_quantile_rounds_q_to_six_places.py": (
        "quantile rounds q to six decimal places before it forms the exact rank target, a student's float-noise guard that changes the target near a whole rank.",
        [("target = max(1, math.ceil(Fraction(q) * self._n - self._exact_epsilon * self._n))",
          "target = max(1, math.ceil(Fraction(round(q, 6)) * self._n - self._exact_epsilon * self._n))")],
    ),
}

for name, (doc, reps) in MUTANTS.items():
    src = REF
    for old, new in reps:
        assert src.count(old) == 1, (name, old[:60], src.count(old))
        src = src.replace(old, new)
    body = src.split('"""', 2)
    # replace the module docstring with the one-line description, keeping the rest of the module
    rest = src[src.index('"""', 3) + 3:]
    (OUT / name).write_text(f'"""{doc}"""\n' + rest, encoding="utf-8")
    print("wrote", name)
