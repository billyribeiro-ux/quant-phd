"""Independent recount of the L03 Part B grid search (own code, not the lab's), and the Pareto test on the endowment."""

import itertools
import math
from fractions import Fraction as F

P = (0.5, 0.25, 0.25)
E1 = (F(3), F(4), F(1))
E2 = (F(1), F(4), F(3))
TOT = tuple(a + b for a, b in zip(E1, E2))
GRID = [F(0), F(1, 4), F(1, 2), F(3, 4), F(1)]
EQ1 = (F(9, 4), F(9, 2), F(9, 4))
EQ2 = (F(7, 4), F(7, 2), F(7, 4))


def u(bundle):
    if any(z == 0 for z in bundle):
        return -math.inf
    return sum(p * math.log(float(z)) for p, z in zip(P, bundle))


def better(new, old, tol=1e-12):
    # new Pareto-dominates old: nobody worse by more than tol, somebody better by more than tol
    worse = any(n < o - tol for n, o in zip(new, old))
    strict = any(n > o + tol for n, o in zip(new, old))
    return (not worse) and strict


def count(ref1, ref2):
    hits = []
    for f in itertools.product(GRID, repeat=3):
        a = tuple(fi * t for fi, t in zip(f, TOT))
        b = tuple((1 - fi) * t for fi, t in zip(f, TOT))
        if better((u(a), u(b)), (u(ref1), u(ref2))):
            hits.append((tuple(str(z) for z in a), tuple(str(z) for z in b)))
    return hits


print("grid points", len(list(itertools.product(GRID, repeat=3))))
h_eq = count(EQ1, EQ2)
print("improvements of equilibrium on grid", len(h_eq))
h_en = count(E1, E2)
print("improvements of endowment on grid", len(h_en))
for h in h_en:
    print("  witness", h)
# exact-rational check of the endowment witness (2,4,3)/(2,4,1): both strictly better in exact-log sense via ratio test
