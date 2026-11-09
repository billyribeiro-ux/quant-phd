"""Sample seeds 0-19 of grader/instance.py: validity ranges and the answers (price, settlement event) per seed."""
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyD12-FC1-c/course/modules/FC/FC1/grader")
from instance import make_instance  # noqa: E402


def half_away(x):
    m = abs(x)
    w = (2 * m.numerator + m.denominator) // (2 * m.denominator)
    return w if x >= 0 else -w


rows = []
for seed in range(20):
    c = make_instance(seed)
    assert 100_000 <= c["face_cents"] <= 5_000_000 and 100 <= c["coupon_bps"] <= 900 and 1 <= c["periods"] <= 8
    assert 50 <= c["yield_bps"] <= 900 and 1 <= c["quantity"] <= 500 and 5_000 <= c["price_cents"] <= 150_000
    assert c["side"] in (1, -1) and 1 <= c["settlement_day"] <= 5
    cpn = half_away(F(c["face_cents"] * c["coupon_bps"], 10_000))
    ev = [(t, cpn) for t in range(1, c["periods"] + 1)]
    ev[-1] = (c["periods"], ev[-1][1] + c["face_cents"])
    y = F(c["yield_bps"], 10_000)
    price = half_away(sum((F(a) / (1 + y) ** t for t, a in ev), F(0)))
    trade = (c["settlement_day"], -c["side"] * c["quantity"] * c["price_cents"])
    rows.append((seed, c["periods"], price, trade))
    print(f"seed {seed:2d} periods {c['periods']} price {price:>9d} trade {trade}")
print("distinct prices:", len({r[2] for r in rows}), "of", len(rows), "; distinct trades:", len({r[3] for r in rows}))
