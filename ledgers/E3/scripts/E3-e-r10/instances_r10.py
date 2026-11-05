"""Round-10: sample 20 seeds (0-19) of the grader instance generator; check validity and that the answers differ."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course" / "modules" / "E" / "E3" / "grader"
sys.path.insert(0, str(GRADER))
from instance import make_instance  # noqa: E402

from fractions import Fraction  # noqa: E402

rows = []
for seed in range(0, 20):
    inst = make_instance(seed)
    resp = json.loads(str(inst["responses_json"]))
    ok = len(resp) >= 12 and all(
        sum(Fraction(p) for p in r["probs_a"]) == 1 and sum(Fraction(p) for p in r["probs_b"]) == 1 for r in resp
    )
    choices = "".join(r["choice"] for r in resp)
    rows.append((seed, ok, len(resp), choices, round(float(inst["gamma"]), 4), round(float(inst["lambda"]), 4), round(float(inst["kappa"]), 4)))
for row in rows:
    print("seed=%d valid=%s pairs=%d choices=%s gamma=%s lambda=%s kappa=%s" % row)
print("distinct choice strings:", len({r[3] for r in rows}), "of", len(rows))
print("distinct (gamma,lambda,kappa):", len({(r[4], r[5], r[6]) for r in rows}), "of", len(rows))
print("all valid:", all(r[1] for r in rows))
