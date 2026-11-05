"""Round-11: VERIFIER_RULES 2.6 autograder item 2: sample 20 seeds (0, 3, 7, ..., 57 and 30, 49), check every instance is valid
(probabilities exact and summing to 1, prizes whole cents, choices A or B, at least one mixed pair, 200 responses) and that the
instances differ materially (the choices and prizes change, not only the labels)."""
import json
import sys
from fractions import Fraction
from pathlib import Path

work = Path(sys.argv[1])
sys.path.insert(0, str(work))
import test_project as tp  # noqa: E402
from instance import make_instance  # noqa: E402

seeds = [0, 1, 2, 3, 7, 11, 13, 17, 19, 23, 29, 30, 31, 37, 41, 43, 47, 49, 53, 57]
assert len(seeds) == 20
sigs = {}
bad = []
for s in seeds:
    resp = json.loads(str(make_instance(s)["responses_json"]))
    ok = len(resp) == 200
    mixed = 0
    for r in resp:
        pa, qa, pb, qb, ch = tp.parse(r)
        ok &= ch in ("A", "B") and all(isinstance(x, int) for x in pa + pb)
        ok &= sum(qa) == 1 and sum(qb) == 1 and all(p >= 0 for p in qa + qb)
        mixed += tp.mixed(pa, qa) or tp.mixed(pb, qb)
    ok &= mixed >= 1
    if not ok:
        bad.append(s)
    sigs[s] = (tuple(r["choice"] for r in resp[:40]), tuple(sum(r["prizes_a"]) for r in resp[:40]))
    print(f"seed {s}: responses={len(resp)} mixed_questions={mixed} valid={ok}")
distinct = len({v[0] for v in sigs.values()}), len({v[1] for v in sigs.values()})
print("invalid seeds:", bad)
print("distinct choice vectors (first 40 answers):", distinct[0], "of 20; distinct prize sums:", distinct[1], "of 20")
