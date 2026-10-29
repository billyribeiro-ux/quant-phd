import sys, json, math
sys.path.insert(0, "/tmp/verifyC2-E3-d/course/modules/E/E3/grader")
import reference as R
from instance import make_instance
from fractions import Fraction
worst_c = (9, None); worst_p = (9, None)
for seed in range(50):
    inst = make_instance(seed); W = int(inst["wealth_cents"]); g=float(inst["gamma"]); l=float(inst["lambda"])
    resp = json.loads(inst["responses_json"])
    for r in resp[:40]:
        pa=[int(x) for x in r["prizes_a"]]; qa=[Fraction(s) for s in r["probs_a"]]
        pb=[int(x) for x in r["prizes_b"]]; qb=[Fraction(s) for s in r["probs_b"]]
        for prizes, probs in ((pa,qa),(pb,qb)):
            c = R._crra_change(prizes, probs, g, W) if True else 0
            d = abs(c - math.floor(c) - 0.5)
            if d < worst_c[0]: worst_c = (d, (seed, round(c, 6)))
            p = R._prospect_ce(prizes, probs, g, l)
            d2 = abs(p - math.floor(p) - 0.5)
            if d2 < worst_p[0]: worst_p = (d2, (seed, round(p, 6)))
print("closest CRRA CE to a half-cent boundary (distance, (seed, value)):", worst_c)
print("closest prospect CE to a half-cent boundary:", worst_p)
