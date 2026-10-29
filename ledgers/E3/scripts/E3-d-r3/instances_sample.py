"""Round-3 check of the autograder instances: 20 seeds (0, 2, 5, ..., 49 spread over 0-49, plus 7919 offsets), each
instance validated against the instance.py docstring; then the spread across seeds. Usage (from the checkout):
.venv/bin/python -I ledgers/E3/scripts/E3-d-r3/instances_sample.py
"""
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "course/modules/E/E3/grader"))
from instance import make_instance  # noqa: E402

seeds = [0, 2, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 117, 3, 26, 44, 7919, 7926]
rows = []
problems = []
for s in seeds:
    inst = make_instance(s)
    recs = json.loads(inst["responses_json"])
    g, l, k, w = inst["gamma"], inst["lambda"], inst["kappa"], inst["wealth_cents"]
    if not (0.10 <= g <= 0.80 and 1.0 <= l <= 3.0 and 0.5 <= k <= 5.0 and 5_000_000 <= w <= 20_000_000):
        problems.append((s, "parameter range"))
    if len(recs) != 200:
        problems.append((s, "pair count"))
    mixed = 0
    for r in recs:
        for side in ("a", "b"):
            pr, pq = r[f"prizes_{side}"], [Fraction(q) for q in r[f"probs_{side}"]]
            if sum(pq) != 1 or any(q < 0 for q in pq) or not (2 <= len(pr) <= 3):
                problems.append((s, r["pair_id"], side, "probability/shape"))
            if any(not (500 <= abs(x) <= 50_000) for x in pr):
                problems.append((s, r["pair_id"], side, "magnitude"))
        if any(x > 0 for x in r["prizes_a"]) and any(x < 0 for x in r["prizes_a"]):
            mixed += 1
    choices = sum(1 for r in recs if r["choice"] == "A")
    rows.append((s, round(g, 3), round(l, 3), round(k, 3), w, mixed, choices))
for row in rows:
    print("seed %5d gamma %.3f lambda %.3f kappa %.3f wealth %d mixedA %d chooseA %d" % row)
print("problems:", problems)
print("distinct gamma values:", len({r[1] for r in rows}), "of", len(rows))
print("distinct wealth values:", len({r[4] for r in rows}))
