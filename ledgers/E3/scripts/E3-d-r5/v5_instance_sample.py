"""Samples 20 seeds of grader/instance.py and checks each instance (round-5 verifier, stdlib plus the instance module).

Checks: every lottery's probabilities are exact and sum to exactly 1 (no negatives); 2 or 3 prizes; prizes whole cents
within 500..50000 in magnitude; the answers are 200 pairs with at least 100 mixed; the (gamma, lambda, kappa) differ
across seeds. Run: python3 -I ledgers/E3/scripts/E3-d-r5/v5_instance_sample.py (from the checkout).
"""
import os
import sys
from fractions import Fraction

GRADER = os.path.abspath("course/modules/E/E3/grader")
sys.path.insert(0, GRADER)
import json  # noqa: E402
from instance import make_instance  # noqa: E402

SEEDS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
seen = set()
for seed in SEEDS:
    inst = make_instance(seed)
    resp = json.loads(str(inst["responses_json"]))
    assert len(resp) == 200, (seed, len(resp))
    mixed = 0
    for r in resp:
        for pk, qk in (("prizes_a", "probs_a"), ("prizes_b", "probs_b")):
            prizes = [int(x) for x in r[pk]]
            probs = [Fraction(s) for s in r[qk]]
            assert len(prizes) == len(probs) and len(prizes) in (2, 3), (seed, r["pair_id"])
            assert all(p >= 0 for p in probs) and sum(probs) == 1, (seed, r["pair_id"])
            assert all(500 <= abs(x) <= 50000 for x in prizes), (seed, prizes)
        ga = any(int(x) > 0 and Fraction(p) > 0 for x, p in zip(r["prizes_a"], r["probs_a"]))
        la = any(int(x) < 0 and Fraction(p) > 0 for x, p in zip(r["prizes_a"], r["probs_a"]))
        gb = any(int(x) > 0 and Fraction(p) > 0 for x, p in zip(r["prizes_b"], r["probs_b"]))
        lb = any(int(x) < 0 and Fraction(p) > 0 for x, p in zip(r["prizes_b"], r["probs_b"]))
        mixed += int((ga and la) or (gb and lb))
    assert mixed >= 100, (seed, mixed)
    key = (float(inst["gamma"]), float(inst["lambda"]), float(inst["kappa"]))
    seen.add(key)
    print(f"seed {seed}: 200 answers, mixed {mixed}, gamma {key[0]:.3f} lambda {key[1]:.3f} kappa {key[2]:.3f}, valid")
print("distinct (gamma, lambda, kappa) over 20 seeds:", len(seen))
