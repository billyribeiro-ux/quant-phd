"""Equivalence check for the dropped mutant 'dual residual without the floor' (round 12, v12_01).

The mutant reports dual = -min(inequality multipliers) with no floor. It differs from the reference only when every
inequality multiplier entry is strictly positive. This script runs the reference on seeds 0-49 and on 400 random small
cases (2 to 5 assets, random bounds, sector caps, turnover limits, including degenerate boxes), and counts the cases
where the minimum entry is positive. The structural argument is in the fragment's row: the working set holds at most
n-1 inequality rows (budget row plus working set is linearly independent in R^n), so the n lower-bound entries contain a zero.

Usage: python -I equiv_v12_01.py <repo_root>
"""

import json
import random
import sys
from fractions import Fraction
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "course/modules/M/M7/grader"))
from instance import make_instance  # noqa: E402
from reference import allocate  # noqa: E402

def entries(m):
    return [*m["lower"], *m["upper"], *m["sector"], *m["turnover_plus"], *m["turnover_minus"], m["turnover_total"]]

cases = [json.loads(make_instance(s)["payload"]) for s in range(50)]
rng = random.Random(12345)
made = 0
while made < 400:
    n = rng.choice((2, 3, 4, 5))
    z = rng.choice((1, 2))
    labels = [i % z for i in range(n)]
    rng.shuffle(labels)
    w0 = [Fraction(1, n)] * n
    w0 = [float(x) for x in w0]
    lower = [rng.choice((-0.2, -0.1, 0.0, w0[0])) for _ in range(n)]
    upper = [max(w0[i], rng.choice((w0[i], 0.5, 1.0))) for i in range(n)]
    if any(lower[i] > upper[i] for i in range(n)):
        continue
    caps = [sum(w0[i] for i in range(n) if labels[i] == k) + rng.choice((0.0, 0.1)) for k in range(z)]
    sigma = [[(1.0 if i == j else 0.0) + 0.1 * rng.random() * (1 if i == j else 0) for j in range(n)] for i in range(n)]
    sigma = [[sigma[i][j] if i == j else 0.0 for j in range(n)] for i in range(n)]
    for i in range(n):
        sigma[i][i] = round(0.01 + 0.05 * rng.random(), 3)
    cases.append({
        "label": "SIMULATED random case for the equivalence check",
        "gamma": rng.choice((0.5, 1.0, 2.0, 5.0)),
        "mu": [round(rng.uniform(-0.02, 0.04), 3) for _ in range(n)],
        "sigma": sigma, "w0": w0, "lower": lower, "upper": upper,
        "sector": labels, "sector_caps": caps, "turnover_limit": rng.choice((0.0, 0.05, 0.2, 0.5)),
    })
    made += 1
ok = positive = refused = 0
for case in cases:
    try:
        out = allocate(case)
    except ValueError:
        refused += 1
        continue
    ok += 1
    if min(entries(out["multipliers"])) > 0:
        positive += 1
print(f"cases answered: {ok}; refused (ValueError, random case invalid): {refused}; answers with every inequality entry > 0: {positive}")
