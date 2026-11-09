"""Round 14, FC1-c: validity and distinctness of the seeded instances (grader/instance.py), seeds 0-49.

Usage: python -I ledgers/FC1/scripts/FC1-c-r14/check_instances_r14.py
Checks, for every seed: every field is in the documented range; the reference bond price and trade event are
computed by an independent Fraction oracle; then counts distinct answers across seeds 0-49 and prints the answers for
seeds 0-19 (the 20 sampled seeds the verifier rules ask for are seeds 0-19 here).
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "course/modules/FC/FC1/grader"))
from instance import make_instance  # noqa: E402


def half_away(x: Fraction) -> int:
    m = abs(x)
    w = math.floor(m + Fraction(1, 2))
    return w if x >= 0 else -w


rows = []
problems = []
for seed in range(50):
    c = make_instance(seed)
    ok = (
        100_000 <= c["face_cents"] <= 5_000_000
        and 100 <= c["coupon_bps"] <= 900
        and 1 <= c["periods"] <= 8
        and 50 <= c["yield_bps"] <= 900
        and 1 <= c["quantity"] <= 500
        and 5_000 <= c["price_cents"] <= 150_000
        and c["side"] in (1, -1)
        and 1 <= c["settlement_day"] <= 5
    )
    if not ok:
        problems.append((seed, "range"))
    coupon = half_away(Fraction(c["face_cents"] * c["coupon_bps"], 10_000))
    events = [(t, coupon) for t in range(1, c["periods"] + 1)]
    events[-1] = (c["periods"], events[-1][1] + c["face_cents"])
    y = Fraction(c["yield_bps"], 10_000)
    price = half_away(sum((Fraction(a) / (1 + y) ** t for t, a in events), Fraction(0)))
    trade = (c["settlement_day"], -c["side"] * c["quantity"] * c["price_cents"])
    rows.append((seed, price, trade, c["periods"], c["yield_bps"], c["face_cents"]))

answers = {(p, tr) for _, p, tr, *_ in rows}
prices = {p for _, p, *_ in rows}
print(f"seeds 0-49: range problems={problems or 'none'}")
print(f"distinct (bond price, trade event) pairs over 50 seeds: {len(answers)}; distinct bond prices: {len(prices)}")
print(f"distinct periods: {sorted({r[3] for r in rows})}; distinct yields: {len({r[4] for r in rows})}")
for seed, price, trade, periods, yb, face in rows[:20]:
    print(f"seed {seed:2d}: face {face} periods {periods} yield_bps {yb} price {price} trade {trade}")
