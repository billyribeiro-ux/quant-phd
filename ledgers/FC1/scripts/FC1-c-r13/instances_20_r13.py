"""Round-13: sample 20 seeds (0, 2, ..., 38), check each instance is valid for the reference engine and that the answers differ."""
import sys
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "course/modules/FC/FC1/grader"))
import importlib.util  # noqa: E402

spec = importlib.util.spec_from_file_location("ref13", root / "course/modules/FC/FC1/grader/reference.py")
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)  # type: ignore[union-attr]
from instance import make_instance  # noqa: E402

rows = []
for seed in range(0, 40, 2):
    inst = make_instance(seed)
    b = ref.Bond(inst["face_cents"], inst["coupon_bps"], inst["periods"])
    price = ref.bond_price_cents(b, inst["yield_bps"])
    t = inst
    trade_ev = ref.CashTrade(t["quantity"], t["price_cents"], t["side"], t["settlement_day"]).events()
    rows.append((seed, inst["face_cents"], inst["coupon_bps"], inst["periods"], inst["yield_bps"], price, trade_ev))
for r in rows:
    print(r)
print("distinct prices", len({r[5] for r in rows}), "of", len(rows))
print("distinct trade events", len({str(r[6]) for r in rows}), "of", len(rows))
print("keys", sorted(make_instance(0).keys()))
