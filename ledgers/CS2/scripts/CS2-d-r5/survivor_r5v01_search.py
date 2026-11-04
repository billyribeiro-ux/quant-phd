"""Round-5 check: does mutant r5v_01 (fold the maximum tuple into its predecessor) break the rank guarantee?

Loads a module from a path given as argv[1], then for short integer streams (values 0..k-1 in every order class
that matters: sorted, reversed, and a seeded shuffle), epsilon in {0.05, 0.1, 0.2}, and probes q in a dense grid
plus 0 and 1, checks the two rank inequalities of the page with exact Fractions. Prints the first violations.
"""

from __future__ import annotations

import importlib.util
import random
import sys
from fractions import Fraction

spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

PROBES = [Fraction(i, 100) for i in range(101)]
violations: list[str] = []
checked = 0
for eps_text in ("0.05", "0.1", "0.2"):
    eps = Fraction(eps_text)
    for n in range(1, 13):
        streams = [list(range(n)), list(range(n))[::-1]]
        for seed in range(200):
            vals = list(range(n))
            random.Random(seed).shuffle(vals)
            streams.append(vals)
        for stream in streams:
            sk = mod.QuantileSketch(float(eps))
            for x in stream:
                sk.add(float(x))
            for q in PROBES:
                v = sk.quantile(float(q))
                checked += 1
                strictly_below = sum(1 for y in stream if y < v)
                at_or_below = sum(1 for y in stream if y <= v)
                target_hi = q * n + eps * n
                target_lo = q * n - eps * n
                if not (strictly_below <= target_hi and at_or_below >= target_lo):
                    violations.append(f"eps={eps_text} n={n} stream={stream} q={float(q)} answer={v}")
print("checked", checked, "violations", len(violations))
for line in violations[:8]:
    print("VIOLATION", line)
