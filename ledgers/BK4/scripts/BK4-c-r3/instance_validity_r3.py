"""Plan 5.5 instance validity and materiality over seeds 0-49, using the grader's make_instance (read-only import)."""
import sys
from math import ceil
from fractions import Fraction
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyE3-BK4-c/course/modules/BK/BK4/grader")
from instance import make_instance

problems = []
answers = {}
differs_from_seed0 = 0
uncovered_total = {}
for seed in range(50):
    c = make_instance(seed)
    ids = c["member_ids"]; d = c["defaulter_id"]; n = len(ids)
    if ids != list(range(1, n + 1)) or not 4 <= n <= 6: problems.append((seed, "ids"))
    if d not in ids: problems.append((seed, "defaulter"))
    if any(f < 1 for f in c["default_fund_cents"]): problems.append((seed, "DF<1"))
    if any(m < 0 for m in c["initial_margin_cents"]) or c["ccp_capital_cents"] < 0: problems.append((seed, "neg"))
    L = c["losses_cents"]
    if not 40 <= len(L) <= 80 or any((not isinstance(x, int)) or x < 0 for x in L): problems.append((seed, "losses"))
    if c["target_bps"] not in (9000, 9500, 9750): problems.append((seed, "target"))
    m = c["initial_margin_cents"][d - 1]; f = c["default_fund_cents"][d - 1]
    if not any(0 <= x <= m for x in L): problems.append((seed, "no margin-region loss"))
    if not any(m < x <= m + f for x in L): problems.append((seed, "no fund-region loss"))
    if not any(x > m + f + c["ccp_capital_cents"] for x in L): problems.append((seed, "no survivor-region loss"))
    k = ceil(Fraction(c["target_bps"] * len(L), 10000))
    answers[seed] = sorted(L)[k - 1]
print("validity problems over seeds 0-49:", problems)
print("distinct sizing answers over seeds 0-49:", len(set(answers.values())))
print("seeds whose sizing answer differs from seed 0:", sum(1 for s in answers if answers[s] != answers[0]))
print("sizing answers seeds 0-9:", [answers[s] for s in range(10)])
