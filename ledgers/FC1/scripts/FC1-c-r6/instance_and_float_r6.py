"""Round-6 verifier: (1) validity and variation of seeds 0-19 under the reference; (2) the float claims in test docstrings.
Usage (from the checkout root): python -I ledgers/FC1/scripts/FC1-c-r6/instance_and_float_r6.py"""
import importlib.util
import pathlib

grader = pathlib.Path("course/modules/FC/FC1/grader")
spec = importlib.util.spec_from_file_location("ref", grader / "reference.py")
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)
spec2 = importlib.util.spec_from_file_location("inst", grader / "instance.py")
inst = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(inst)
valid = True
prices, trades = set(), set()
for seed in range(20):
    i = inst.make_instance(seed)
    valid = valid and 100_000 <= i["face_cents"] <= 5_000_000 and 100 <= i["coupon_bps"] <= 900
    valid = valid and 1 <= i["periods"] <= 8 and 50 <= i["yield_bps"] <= 900 and 1 <= i["quantity"] <= 500
    bond = ref.Bond(i["face_cents"], i["coupon_bps"], i["periods"])
    prices.add(ref.bond_price_cents(bond, i["yield_bps"]))
    trades.add(ref.CashTrade(i["quantity"], i["price_cents"], i["side"], i["settlement_day"]).events()[0][1])
print("seeds 0-19 valid:", valid, "| distinct bond prices:", len(prices), "| distinct trade amounts:", len(trades))
print("13 * (1 + 0.04) ** -1 =", repr(13 * (1 + 0.04) ** -1), "(docstring: 12.499999999999998)")
print("1734792 * (1 + 0.0496) ** -1 =", repr(1734792 * (1 + 0.0496) ** -1), "(docstring: 1652812.4999999998)")
print("10**17 + 4999 coupon at 1 bps, exact:", ref.Bond(10**17 + 4999, 1, 1).events())
