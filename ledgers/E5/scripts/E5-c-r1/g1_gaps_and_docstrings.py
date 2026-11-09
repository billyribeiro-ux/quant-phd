"""Gap values, CU docstring and changed-line symbol check for E5 slice c (verifier G1, round 1). Run with python -I."""

from __future__ import annotations

import re
import subprocess
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
c, dG = F(3, 5), F(10000)
target = dG / (1 - c)
S = lambda n: sum(dG * c**k for k in range(n))  # noqa: E731
for n, shown in ((1, "15000"), (5, "1944"), (10, "151.165440"), (20, "0.914040"), (30, "0.005527")):
    gap = target - S(n)
    print(f"gap N={n} exact={float(gap):.6f} printed={shown} ok={f'{float(gap):.6f}' == shown}")
print("Y before 162500 + 25000 = 187500:", 162500 + 25000 == 187500)
twin = (ROOT / "tests/labs/E5/lab-E5-L08-1.py").read_text(encoding="utf-8")
print("L08 twin docstring 'CU' mention:", re.findall(r"[^.\n]*CU[^.\n]*", twin)[:2])
print("L08 twin docstring 100 cents per CU in page line 58:", "100 cents" in (ROOT / "course/modules/E/E5/L08.html").read_text(encoding="utf-8"))

# symbols inside the two changed L07 lines (52, 227) and L08 line 52: old vs new
def math_tokens(text: str) -> set[str]:
    return set(re.findall(r"\\\((.*?)\\\)", text))

for name, line_no in (("L07", 52), ("L07", 227), ("L08", 52)):
    new = (ROOT / f"course/modules/E/E5/{name}.html").read_text(encoding="utf-8").splitlines()[line_no - 1]
    old = subprocess.run(
        ["git", "show", f"95f3f8cb:course/modules/E/E5/{name}.html"], capture_output=True, text=True, check=True, cwd=ROOT
    ).stdout.splitlines()[line_no - 1]
    print(f"{name}:{line_no} new math tokens subset of old: {math_tokens(new) <= math_tokens(old)} "
          f"new-only={sorted(math_tokens(new) - math_tokens(old))}")
