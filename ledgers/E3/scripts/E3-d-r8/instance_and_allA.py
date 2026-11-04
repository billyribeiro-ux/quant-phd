# (a) instance.py docstring claims over seeds 0-49 and seed 30; (b) the all-A set quoted in test_estimate_counts_... (choice precision near 925, SE above 1e5).
import sys, json, math
from fractions import Fraction
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyD8-E3-d/course/modules/E/E3/grader")
import instance, reference
from instance import make_instance
bad = []
for seed in list(range(50)) + [30]:
    inst = make_instance(seed)
    g, l, k, w = inst["gamma"], inst["lambda"], inst["kappa"], inst["wealth_cents"]
    if not (0.10 <= g <= 0.80 and 1.0 <= l <= 3.0 and 0.5 <= k <= 5.0 and 5_000_000 <= w <= 20_000_000 and w % 100 == 0):
        bad.append((seed, "param range"))
    recs = json.loads(inst["responses_json"])
    if len(recs) != 200:
        bad.append((seed, "pairs", len(recs)))
    mixed = 0
    for r in recs:
        mixed_any = False
        for side in ("a", "b"):
            pr = [int(x) for x in r[f"prizes_{side}"]]
            pq = [Fraction(s) for s in r[f"probs_{side}"]]
            if not (2 <= len(pr) <= 3 and len(pr) == len(pq)):
                bad.append((seed, "prize count"))
            if any(not (500 <= abs(x) <= 50000) for x in pr):
                bad.append((seed, "magnitude"))
            if sum(pq) != 1 or any(p <= 0 for p in pq):
                bad.append((seed, "probs"))
            if any(p.denominator not in (1, 2, 4, 5, 10, 20) for p in pq):
                bad.append((seed, "denominator"))
            mixed_any = mixed_any or ((any(x > 0 for x in pr) and any(x < 0 for x in pr)))
        mixed += mixed_any
    if mixed < 100:
        bad.append((seed, "mixed<100", mixed))
print("instance checks over seeds 0-49 and 30: problems =", bad[:10], "count", len(bad))
print("seed 30 kappa", make_instance(30)["kappa"])
# (b) all-A set from test_estimate_counts_a_mixed_lottery_whether_or_not_it_was_chosen
B_SIDE_SURE_A = [700, 1900, 0, 2600, -300, 1500, 900, 2100, -600, 1100, 400, 1800]
B_SIDE_LOTTERIES = [([2000, -1500], ["1/2", "1/2"]), ([3000, -2500], ["2/5", "3/5"]), ([1500, -1000], ["3/4", "1/4"]), ([4000, -3000], ["1/3", "2/3"]), ([2500, -4000], ["1/2", "1/2"]), ([1000, -500], ["4/5", "1/5"]), ([3500, -2000], ["1/4", "3/4"]), ([800, -1200], ["1/2", "1/2"]), ([5000, -3000], ["3/10", "7/10"]), ([2200, -2800], ["3/5", "2/5"]), ([1200, -600], ["1/2", "1/2"]), ([4500, -5000], ["2/3", "1/3"])]
responses = [{"pair_id": i, "choice": "A", "prizes_a": [B_SIDE_SURE_A[i]], "probs_a": ["1"], "prizes_b": B_SIDE_LOTTERIES[i][0], "probs_b": B_SIDE_LOTTERIES[i][1]} for i in range(12)]
try:
    r = reference.estimate(responses)
    print("all-A estimate:", r)
except Exception as e:
    print("all-A estimate raised:", type(e).__name__, e)
