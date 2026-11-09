"""Round 17 (BK4 slice c): validity of the instances for seeds 0-49, and how much the answers change across seeds.
Usage: python -I instance_sample_r17.py <checkout-root>"""
import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("instance", ROOT / "course/modules/BK/BK4/grader/instance.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
make_instance = mod.make_instance
bad = []
margins, uncovered_totals, sizing_at_target, kinds = set(), set(), set(), []
for seed in range(50):
    c = make_instance(seed)
    ids = c["member_ids"]
    n = len(ids)
    ok = 4 <= n <= 6 and ids == list(range(1, n + 1)) and c["defaulter_id"] in ids
    ok = ok and all(f >= 1 for f in c["default_fund_cents"]) and all(m >= 0 for m in c["initial_margin_cents"])
    ok = ok and c["ccp_capital_cents"] >= 0 and 40 <= len(c["losses_cents"]) <= 80
    ok = ok and all(isinstance(x, int) and x >= 0 for x in c["losses_cents"]) and c["target_bps"] in (9000, 9500, 9750)
    d = c["defaulter_id"] - 1
    m_d, f_d = c["initial_margin_cents"][d], c["default_fund_cents"][d]
    L = c["losses_cents"]
    ok = ok and any(0 <= x <= m_d for x in L) and any(m_d < x <= m_d + f_d for x in L)
    ok = ok and any(x > m_d + f_d + c["ccp_capital_cents"] for x in L)
    if not ok:
        bad.append(seed)
    S = len(L)
    srt = sorted(L)
    k = -((-c["target_bps"] * S) // 10_000)
    sizing_at_target.add(srt[k - 1])
    # uncovered total over the scenarios, by the page's rules
    pool = sum(c["default_fund_cents"][i] for i in range(n) if i != d)
    tot = 0
    for x in L:
        r = max(0, x - m_d - f_d - c["ccp_capital_cents"])
        tot += max(0, r - pool)
    uncovered_totals.add(tot)
    kinds.append((seed, n, S, c["target_bps"], srt[k - 1], tot))
print("seeds checked: 50; invalid seeds:", bad)
print("distinct sizing margins at each seed's own target:", len(sizing_at_target))
print("distinct total-uncovered values across seeds:", len(uncovered_totals))
print("sample (seed, N, S, target, margin, uncovered_total):")
for row in kinds[:20]:
    print(row)
