"""Materiality over seeds 0-49 (plan 5.5): distinct margins, distinct uncovered totals (round 15, slice c)."""
import importlib.util
import math
from fractions import Fraction
from pathlib import Path

spec = importlib.util.spec_from_file_location("inst", Path("course/modules/BK/BK4/grader/instance.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
own, fixed9500, uncovered_totals, fixed_margin_seeds = [], [], [], 0
for seed in range(50):
    c = mod.make_instance(seed)
    L = sorted(c["losses_cents"])
    S = len(L)
    k = math.ceil(Fraction(c["target_bps"] * S, 10000))
    own.append(L[k - 1])
    k5 = math.ceil(Fraction(9500 * S, 10000))
    fixed9500.append(L[k5 - 1])
    d = c["defaulter_id"]
    ids = c["member_ids"]
    margins = dict(zip(ids, c["initial_margin_cents"]))
    funds = dict(zip(ids, c["default_fund_cents"]))
    unc = 0
    for x in c["losses_cents"]:
        a1 = min(x, margins[d]); a2 = min(x - a1, funds[d]); a3 = min(x - a1 - a2, c["ccp_capital_cents"])
        r = x - a1 - a2 - a3
        pool = sum(funds[m] for m in ids if m != d)
        unc += max(0, r - pool)
    uncovered_totals.append(unc)
print("distinct margin at each seed's own target, seeds 0-49:", len(set(own)))
print("distinct margin at fixed 9500 bps, seeds 0-49:", len(set(fixed9500)))
print("distinct total uncovered loss, seeds 0-49:", len(set(uncovered_totals)), "| seeds with uncovered > 0:", sum(1 for u in uncovered_totals if u > 0))
