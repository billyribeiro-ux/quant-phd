"""Writes three new student-error mutants (complete solution modules) from the grader's reference.py.

Each mutant changes exactly one statement of the reference (asserted to match once) and its first docstring line
names the error. Usage: python -I make_mutants_r14.py <reference.py> <output dir>
"""

from __future__ import annotations

import sys
from pathlib import Path

ref = Path(sys.argv[1]).read_text(encoding="utf-8")
out = Path(sys.argv[2])

MUTANTS = {
    "r14_01_welford_m2_increment_sign_flipped.py": (
        "Welford M2 is decreased by delta times the new deviation (a sign error), so the variance goes negative.",
        "        self._m2 += delta * (x - self._mean)",
        "        self._m2 -= delta * (x - self._mean)",
    ),
    "r14_02_quantile_tests_rank_upper_bound.py": (
        "quantile returns the first stored value whose upper rank bound (running g plus delta) reaches the target.",
        "        for value, g in zip(self._values, self._g, strict=True):\n            rank += g\n            if rank >= target:",
        "        for value, g, d in zip(self._values, self._g, self._delta, strict=True):\n            rank += g\n            if rank + d >= target:",
    ),
    "r14_03_welford_mean_divisor_clamped.py": (
        "Welford mean divides by max(count - 1, 1), so the second value is averaged with the wrong divisor.",
        "        self._mean += delta / self._count",
        "        self._mean += delta / max(self._count - 1, 1)",
    ),
}

for name, (first_line, old, new) in MUTANTS.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    body = ref.replace(old, new)
    head, rest = body.split('"""', 2)[1], body.split('"""', 2)[2]
    doc_rest = head.split("\n", 1)[1] if "\n" in head else ""
    text = f'"""{first_line}\n{doc_rest}"""{rest}'
    (out / name).write_text(text, encoding="utf-8")
    print("wrote", name)
