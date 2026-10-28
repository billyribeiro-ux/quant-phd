# Search for a float-computed rank target that differs from the exact one (page claim, project.html Exact counts item).
import math
from fractions import Fraction
probes = [0.5, 0.25, 0.75, 0.1, 0.9, 0.3, 0.7, 0.05, 0.95, 0.6]
found = []
for eps in (0.05, 0.1, 0.2):
    for n in range(1, 401):
        for q in probes:
            exact = max(1, math.ceil(Fraction(q) * n - Fraction(eps) * n))
            flt = max(1, math.ceil(q * n - eps * n))
            if exact != flt:
                found.append((eps, n, q, exact, flt))
print(len(found), found[:5])
