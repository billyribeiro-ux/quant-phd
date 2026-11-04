"""Validity and materiality of the grader's instances, seeds 0-49 (all) and 20 sampled seeds in detail.

Usage: python -I sample_instances_r5.py <grader dir>. Standard library only; imports instance.py from the grader dir.
"""

from __future__ import annotations

import math
import random
import sys
from fractions import Fraction

sys.path.insert(0, sys.argv[1])
from instance import make_instance  # noqa: E402

problems: list[str] = []
answers: dict[int, int] = {}
uncovered_at: dict[int, int] = {}
for seed in range(50):
    c = make_instance(seed)
    ids = c["member_ids"]
    n = len(ids)
    if ids != list(range(1, n + 1)) or not 4 <= n <= 6:
        problems.append(f"seed {seed}: member ids")
    if c["defaulter_id"] not in ids:
        problems.append(f"seed {seed}: defaulter not a member")
    if any(f < 1 for f in c["default_fund_cents"]) or any(m < 0 for m in c["initial_margin_cents"]):
        problems.append(f"seed {seed}: fund or margin")
    if c["ccp_capital_cents"] < 0 or not 40 <= len(c["losses_cents"]) <= 80:
        problems.append(f"seed {seed}: capital or S")
    if not all(type(x) is int and x >= 0 for x in c["losses_cents"]):
        problems.append(f"seed {seed}: loss type")
    if c["target_bps"] not in (9000, 9500, 9750):
        problems.append(f"seed {seed}: target")
    losses = c["losses_cents"]
    k = math.ceil(Fraction(c["target_bps"] * len(losses), 10000))
    answers[seed] = sorted(losses)[k - 1]
    d = c["defaulter_id"] - 1
    margin_d, fund_d = c["initial_margin_cents"][d], c["default_fund_cents"][d]
    # uncovered total over all scenarios of the case (page rules), a second answer that must vary across seeds
    total_uncovered = 0
    pool = sum(f for i, f in enumerate(c["default_fund_cents"]) if i != d)
    for loss in losses:
        r = max(0, loss - margin_d - fund_d - c["ccp_capital_cents"])
        total_uncovered += max(0, r - pool)
    uncovered_at[seed] = total_uncovered
    if not (margin_d // 2 == losses[0] and losses[1] > margin_d and losses[2] > margin_d + fund_d + c["ccp_capital_cents"]):
        problems.append(f"seed {seed}: the three designed scenarios are not in place")

print("problems:", problems if problems else "none")
print("distinct sizing answers over seeds 0-49:", len(set(answers.values())))
print("seeds whose sizing answer differs from seed 0:", sum(1 for s in range(50) if answers[s] != answers[0]))
print("distinct total-uncovered values over seeds 0-49:", len(set(uncovered_at.values())))
print("seeds with a nonzero total uncovered:", sum(1 for s in range(50) if uncovered_at[s] > 0))
rng = random.Random(20260311)
sample = sorted(rng.sample(range(50), 20))
print("sampled seeds:", sample)
for s in sample:
    c = make_instance(s)
    print(f"seed {s}: N={len(c['member_ids'])} D={c['defaulter_id']} S={len(c['losses_cents'])} target={c['target_bps']} margin_answer={answers[s]} uncovered_total={uncovered_at[s]}")
