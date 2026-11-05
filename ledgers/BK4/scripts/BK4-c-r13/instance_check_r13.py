"""Round-13 BK4-c: independent validity and materiality check of grader/instance.py on seeds 0-49 (and determinism).

Rules are taken from the project page (Inputs, line 200) and from instance.py's docstring, not from the test suite.
Run from the checkout root: python3 -I ledgers/BK4/scripts/BK4-c-r13/instance_check_r13.py
"""

import importlib.util
import os
import sys

ROOT = os.getcwd()
spec = importlib.util.spec_from_file_location("instance", os.path.join(ROOT, "course/modules/BK/BK4/grader/instance.py"))
inst = importlib.util.module_from_spec(spec)
sys.modules["instance"] = inst
spec.loader.exec_module(inst)


def check(seed):
    case = inst.make_instance(seed)
    assert inst.make_instance(seed) == case, f"seed {seed} not deterministic"
    ids = case["member_ids"]
    n = len(ids)
    assert 4 <= n <= 6 and ids == list(range(1, n + 1)), f"seed {seed}: member ids"
    im, df = case["initial_margin_cents"], case["default_fund_cents"]
    assert len(im) == n and len(df) == n, f"seed {seed}: lists not aligned with member ids"
    assert all(isinstance(v, int) and v >= 0 for v in im), f"seed {seed}: margins"
    assert all(isinstance(v, int) and v >= 1 for v in df), f"seed {seed}: default funds >= 1"
    assert isinstance(case["ccp_capital_cents"], int) and case["ccp_capital_cents"] >= 0, f"seed {seed}: capital"
    assert case["defaulter_id"] in ids, f"seed {seed}: defaulter"
    losses = case["losses_cents"]
    assert 40 <= len(losses) <= 80 and all(isinstance(x, int) and x >= 0 for x in losses), f"seed {seed}: losses"
    assert case["target_bps"] in (9000, 9500, 9750), f"seed {seed}: target"
    d = case["defaulter_id"] - 1
    assert any(x <= im[d] for x in losses), f"seed {seed}: no loss inside the margin"
    assert any(im[d] < x <= im[d] + df[d] for x in losses), f"seed {seed}: no loss inside the default fund"
    assert any(x > im[d] + df[d] + case["ccp_capital_cents"] for x in losses), f"seed {seed}: no loss past every layer"
    return case


def margin(case):
    k = -((-case["target_bps"] * len(case["losses_cents"])) // 10_000)
    return sorted(case["losses_cents"])[k - 1]


cases = {s: check(s) for s in range(50)}
margins = {s: margin(c) for s, c in cases.items()}
distinct_margins = len(set(margins.values()))
print("seeds 0-49: all valid; distinct sized margins:", distinct_margins)
print("seeds with a distinct (target, margin) pair:", len({(c["target_bps"], margins[s]) for s, c in cases.items()}))
print("distinct defaulter ids:", sorted({c["defaulter_id"] for c in cases.values()}))
print("distinct member counts:", sorted({len(c["member_ids"]) for c in cases.values()}))
print("distinct targets:", sorted({c["target_bps"] for c in cases.values()}))
print("seed 0 summary:", {k: v for k, v in cases[0].items() if k != "losses_cents"}, "n losses", len(cases[0]["losses_cents"]))
print("seed 0 margin", margins[0], "seed 1 margin", margins[1], "seed 7 margin", margins[7])
uncovered_totals = set()
for s, c in cases.items():
    im, df = c["initial_margin_cents"], c["default_fund_cents"]
    d = c["defaulter_id"] - 1
    pool = sum(df) - df[d]
    unc = 0
    for x in c["losses_cents"]:
        r = x - min(x, im[d]) - min(x - min(x, im[d]), df[d])
        r -= min(r, c["ccp_capital_cents"])
        unc += max(0, r - pool) if r >= 0 else 0
    uncovered_totals.add(unc)
print("distinct total uncovered cents across seeds 0-49 (independent of the suite):", len(uncovered_totals))
print("ALL VALID")
