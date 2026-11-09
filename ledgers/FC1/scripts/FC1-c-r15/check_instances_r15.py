"""Round 15, FC1-c: sample instances, distinct answers, and starter-versus-reference signatures (run with python -I).

Usage: python -I check_instances_r15.py <checkout>
"""

import importlib.util
import inspect
import sys

checkout = sys.argv[1]
grader = f"{checkout}/course/modules/FC/FC1/grader"


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


inst = load("instance", f"{grader}/instance.py")
ref = load("reference", f"{grader}/reference.py")
starter = load("starter", f"{grader}/starter.py")

ranges = {
    "face_cents": (100_000, 5_000_000), "coupon_bps": (100, 900), "periods": (1, 8), "yield_bps": (50, 900),
    "quantity": (1, 500), "price_cents": (5_000, 150_000), "settlement_day": (1, 5),
}
answers = []
bad = []
for seed in range(50):
    c = inst.make_instance(seed)
    for k, (lo, hi) in ranges.items():
        if not (lo <= c[k] <= hi):
            bad.append((seed, k, c[k]))
    if c["side"] not in (1, -1):
        bad.append((seed, "side", c["side"]))
    bond = ref.Bond(c["face_cents"], c["coupon_bps"], c["periods"])
    price = ref.bond_price_cents(bond, c["yield_bps"])
    trade = ref.CashTrade(c["quantity"], c["price_cents"], c["side"], c["settlement_day"]).events()
    answers.append((seed, price, tuple(bond.events()), tuple(trade)))
print("range violations (seeds 0-49):", bad)
print("distinct bond prices over seeds 0-49:", len({a[1] for a in answers}))
print("distinct bond event lists over seeds 0-49:", len({a[2] for a in answers}))
print("distinct trade events over seeds 0-49:", len({a[3] for a in answers}))
print("distinct full answer tuples over seeds 0-49:", len({a[1:] for a in answers}))
print("sample seeds 0-19 prices:", [a[1] for a in answers[:20]])
for seed in range(20):
    c = inst.make_instance(seed)
    assert set(c) == {"seed", "label", "face_cents", "coupon_bps", "periods", "yield_bps", "quantity", "price_cents", "side", "settlement_day"}, seed
print("instance keys: ok for seeds 0-19; label contains SIMULATED:", "SIMULATED" in inst.make_instance(0)["label"])

names = ["Bond", "bond_price_cents", "CashTrade"]
for name in names:
    rs, ss = getattr(ref, name), getattr(starter, name)
    if inspect.isclass(rs):
        for meth in (["__init__"] + [m for m in ("events",) if hasattr(rs, m)]):
            print(name, meth, "ref", inspect.signature(getattr(rs, meth)), "starter", inspect.signature(getattr(ss, meth)))
    else:
        print(name, "ref", inspect.signature(rs), "starter", inspect.signature(ss))
