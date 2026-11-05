"""Independent instance check for grader/instance.py (round 8). Uses only the page's rules; no grader import of reference.

Reports, for seeds 0-49: validity of every instance, the three separated regions, the sizing answer by an independent
oracle (Fraction ceiling), the uncovered total over the scenarios, and distinct counts. Sampled seeds (20, fixed by
random.Random(20261104)) are printed in full.
"""

from __future__ import annotations

import pathlib
import random
import sys
from fractions import Fraction
import math

GRADER = pathlib.Path(sys.argv[1]) / "course/modules/BK/BK4/grader"
sys.path.insert(0, str(GRADER))
from instance import make_instance  # noqa: E402  (path inserted above)


def waterfall(loss, d, margins, funds, cap):
    m = min(loss, margins[d])
    f = min(loss - m, funds[d])
    c = min(loss - m - f, cap)
    r = loss - m - f - c
    surv = sorted(x for x in funds if x != d)
    pool = sum(funds[x] for x in surv)
    if r >= pool:
        return m, f, c, {x: funds[x] for x in surv}, r - pool
    sh = {x: r * funds[x] // pool for x in surv}
    left = r - sum(sh.values())
    for x in surv:
        if left > 0 and funds[x] > 0:
            sh[x] += 1
            left -= 1
    assert left == 0
    return m, f, c, sh, 0


def check_valid(case):
    ids = case["member_ids"]
    n = len(ids)
    problems = []
    if not 4 <= n <= 6 or ids != list(range(1, n + 1)):
        problems.append("ids")
    if len(case["initial_margin_cents"]) != n or len(case["default_fund_cents"]) != n:
        problems.append("lengths")
    if any(not isinstance(x, int) or x < 0 for x in case["initial_margin_cents"]):
        problems.append("IM")
    if any(not isinstance(x, int) or x < 1 for x in case["default_fund_cents"]):
        problems.append("DF>=1")
    if not isinstance(case["ccp_capital_cents"], int) or case["ccp_capital_cents"] < 0:
        problems.append("K")
    if case["defaulter_id"] not in ids:
        problems.append("defaulter")
    if not 40 <= len(case["losses_cents"]) <= 80 or any(not isinstance(x, int) or x < 0 for x in case["losses_cents"]):
        problems.append("losses")
    if case["target_bps"] not in (9000, 9500, 9750):
        problems.append("target")
    return problems


def regions(case):
    ids = case["member_ids"]
    margins = dict(zip(ids, case["initial_margin_cents"]))
    funds = dict(zip(ids, case["default_fund_cents"]))
    d = case["defaulter_id"]
    L = case["losses_cents"]
    K = case["ccp_capital_cents"]
    inside_margin = 0 <= L[0] <= margins[d]
    in_fund = margins[d] < L[1] <= margins[d] + funds[d]
    past_all = L[2] > margins[d] + funds[d] + K
    return inside_margin, in_fund, past_all, margins, funds


def oracle_margin(losses, target):
    k = math.ceil(Fraction(target * len(losses), 10_000))
    return sorted(losses)[k - 1]


rows = []
for seed in range(50):
    case = make_instance(seed)
    probs = check_valid(case)
    im, inf, pa, margins, funds = regions(case)
    d = case["defaulter_id"]
    L = case["losses_cents"]
    unc_total = sum(waterfall(x, d, margins, funds, case["ccp_capital_cents"])[4] for x in L)
    m = oracle_margin(L, case["target_bps"])
    # conservation on every scenario
    for x in L:
        a1, a2, a3, sh, u = waterfall(x, d, margins, funds, case["ccp_capital_cents"])
        assert a1 + a2 + a3 + sum(sh.values()) + u == x, (seed, x)
    rows.append((seed, probs, im, inf, pa, m, unc_total, case["target_bps"], len(L), len(case["member_ids"]), d))

bad = [(r[0], r[1]) for r in rows if r[1] or not (r[2] and r[3] and r[4])]
print("seeds checked: 50; invalid or region-missing seeds:", bad if bad else "none")
margin_answers = {r[5] for r in rows}
print("distinct sizing answers across seeds 0-49:", len(margin_answers))
print("seeds with a margin answer different from seed 0's:", sum(1 for r in rows if r[5] != rows[0][5]))
print("distinct uncovered totals across seeds 0-49:", len({r[6] for r in rows}))
print("seeds with nonzero uncovered total:", sum(1 for r in rows if r[6] > 0))
print("targets used:", sorted({r[7] for r in rows}))
print("N values:", sorted({r[9] for r in rows}), " S values range:", min(r[8] for r in rows), max(r[8] for r in rows))
sample = random.Random(20261104).sample(range(50), 20)
print("sampled seeds (20):", sorted(sample))
for r in rows:
    if r[0] in sample:
        print("seed", r[0], "| N", r[9], "| defaulter", r[10], "| S", r[8], "| target", r[7], "| margin answer", r[5], "| uncovered total", r[6], "| invalid", r[1], "| regions", r[2], r[3], r[4])
