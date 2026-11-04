# ruff: noqa: E501
"""Round-5 check: the rank guarantee of Conventions for epsilon values beyond the instance set {0.05, 0.1, 0.2}.

argv[1] is a streamstats-style module path. Streams: sorted, reversed and 200 seeded shuffles of 0..n-1 for n in 1..12
(plus the 2-value streams in both orders). Probes: q = i/100 for i in 0..100. Epsilons: 0.01 to 0.99 in steps of 0.01 and
the boundary values 0.000001 and 0.999999. The two inequalities are checked with exact Fractions.
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

EPS = [Fraction(i, 100) for i in range(1, 100)] + [Fraction(1, 1000000), Fraction(999999, 1000000)]
PROBES = [Fraction(i, 100) for i in range(101)]
violations: list[str] = []
checked = 0
for eps in EPS:
    for n in range(1, 13):
        streams = [list(range(n)), list(range(n))[::-1]]
        streams += [random.Random(seed).sample(range(n), n) for seed in range(200)]
        for stream in streams:
            sk = mod.QuantileSketch(float(eps))
            for x in stream:
                sk.add(float(x))
            for q in PROBES:
                v = sk.quantile(float(q))
                checked += 1
                strictly_below = sum(1 for y in stream if y < v)
                at_or_below = sum(1 for y in stream if y <= v)
                if not (strictly_below <= q * n + eps * n and at_or_below >= q * n - eps * n):
                    violations.append(f"eps={float(eps)} n={n} stream={stream} q={float(q)} answer={v}")
print("checked", checked, "violations", len(violations))
for line in violations[:6]:
    print("VIOLATION", line)
