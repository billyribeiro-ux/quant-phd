"""Sample 20 seeds: instances valid, answers change (round 15, slice c). Own oracle, page rules only."""
import importlib.util
import math
from fractions import Fraction
from pathlib import Path

spec = importlib.util.spec_from_file_location("inst", Path("course/modules/BK/BK4/grader/instance.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
rows = []
for seed in range(20):
    c = mod.make_instance(seed)
    ids = c["member_ids"]
    assert ids == list(range(1, len(ids) + 1)) and 4 <= len(ids) <= 6
    assert all(f >= 1 for f in c["default_fund_cents"]) and c["ccp_capital_cents"] >= 0
    assert 40 <= len(c["losses_cents"]) <= 80 and c["target_bps"] in (9000, 9500, 9750)
    assert all(isinstance(x, int) and x >= 0 for x in c["losses_cents"])
    d = c["defaulter_id"] - 1
    m_d, f_d = c["initial_margin_cents"][d], c["default_fund_cents"][d]
    L = c["losses_cents"]
    inside_margin = any(x <= m_d for x in L)
    inside_fund = any(m_d < x <= m_d + f_d for x in L)
    past_all = any(x > m_d + f_d + c["ccp_capital_cents"] for x in L)
    k = math.ceil(Fraction(c["target_bps"] * len(L), 10000))
    margin = sorted(L)[k - 1]
    rows.append((seed, len(ids), c["defaulter_id"], c["target_bps"], len(L), k, margin, inside_margin, inside_fund, past_all))
for r in rows:
    print("seed %2d N=%d defaulter=%d target=%d S=%d k=%d margin=%d | regions: margin %s fund %s past-all %s" % (r + ()))
print("distinct margins over 20 seeds:", len({r[6] for r in rows}), "| distinct (N, defaulter, target):", len({(r[1], r[2], r[3]) for r in rows}))
