"""Round-7 check of the floor sentence (project.html line 320): for each seed, the smallest inequality multiplier of the
reference answer, and whether an unfloored dual residual (= minus that smallest multiplier) passes the agreement check
(|reported - recomputed| <= 1e-9, recomputed = floored value = 0 when every multiplier is positive).
Usage: python -I floor_sentence_r7.py <grader_dir>
"""
import json
import sys
from fractions import Fraction

sys.path.insert(0, sys.argv[1])
from instance import make_instance  # noqa: E402
import reference as ref  # noqa: E402

rows = []
for seed in range(50):
    case = json.loads(make_instance(seed)["payload"])
    out = ref.allocate(case)
    m = out["multipliers"]
    ineq = [*m["lower"], *m["upper"], *m["sector"], *m["turnover_plus"], *m["turnover_minus"], m["turnover_total"]]
    smallest = min(ineq)
    unfloored = -smallest
    floored = max(0.0, unfloored)
    passes = abs(unfloored - floored) <= 1e-9
    rows.append((seed, smallest, passes))
print("seeds with every inequality multiplier > 0:", [(s, m) for s, m, _ in rows if m > 0])
print("seeds whose smallest multiplier is in (0, 1e-9]:", [(s, m) for s, m, _ in rows if 0 < m <= 1e-9])
print("min over seeds of smallest multiplier:", min(m for _, m, _ in rows))
print("unfloored-report agreement pass count:", sum(p for _, _, p in rows), "of", len(rows))
