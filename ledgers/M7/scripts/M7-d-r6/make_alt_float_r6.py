"""Round 6 (M7-d) alternative correct implementation: the reference active-set solver in float arithmetic with
different numerical cutoffs (1e-9 pivot and rate tests, 1e-12 zero tests). Writes ws/alt_float/constrained_allocator.py."""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB6-M7-d")
SRC = (ROOT / "course/modules/M/M7/grader/reference.py").read_text(encoding="utf-8")
body = SRC
reps = [
    ("from fractions import Fraction\n", "Fraction = float\n"),
    ("TOL = Fraction(1, 10**9)", "TOL = 1e-9"),
    ("return Fraction(repr(value))  # the decimal text the case carries, read exactly", "return float(value)"),
    ("    return Fraction(value)\n", "    return float(value)\n"),
    ("pivot = next(r for r in range(col, size) if rows[r][col] != 0)", "pivot = max(range(col, size), key=lambda r: abs(rows[r][col]))"),
    ("if r != col and rows[r][col] != 0:", "if r != col and abs(rows[r][col]) > 1e-14:"),
    ("pivot = next((r for r in range(rank, len(rows)) if rows[r][col] != 0), None)", "pivot = max(range(rank, len(rows)), key=lambda r: abs(rows[r][col]), default=None)\n        if pivot is not None and abs(rows[pivot][col]) <= 1e-12:\n            pivot = None"),
    ("if r != rank and rows[r][col] != 0:", "if r != rank and abs(rows[r][col]) > 1e-12:"),
    ("if all(v == 0 for v in p):", "if all(abs(v) <= 1e-11 for v in p):"),
    ("negative = [(lam[1 + k], k) for k in range(len(working)) if lam[1 + k] < 0]", "negative = [(lam[1 + k], k) for k in range(len(working)) if lam[1 + k] < -1e-11]"),
    ("if rate > 0:", "if rate > 1e-12:"),
    ("if ratio < step:", "if ratio < step - 1e-15:"),
    ("if _rank([budget, *(rows[j][0] for j in working), candidate]) <= len(working) + 1:", "if _rank([budget, *(rows[j][0] for j in working), candidate]) <= len(working) + 1:"),
]
for old, new in reps:
    n = body.count(old)
    if n == 0:
        print("NOT FOUND:", old[:70], file=sys.stderr)
        raise SystemExit(1)
    body = body.replace(old, new)
out = ROOT / "ledgers/M7/scripts/M7-d-r6/alt_float/constrained_allocator.py"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(body, encoding="utf-8")
print("wrote", out, "lines", body.count("\n"))
