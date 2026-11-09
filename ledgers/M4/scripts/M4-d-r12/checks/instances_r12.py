"""Verifier round 12: validity of make_instance over seeds 0-199 (grader/instance.py docstring claims)."""
import math
import sys
from pathlib import Path
sys.path.insert(0, "course/modules/M/M4/grader")
import instance  # noqa: E402

DRAWS = {6003, 8001, 9997, 12011, 15013, 19987}
bad = []
tuples = set()
for s in range(200):
    d = instance.make_instance(s)
    p, c, nu, n = d["positions_cents"], d["cov"], d["nu"], d["n_draws"]
    k = d["n_assets"]
    if not (k in (2, 3) and len(p) == k):
        bad.append((s, "n_assets"))
    if not all(type(x) is int and 100_000 <= x <= 5_000_000 for x in p):
        bad.append((s, "positions"))
    if not all(c[i][j] == c[j][i] for i in range(k) for j in range(k)):
        bad.append((s, "symmetry"))
    if not (3 <= nu <= 8):
        bad.append((s, "nu"))
    if n not in DRAWS or n % 100 == 0 or n > 19987:
        bad.append((s, "draws"))
    if d["label"] != "SIMULATED":
        bad.append((s, "label"))
    # positive definiteness by an exact pivot check (Fraction of the float entries)
    from fractions import Fraction
    a = [[Fraction(c[i][j]) for j in range(k)] for i in range(k)]
    dd = []
    L = [[Fraction(0)] * k for _ in range(k)]
    ok = True
    for j in range(k):
        dj = a[j][j] - sum(L[j][m] * L[j][m] * dd[m] for m in range(j))
        dd.append(dj)
        if not dj > 0:
            ok = False
            break
        for i in range(j + 1, k):
            L[i][j] = (a[i][j] - sum(L[i][m] * L[j][m] * dd[m] for m in range(j))) / dj
    if not ok:
        bad.append((s, "not PD"))
    tuples.add((tuple(p), tuple(map(tuple, c)), nu, n))
print("seeds 0-199: violations", bad)
print("distinct instances", len(tuples))
# draw-set coverage
from collections import Counter
print("nu counts", sorted(Counter(instance.make_instance(s)["nu"] for s in range(200)).items()))
print("n_draws counts", sorted(Counter(instance.make_instance(s)["n_draws"] for s in range(200)).items()))
print("n_assets counts", sorted(Counter(instance.make_instance(s)["n_assets"] for s in range(200)).items()))
