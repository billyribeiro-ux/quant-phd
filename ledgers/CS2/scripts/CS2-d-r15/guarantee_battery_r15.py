"""Rank-guarantee battery for a candidate streamstats module (exact Fraction counts, spec Conventions).

Usage: python -I guarantee_battery_r15.py <candidate.py>
For random streams (n up to 300, repeats and sorted runs included) and epsilons 0.05, 0.1, 0.2, 0.3, 0.5, checks at
every q = k/40 and at the ten probes that the answer v satisfies
  #(values < v) <= qn + eps n   and   #(values <= v) >= qn - eps n   (exact rationals of the floats),
and that quantile(q) is nondecreasing in q. Prints the number of checks and the first violation, if any.
"""

import importlib.util
import random
import sys
from fractions import Fraction
from pathlib import Path

path = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("cand", path)
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

rng = random.Random(15)
checks = 0
violations: list[str] = []
grid = [k / 40 for k in range(41)]
for eps in (0.05, 0.1, 0.2, 0.3, 0.5):
    for trial in range(60):
        n = rng.randint(1, 300)
        kind = trial % 3
        if kind == 0:
            stream = [round(rng.gauss(0, 1), rng.choice([1, 6])) for _ in range(n)]
        elif kind == 1:
            stream = sorted(rng.randrange(10) / 4 for _ in range(n))
        else:
            stream = [float(rng.randrange(6)) for _ in range(n)]
        sk = mod.QuantileSketch(eps)
        for x in stream:
            sk.add(x)
        e = Fraction(eps)
        last = None
        for q in sorted(set(grid + [rng.random() for _ in range(10)])):
            v = sk.quantile(q)
            qq = Fraction(q)
            below = sum(1 for y in stream if Fraction(y) < Fraction(v))
            atmost = sum(1 for y in stream if Fraction(y) <= Fraction(v))
            checks += 1
            if not (below <= qq * n + e * n and atmost >= qq * n - e * n):
                violations.append(f"eps={eps} n={n} trial={trial} q={q} v={v}")
            if last is not None and v < last:
                violations.append(f"monotone eps={eps} n={n} trial={trial} q={q}")
            last = v
print(f"{path.name}: checks={checks} violations={len(violations)}")
for v in violations[:5]:
    print("  ", v)
