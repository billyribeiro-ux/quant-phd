"""Randomized exact check of the rank guarantee of Conventions for a sketch file.

Usage: guarantee_battery.py <solution.py> <trials> [seed]
Each trial draws a stream (length 1-60, values with ties, or sorted, or offset floats), an epsilon from
{0.05, 0.1, 0.2, 0.3, 0.5, 0.9}, and checks both inequalities with Fraction counts at a q grid of 0..1 step 1/40 plus
random q, and that quantile(q) is nondecreasing in q. Prints the number of violations (0 expected for a correct sketch).
"""

from __future__ import annotations

import importlib.util
import random
import sys
from fractions import Fraction
from pathlib import Path

spec = importlib.util.spec_from_file_location("sol", Path(sys.argv[1]).resolve())
assert spec and spec.loader
sol = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sol)
trials = int(sys.argv[2])
rng = random.Random(int(sys.argv[3]) if len(sys.argv) > 3 else 1)
EPS = [0.05, 0.1, 0.2, 0.3, 0.5, 0.9]
violations = 0
checks = 0
for t in range(trials):
    n = rng.randint(1, 60)
    kind = rng.randrange(3)
    if kind == 0:
        stream = [float(rng.randint(0, 5)) for _ in range(n)]  # heavy ties
    elif kind == 1:
        stream = sorted(rng.uniform(-5, 5) for _ in range(n))
        if rng.random() < 0.5:
            stream.reverse()
    else:
        stream = [round(1e4 + rng.uniform(-5, 5), 1) for _ in range(n)]
    eps = rng.choice(EPS)
    sk = sol.QuantileSketch(eps)
    for x in stream:
        sk.add(x)
    qs = sorted({k / 40 for k in range(41)} | {rng.random() for _ in range(5)})
    answers = []
    for q in qs:
        v = sk.quantile(q)
        answers.append(v)
        below = sum(1 for x in stream if x < v)
        at_or_below = sum(1 for x in stream if x <= v)
        qn = Fraction(q) * n
        slack = Fraction(eps) * n
        checks += 1
        if not (below <= qn + slack and at_or_below >= qn - slack):
            violations += 1
    if any(a > b for a, b in zip(answers, answers[1:])):
        violations += 1
print(f"{sys.argv[1].split('/')[-1]}: trials {trials}, quantile checks {checks}, violations {violations}")
