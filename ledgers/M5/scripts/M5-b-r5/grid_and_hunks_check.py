"""Round 5, slice M5-b: recompute the L05 Part A distances (to the printed limit 0 and to the true limit f) and the
L07 E2 window bounds, and list the changed hunks of L05.html and L07.html since the round-4 pin 2657ab5.
Run as: <checkout>/.venv/bin/python -I <this file> <checkout>
"""
import subprocess
import sys
from fractions import Fraction
from math import sqrt

root = sys.argv[1]
grid = [Fraction(k, 100) for k in range(101)]


def f_true(x: Fraction) -> Fraction:
    return Fraction(1) if x == 1 else Fraction(0)


for n in (1, 2, 5, 10, 50):
    to_zero = max(x**n for x in grid)
    to_limit = max(abs(x**n - f_true(x)) for x in grid)
    print(f"order {n}: grid sup distance to 0 = {float(to_zero)}; grid sup distance to true limit f = {float(to_limit):.10f}")
print("E2 bounds: f'(5) =", 5 / sqrt(26), " f'(50) =", 50 / sqrt(2501))
for path in ("course/modules/M/M5/L05.html", "course/modules/M/M5/L07.html"):
    out = subprocess.run(["git", "-C", root, "diff", "-U0", "2657ab5", "09b8751", "--", path],
                         capture_output=True, text=True).stdout
    print(path, [line for line in out.splitlines() if line.startswith("@@")])
