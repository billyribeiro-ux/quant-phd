"""Re-check instance validity on seeds 0-49 and the materiality counts, from the page's rules (stdlib only)."""
import sys
import math
from fractions import Fraction
sys.path.insert(0, sys.argv[1] + "/course/modules/BK/BK4/grader")
from instance import make_instance  # noqa: E402

def margin_answer(case):
    s = sorted(case["losses_cents"])
    return s[math.ceil(Fraction(case["target_bps"] * len(s), 10000)) - 1]

ans, totals, bad = {}, {}, []
for seed in range(50):
    c = make_instance(seed)
    ids = c["member_ids"]
    ok = (ids == list(range(1, len(ids) + 1)) and 4 <= len(ids) <= 6 and c["defaulter_id"] in ids
          and all(f >= 1 for f in c["default_fund_cents"]) and all(m >= 0 for m in c["initial_margin_cents"])
          and c["ccp_capital_cents"] >= 0 and 40 <= len(c["losses_cents"]) <= 80
          and all(isinstance(x, int) and x >= 0 for x in c["losses_cents"]) and c["target_bps"] in (9000, 9500, 9750))
    if not ok:
        bad.append(seed)
    ans[seed] = margin_answer(c)
print("invalid seeds:", bad)
print("distinct margin answers over seeds 0-49:", len(set(ans.values())))
print("seeds whose margin answer differs from seed 0:", sum(1 for s in range(50) if ans[s] != ans[0]))
print("first 20 seeds (seed, N, defaulter, S, target, margin):")
for seed in range(20):
    c = make_instance(seed)
    print(seed, len(c["member_ids"]), c["defaulter_id"], len(c["losses_cents"]), c["target_bps"], ans[seed])
