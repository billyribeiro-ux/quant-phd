"""Round-9 instance check: validity of seeds 0-49 by the page's rules, and how many seeds change the answer."""
import sys, math
from fractions import Fraction
sys.path.insert(0, sys.argv[1] + "/course/modules/BK/BK4/grader")
from instance import make_instance

bad = []
sizing_answers = set()
margin_answers = []
uncovered_totals = set()
for seed in range(50):
    c = make_instance(seed)
    ids = c["member_ids"]; n = len(ids)
    ok = (4 <= n <= 6 and ids == list(range(1, n + 1)) and c["defaulter_id"] in ids
          and all(f >= 1 for f in c["default_fund_cents"]) and all(m >= 0 for m in c["initial_margin_cents"])
          and c["ccp_capital_cents"] >= 0 and 40 <= len(c["losses_cents"]) <= 80
          and all(isinstance(x, int) and x >= 0 for x in c["losses_cents"]) and c["target_bps"] in (9000, 9500, 9750)
          and len(c["default_fund_cents"]) == n and len(c["initial_margin_cents"]) == n)
    d = c["defaulter_id"] - 1
    L = c["losses_cents"]
    inside_margin = any(x <= c["initial_margin_cents"][d] for x in L)
    in_fund = any(c["initial_margin_cents"][d] < x <= c["initial_margin_cents"][d] + c["default_fund_cents"][d] for x in L)
    past = any(x > c["initial_margin_cents"][d] + c["default_fund_cents"][d] + c["ccp_capital_cents"] for x in L)
    if not (ok and inside_margin and in_fund and past):
        bad.append(seed)
    k = math.ceil(Fraction(c["target_bps"] * len(L), 10000))
    m = sorted(L)[k - 1]
    margin_answers.append(m)
    sizing_answers.add(m)
    # uncovered by the reference rule at the page's worst loss
    uncovered_totals.add(max(L) - (c["initial_margin_cents"][d] + c["default_fund_cents"][d] + c["ccp_capital_cents"]))
print("invalid_or_missing_region seeds:", bad)
print("distinct margin answers (own target per seed):", len(sizing_answers))
print("distinct uncovered-at-max-loss values:", len(uncovered_totals))
print("seeds with margin answer distinct from seed 0's:", sum(1 for x in margin_answers if x != margin_answers[0]))
print("targets used:", sorted({make_instance(s)["target_bps"] for s in range(50)}))
print("N values:", sorted({len(make_instance(s)["member_ids"]) for s in range(50)}))
print("scenario counts:", sorted({len(make_instance(s)["losses_cents"]) for s in range(50)})[:3], "...", sorted({len(make_instance(s)["losses_cents"]) for s in range(50)})[-3:])
