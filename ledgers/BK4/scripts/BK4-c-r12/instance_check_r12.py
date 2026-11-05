"""Validity and materiality of grader/instance.py over seeds 0-49 (round 12). Run: python3 -I instance_check_r12.py <checkout>"""

import math
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]) / "course/modules/BK/BK4/grader"))
from instance import make_instance  # noqa: E402

problems = []
margin_answers = set()
uncovered_totals = set()
regions_missing = []
for seed in range(50):
    c = make_instance(seed)
    ids = c["member_ids"]
    im, df = c["initial_margin_cents"], c["default_fund_cents"]
    if ids != list(range(1, len(ids) + 1)) or not 4 <= len(ids) <= 6:
        problems.append((seed, "ids"))
    if any(f < 1 for f in df) or any(m < 0 for m in im) or c["ccp_capital_cents"] < 0:
        problems.append((seed, "amounts"))
    if c["defaulter_id"] not in ids or not 40 <= len(c["losses_cents"]) <= 80:
        problems.append((seed, "defaulter/S"))
    if any(type(x) is not int or x < 0 for x in c["losses_cents"]) or c["target_bps"] not in (9000, 9500, 9750):
        problems.append((seed, "losses/target"))
    d = c["defaulter_id"] - 1
    L = c["losses_cents"]
    if not (any(x <= im[d] for x in L) and any(im[d] < x <= im[d] + df[d] for x in L)
            and any(x > im[d] + df[d] + c["ccp_capital_cents"] for x in L)):
        regions_missing.append(seed)
    S = len(L)
    k = math.ceil(Fraction(c["target_bps"] * S, 10000))
    margin = sorted(L)[k - 1]
    margin_answers.add(margin)
    # uncovered total on the scenarios, one default at a time, by the page's layers
    surv = sum(df) - df[d]
    unc = 0
    for x in L:
        a1 = min(x, im[d])
        a2 = min(x - a1, df[d])
        a3 = min(x - a1 - a2, c["ccp_capital_cents"])
        r = x - a1 - a2 - a3
        unc += max(0, r - surv)
    uncovered_totals.add(unc)
print("problems:", problems)
print("seeds without all three regions:", regions_missing)
print("distinct margin answers over seeds 0-49:", len(margin_answers))
print("distinct uncovered totals over seeds 0-49:", len(uncovered_totals))
