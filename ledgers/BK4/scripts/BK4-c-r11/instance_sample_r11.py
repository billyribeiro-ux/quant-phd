"""Round-10: sample 20 seeds of the BK4 instance; check validity against the project page, and that answers differ.

Usage: python instance_sample_r10.py <repo_root>   (run with -I from the checkout)
"""

import importlib.util
import sys
from pathlib import Path
from fractions import Fraction
from math import ceil

root = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("inst", root / "course/modules/BK/BK4/grader/instance.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

bad = []
margins, losses_t, caps, ns, defaulters = set(), set(), set(), set(), set()
for seed in range(20):
    c = mod.make_instance(seed)
    n = len(c["member_ids"])
    if c["member_ids"] != list(range(1, n + 1)) or not 4 <= n <= 6:
        bad.append((seed, "member ids"))
    if not all(isinstance(x, int) and x >= 1 for x in c["default_fund_cents"]):
        bad.append((seed, "fund < 1 cent"))
    if not all(isinstance(x, int) and x >= 0 for x in c["initial_margin_cents"]):
        bad.append((seed, "margin"))
    if not (isinstance(c["ccp_capital_cents"], int) and c["ccp_capital_cents"] >= 0):
        bad.append((seed, "capital"))
    if c["defaulter_id"] not in c["member_ids"]:
        bad.append((seed, "defaulter"))
    if not 40 <= len(c["losses_cents"]) <= 80:
        bad.append((seed, "scenario count"))
    if c["target_bps"] not in (9000, 9500, 9750):
        bad.append((seed, "target"))
    d = c["defaulter_id"] - 1
    im, fd = c["initial_margin_cents"][d], c["default_fund_cents"][d]
    L = c["losses_cents"]
    if not (0 <= L[0] <= im and im < L[1] <= im + fd and L[2] > im + fd + c["ccp_capital_cents"]):
        bad.append((seed, "three regions"))
    k = ceil(Fraction(c["target_bps"] * len(L), 10_000))
    margins.add(sorted(L)[k - 1])
    losses_t.add(tuple(L))
    caps.add(c["ccp_capital_cents"])
    ns.add(len(L))
    defaulters.add(c["defaulter_id"])
    print(f"seed {seed:2d}: N={n} defaulter={c['defaulter_id']} S={len(L)} target={c['target_bps']} "
          f"margin_for_target={sorted(L)[k-1]} capital={c['ccp_capital_cents']}")
print("invalid:", bad)
print(f"distinct sizing margins over 20 seeds: {len(margins)}; distinct loss sets: {len(losses_t)}; "
      f"distinct capitals: {len(caps)}; distinct S: {len(ns)}; distinct defaulters: {len(defaulters)}")
print("INSTANCES PASS" if not bad and len(margins) >= 3 else "INSTANCES FAIL")
