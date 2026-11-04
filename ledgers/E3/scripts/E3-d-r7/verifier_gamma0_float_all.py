import sys, json, math
from fractions import Fraction
sys.path.insert(0, "/Users/billyribeiro/.fanout/scratch-E3-d-r7/work")
from instance import make_instance
bad_seeds = []
total_div = 0
for seed in range(0, 50):
    inst = make_instance(seed)
    resp = json.loads(inst["responses_json"])
    seed_div = 0
    # the test checks PARSED[:40]: the first 40 responses, lotteries A and B
    for r in resp[:40]:
        for side in ("a", "b"):
            pr = [int(x) for x in r["prizes_" + side]]
            pq = [Fraction(s) for s in r["probs_" + side]]
            ex = sum((p * x for p, x in zip(pq, pr)), Fraction(0))
            fl = sum(float(p) * x for p, x in zip(pq, pr))
            if math.floor(ex + Fraction(1, 2)) != math.floor(fl + 0.5):
                seed_div += 1
    total_div += seed_div
    if seed_div:
        bad_seeds.append((seed, seed_div))
print("seeds with a float-vs-exact divergence in PARSED[:40] (gamma=0 check):", len(bad_seeds), "of 50")
print("first divergent seeds:", bad_seeds[:12])
print("total divergent lotteries:", total_div)
