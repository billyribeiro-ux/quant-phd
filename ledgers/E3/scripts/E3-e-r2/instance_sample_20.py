"""Sample 20 seeds of the E3 instance generator: validity and material difference (verifier E3-e round 2).

Usage: python -I ledgers/E3/scripts/E3-e-r2/instance_sample_20.py   (run from the checkout root)
"""

import hashlib
import importlib.util
import json
from fractions import Fraction

spec = importlib.util.spec_from_file_location("instance_mod", "course/modules/E/E3/grader/instance.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

rows = []
for seed in range(0, 50, 2):
    inst = mod.make_instance(seed)
    recs = json.loads(inst["responses_json"])
    assert len(recs) == 200, seed
    for r in recs:
        for side in ("a", "b"):
            probs = [Fraction(s) for s in r[f"probs_{side}"]]
            assert all(p > 0 for p in probs) and sum(probs) == 1, (seed, r["pair_id"])
            assert all(isinstance(x, int) and 500 <= abs(x) <= 50_000 for x in r[f"prizes_{side}"]), seed
    mixed = sum(
        any(x > 0 for x in r["prizes_a"]) and any(x < 0 for x in r["prizes_a"])
        or any(x > 0 for x in r["prizes_b"]) and any(x < 0 for x in r["prizes_b"])
        for r in recs
    )
    a_share = sum(r["choice"] == "A" for r in recs) / len(recs)
    digest = hashlib.sha256(inst["responses_json"].encode()).hexdigest()[:12]
    rows.append((seed, inst["gamma"], inst["lambda"], inst["kappa"], inst["wealth_cents"], mixed, round(a_share, 3), digest))
for row in rows:
    print("seed %2d gamma %.3f lambda %.3f kappa %.3f wealth %d mixed(sign test) %d A-share %.3f sha %s" % row)
print("distinct answer digests:", len({r[-1] for r in rows}), "of", len(rows))
print("distinct (gamma, lambda, kappa):", len({r[1:4] for r in rows}), "of", len(rows))
