# Round-10 check: distance of oracle CE values from the half-cent boundary, seeds 0-49 (instance.py, test oracles).
import json
import math
import sys
from fractions import Fraction

sys.path.insert(0, sys.argv[1])
from instance import make_instance  # noqa: E402


def oracle_value(x, g, lam):
    return math.pow(float(x), 1.0 - g) if x >= 0 else -lam * math.pow(float(-x), 1.0 - g)


def oracle_prospect(prizes, probs, g, lam):
    total = sum(float(p) * oracle_value(x, g, lam) for x, p in zip(prizes, probs, strict=True))
    return math.pow(total, 1.0 / (1.0 - g)) if total >= 0 else -math.pow(-total / lam, 1.0 / (1.0 - g))


def oracle_crra(prizes, probs, g, w):
    finals = [w + x for x in prizes]
    expected = sum(float(p) * math.pow(float(f), 1.0 - g) for p, f in zip(probs, finals, strict=True))
    return math.pow(expected, 1.0 / (1.0 - g)) - w


def dist(c):
    # distance from c to the nearest boundary k + 1/2
    return abs((c - math.floor(c)) - 0.5)


worst_crra = (9.0, None, None)
worst_pro = (9.0, None, None)
for seed in range(50):
    inst = make_instance(seed)
    resp = json.loads(str(inst["responses_json"]))
    wealth = int(inst["wealth_cents"])
    g = float(inst["gamma"])
    lam = float(inst["lambda"])
    for idx, r in enumerate(resp):
        for side in ("a", "b"):
            pr = [int(x) for x in r["prizes_" + side]]
            qs = [Fraction(str(s)) for s in r["probs_" + side]]
            d1 = dist(oracle_crra(pr, qs, g, wealth))
            d2 = dist(oracle_prospect(pr, qs, g, lam))
            if d1 < worst_crra[0]:
                worst_crra = (d1, seed, idx)
            if d2 < worst_pro[0]:
                worst_pro = (d2, seed, idx)
print("min distance (cents) from half-cent boundary, CRRA, all responses seeds 0-49:", worst_crra)
print("min distance (cents) from half-cent boundary, prospect, all responses seeds 0-49:", worst_pro)
