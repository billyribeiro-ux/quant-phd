"""Samples seeds 0-19 of grader/instance.py: validity (page rules) and whether the answers change across seeds.

Usage: python -I instances_seeds_0_19.py <grader dir>
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from instance import make_instance  # noqa: E402


def half_away(x: Fraction) -> int:
    m = abs(x)
    w = (2 * m.numerator + m.denominator) // (2 * m.denominator)
    return w if x >= 0 else -w


rows = []
for seed in range(20):
    c = make_instance(seed)
    assert c["face_cents"] > 0 and c["periods"] >= 1 and c["coupon_bps"] >= 0 and c["yield_bps"] > -10000
    assert c["quantity"] >= 1 and c["price_cents"] >= 0 and c["side"] in (1, -1) and c["settlement_day"] >= 1
    coupon = half_away(Fraction(c["face_cents"] * c["coupon_bps"], 10_000))
    ev = [(t, coupon) for t in range(1, c["periods"] + 1)]
    ev[-1] = (c["periods"], ev[-1][1] + c["face_cents"])
    y = Fraction(c["yield_bps"], 10_000)
    price = half_away(sum((Fraction(a) / (1 + y) ** t for t, a in ev), Fraction(0)))
    trade = -c["side"] * c["quantity"] * c["price_cents"]
    rows.append((seed, c["periods"], c["yield_bps"], price, trade))
    print(seed, "periods", c["periods"], "yield_bps", c["yield_bps"], "price", price, "trade", trade)
print("distinct prices", len({r[3] for r in rows}), "distinct trades", len({r[4] for r in rows}), "of 20")
