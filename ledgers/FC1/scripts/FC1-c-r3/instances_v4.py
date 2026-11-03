"""Sample seeds 0-19 of grader/instance.py: validity against the page's ranges, and whether the answers change across seeds."""
import sys
from pathlib import Path

grader = Path(sys.argv[1])
sys.path.insert(0, str(grader))
from fractions import Fraction  # noqa: E402

import instance  # noqa: E402
import reference  # noqa: E402

rows = []
for seed in range(20):
    c = instance.make_instance(seed)
    b = reference.Bond(c["face_cents"], c["coupon_bps"], c["periods"])
    price = reference.bond_price_cents(b, c["yield_bps"])
    trade = reference.CashTrade(c["quantity"], c["price_cents"], c["side"], c["settlement_day"]).events()
    valid = (
        isinstance(c["face_cents"], int) and c["face_cents"] >= 1 and 1 <= c["periods"]
        and 0 <= c["coupon_bps"] and 1 <= c["quantity"] and c["price_cents"] >= 0 and c["side"] in (1, -1)
        and c["settlement_day"] >= 1 and c["yield_bps"] > -10000
    )
    rows.append((seed, c["face_cents"], c["coupon_bps"], c["periods"], c["yield_bps"], price, trade[0][1], valid))
    print(seed, c["face_cents"], c["coupon_bps"], c["periods"], c["yield_bps"], "price", price, "trade", trade, "valid", valid)
print("all valid:", all(r[-1] for r in rows))
print("distinct prices:", len({r[5] for r in rows}), "distinct trade cash flows:", len({r[6] for r in rows}))
print("distinct (periods) values:", sorted({r[3] for r in rows}))
