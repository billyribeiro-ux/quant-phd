"""Validity and materiality of grader/instance.py over seeds 0-49, computed with the reference solution (BK4-c r1)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "course" / "modules" / "BK" / "BK4" / "grader"))
sys.path.insert(0, str(ROOT / "course" / "modules" / "BK" / "BK4" / "grader"))
from instance import make_instance  # noqa: E402
import reference as ref  # noqa: E402

problems: list[str] = []
answers: dict[int, int] = {}
uncovered_seeds = 0
distinct_uncovered: set[int] = set()
targets: set[int] = set()
sizes: set[int] = set()
for seed in range(50):
    case = make_instance(seed)
    ids = case["member_ids"]
    n = len(ids)
    sizes.add(n)
    if ids != list(range(1, n + 1)) or not 4 <= n <= 6:
        problems.append(f"seed {seed}: member ids")
    if case["defaulter_id"] not in ids:
        problems.append(f"seed {seed}: defaulter")
    margins = dict(zip(ids, case["initial_margin_cents"], strict=True))
    funds = dict(zip(ids, case["default_fund_cents"], strict=True))
    if any(v < 1 for v in funds.values()) or any(v < 0 for v in margins.values()) or case["ccp_capital_cents"] < 0:
        problems.append(f"seed {seed}: amounts")
    losses = case["losses_cents"]
    if not 40 <= len(losses) <= 80 or any((not isinstance(x, int)) or x < 0 for x in losses):
        problems.append(f"seed {seed}: losses")
    if case["target_bps"] not in (9_000, 9_500, 9_750):
        problems.append(f"seed {seed}: target {case['target_bps']}")
    targets.add(case["target_bps"])
    d = case["defaulter_id"]
    if not any(0 <= x <= margins[d] for x in losses):
        problems.append(f"seed {seed}: no loss inside margin")
    if not any(margins[d] < x <= margins[d] + funds[d] for x in losses):
        problems.append(f"seed {seed}: no loss inside fund")
    if not any(x > margins[d] + funds[d] + case["ccp_capital_cents"] for x in losses):
        problems.append(f"seed {seed}: no loss past capital")
    answer = ref.margin_for_cover(losses, case["target_bps"])
    answers[seed] = answer
    # Uncovered total over the scenarios (the reference waterfall) for this seed.
    total_uncovered = 0
    for loss in losses:
        w = ref.waterfall(loss, d, margins, funds, case["ccp_capital_cents"])
        total_uncovered += w.uncovered_cents
    if total_uncovered > 0:
        uncovered_seeds += 1
    distinct_uncovered.add(total_uncovered)

print(f"validity problems over seeds 0-49: {len(problems)}")
for p in problems[:20]:
    print("  ", p)
print(f"member counts seen: {sorted(sizes)}; targets seen: {sorted(targets)}")
print(f"distinct margin_for_cover answers over seeds 0-49: {len(set(answers.values()))}")
print(f"seeds whose margin differs from seed 0's margin: {sum(1 for s in answers if answers[s] != answers[0])}")
print(f"seeds with a positive total uncovered loss: {uncovered_seeds}; distinct uncovered totals: {len(distinct_uncovered)}")
print(f"seed 0: target {make_instance(0)['target_bps']} margin {answers[0]}")
print(f"seed 0 answer equals 73529: {answers[0] == 73529}")
