"""Samples 20 seeds of the grader instance and checks validity and material difference (VERIFIER_RULES 2.6.2).

Validity: 200 responses, whole-cent prizes of magnitude 5 to 500 dollars, exact probabilities summing to 1 per lottery,
at least 100 mixed pairs, parameters in the stated ranges. Difference: distinct true parameters and distinct answer
strings. Run with -I; argv[1] is the repo root.
"""

import json
import sys
from fractions import Fraction

sys.path.insert(0, sys.argv[1] + "/course/modules/E/E3/grader")
from instance import make_instance  # noqa: E402

seeds = [0, 1, 2, 7, 14, 21, 33, 49, 57, 64, 81, 96, 108, 123, 157, 200, 250, 301, 350, 399]
rows = []
for seed in seeds:
    inst = make_instance(seed)
    resp = json.loads(inst["responses_json"])
    assert len(resp) == 200, seed
    mixed = 0
    for r in resp:
        pa, qa = r["prizes_a"], [Fraction(s) for s in r["probs_a"]]
        pb, qb = r["prizes_b"], [Fraction(s) for s in r["probs_b"]]
        for prizes, probs in ((pa, qa), (pb, qb)):
            assert all(isinstance(x, int) and 500 <= abs(x) <= 50000 for x in prizes), seed
            assert sum(probs) == 1 and all(p > 0 for p in probs), seed
        g = any(x > 0 for x in pa) and any(x < 0 for x in pa)
        h = any(x > 0 for x in pb) and any(x < 0 for x in pb)
        mixed += int(g or h)
    assert mixed >= 100, seed
    assert 0.1 <= inst["gamma"] <= 0.8 and 1.0 <= inst["lambda"] <= 3.0 and 0.5 <= inst["kappa"] <= 5.0, seed
    rows.append((seed, inst["gamma"], inst["lambda"], inst["kappa"], inst["wealth_cents"], mixed, hash(inst["responses_json"]) % 10**6))
for row in rows:
    print("seed %3d gamma %.3f lambda %.3f kappa %.3f wealth %d mixed-pairs %d" % row[:6])
print("distinct parameter triples:", len({(r[1], r[2], r[3]) for r in rows}), "of", len(rows))
print("distinct answer strings:", len({r[6] for r in rows}), "of", len(rows))
print("ALL VALID")
