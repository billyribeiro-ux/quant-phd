"""Sample seeds 0-19 of the FC1 instance (verifier r4): validity by the page's named conditions, and that the answers differ."""
import sys
from pathlib import Path

GRADER = Path("/Users/billyribeiro/.fanout/wt/verifyD4-FC1-c/course/modules/FC/FC1/grader")
sys.path.insert(0, str(GRADER))
sys.path.insert(1, "/Users/billyribeiro/.fanout/wt/verifyD4-FC1-c/ledgers/FC1/scripts/FC1-c-r4")
from instance import make_instance  # noqa: E402
import importlib.util  # noqa: E402

spec = importlib.util.spec_from_file_location("ref_r4", GRADER / "reference.py")
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)

prices = []
for seed in range(20):
    c = make_instance(seed)
    assert c["face_cents"] >= 1 and c["periods"] >= 1 and c["coupon_bps"] >= 0 and c["yield_bps"] > -10000
    assert c["quantity"] >= 1 and c["price_cents"] >= 0 and c["side"] in (1, -1) and c["settlement_day"] >= 1
    b = ref.Bond(c["face_cents"], c["coupon_bps"], c["periods"])
    p = ref.bond_price_cents(b, c["yield_bps"])
    t = ref.CashTrade(c["quantity"], c["price_cents"], c["side"], c["settlement_day"]).events()
    prices.append((p, t[0][1]))
    print(seed, c["face_cents"], c["coupon_bps"], c["periods"], c["yield_bps"], c["quantity"], c["price_cents"], c["side"], c["settlement_day"], "price", p, "trade", t)
print("distinct (price, trade) answers:", len(set(prices)), "of 20")
print("distinct periods:", len({make_instance(s)["periods"] for s in range(20)}))
