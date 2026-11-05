"""Recompute the central-difference error ratio for sin at x0 of both instances of seeds 0-49 (page claim 3.9999842-3.9999851)."""
import math
import sys
sys.path.insert(0, sys.argv[1])  # the grader directory (instance.py)
from instance import make_instance
from decimal import Decimal, getcontext
getcontext().prec = 50

def central(x0: float, h: float) -> float:
    return (math.sin(x0 + h) - math.sin(x0 - h)) / (2 * h)

lo, hi = float("inf"), float("-inf")
rows = []
for seed in range(50):
    for s in (seed, seed + 7_919):
        inst = make_instance(s)
        x0 = inst["x0"]
        exact = math.cos(x0)
        r = abs(central(x0, 1e-2) - exact) / abs(central(x0, 5e-3) - exact)
        lo, hi = min(lo, r), max(hi, r)
        rows.append((seed, s, x0, r))
print("n instances", len(rows))
print("min ratio %.10f max ratio %.10f" % (lo, hi))
print("rounded 7dp min %.7f max %.7f" % (round(lo, 7), round(hi, 7)))
for row in rows[:4]:
    print("seed %d inst_seed %d x0 %.2f ratio %.10f" % row)
