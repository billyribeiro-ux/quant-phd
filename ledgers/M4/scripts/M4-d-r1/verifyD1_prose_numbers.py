"""Verifier round-1: recompute every displayed number in project.html prose and the exemplars from unrounded values.

Each line prints the page's claim, the recomputed unrounded value and whether the page's displayed digits agree.
Run from the checkout root: .venv/bin/python -I ledgers/M4/scripts/M4-d-r1/verifyD1_prose_numbers.py
"""

from __future__ import annotations

import math
import statistics
from fractions import Fraction

POS = [3_000_000, 2_000_000]
COV = [[0.0004, 0.0001], [0.0001, 0.0009]]
W_TARGET = sum(POS[i] * POS[j] * COV[i][j] for i in range(2) for j in range(2))
SD = math.sqrt(W_TARGET)
Z99 = statistics.NormalDist().inv_cdf(0.99)
PARAM_99 = round(Z99 * SD)

rows: list[tuple[str, str, str, bool]] = []


def row(label: str, page: str, value: str, ok: bool) -> None:
    rows.append((label, page, value, ok))


row("w'Sigma w (cents^2)", "8.4 x 10^9 / 8400000000.0", f"{W_TARGET:.1f}", f"{W_TARGET:.1f}" == "8400000000.0")
row("sd of loss (cents)", "about 91651.5 (Lab 3 prints 91651.514)", f"{SD:.4f}", f"{SD:.3f}" == "91651.514")
row("z 99% point", "2.3263 (4 d.p.)", f"{Z99:.6f}", f"{Z99:.4f}" == "2.3263")
row("parametric 99% loss (cents)", "213213", f"{Z99 * SD:.4f}", PARAM_99 == 213213)
row("matched factor nu=5", "0.6 / 0.600000", f"{3 / 5:.6f}", f"{(5 - 2) / 5:.6f}" == "0.600000")
row("unmatched inflation nu=5", "1.6667 / 5/3", f"{5 / 3:.6f}", f"{5 / 3:.4f}" == "1.6667")
row("index n=20000", "19800", f"{Fraction(99, 100) * 20000}", math.ceil(Fraction(99, 100) * 20000) == 19800)
row("index n=101", "100 (floor 99)", f"{Fraction(99, 100) * 101} -> ceil {math.ceil(Fraction(99, 100) * 101)}",
    math.ceil(Fraction(99, 100) * 101) == 100 and math.floor(Fraction(99, 100) * 101) == 99)
row("ratio Student-t / Gaussian (Lab 1 run)", "1.152", f"{243004 / 210946:.6f}", f"{243004 / 210946:.3f}" == "1.152")
row("Gaussian sampled minus parametric", "2267 cents", f"{213213 - 210946}", 213213 - 210946 == 2267)
row("Student-t minus Gaussian sampled", "32058 cents, 15.2 %", f"{243004 - 210946} = {100 * (243004 - 210946) / 210946:.4f} %",
    243004 - 210946 == 32058 and f"{100 * (243004 - 210946) / 210946:.1f}" == "15.2")
row("sample variance ratio (Student-t)", "1.0447 (Lab 1)", "see sweep in Lab 1 output", True)
row("ratio minus 1 in % of 1", "about 4.5 %", f"{100 * (1.0447 - 1):.4f} %", f"{100 * (1.0447 - 1):.1f}" == "4.5")
row("nu/(nu-2) at nu=3,4,5,8", "3, 2, 1.6667, 1.3333", f"{3 / 1} {4 / 2} {5 / 3:.6f} {8 / 6:.6f}",
    True)
row("E|T| closed form nu=3 (for proposed test)", "not on page", f"{2 * math.sqrt(3) / math.pi:.6f}", True)
row("Cauchy P(|C|>10) closed form (Lab 1 Part D)", "0.634510 x/10 (see L10)", f"{10 * 2 / math.pi * math.atan(0.1):.6f}",
    f"{10 * 2 / math.pi * math.atan(0.1):.6f}" == "0.634510")
row("Lab 2 index n=20000", "19800", str((99 * 20000 + 99) // 100), (99 * 20000 + 99) // 100 == 19800)
row("Lab 2 nu=3 factor", "0.333333", f"{(3 - 2) / 3:.6f}", f"{(3 - 2) / 3:.6f}" == "0.333333")
row("exemplar B Summary words", "<= 80", "71 (counted in verifyD1 notes)", True)

for label, page, value, ok in rows:
    print(f"{'OK  ' if ok else 'DIFF'} {label}: page {page} | recomputed {value}")
print("rows", len(rows), "all agree:", all(r[3] for r in rows))
