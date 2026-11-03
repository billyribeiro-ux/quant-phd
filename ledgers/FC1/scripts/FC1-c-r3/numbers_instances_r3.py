"""Round-3 independent checks (verifier D3, FC1-c). Read-only. Usage: numbers_instances_r3.py <checkout root>."""
import importlib.util
import sys
from fractions import Fraction as F
from pathlib import Path

root = Path(sys.argv[1])
grader = root / "course/modules/FC/FC1/grader"
spec = importlib.util.spec_from_file_location("instance", grader / "instance.py")
inst = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inst)
spec2 = importlib.util.spec_from_file_location("ref", grader / "reference.py")
ref = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(ref)


def half(x):
    m = abs(x)
    w = (2 * m.numerator + m.denominator) // (2 * m.denominator)
    return w if x >= 0 else -w


def events(face, c, n):
    coupon = half(F(face * c, 10000))
    rows = [(t, coupon) for t in range(1, n + 1)]
    rows[-1] = (n, coupon + face)
    return rows


def price(ev, bps):
    y = F(bps, 10000)
    return half(sum((F(a) / (1 + y) ** t for t, a in ev), F(0)))


print("== instances seeds 0-19 (page valid-input rules)")
prices, flows = set(), set()
for s in range(20):
    c = inst.make_instance(s)
    ok = (c["periods"] >= 1 and c["face_cents"] > 0 and c["coupon_bps"] >= 0 and c["yield_bps"] > -10000
          and c["quantity"] >= 1 and c["price_cents"] >= 0 and c["side"] in (1, -1) and c["settlement_day"] >= 1)
    p = ref.bond_price_cents(ref.Bond(c["face_cents"], c["coupon_bps"], c["periods"]), c["yield_bps"])
    f = ref.CashTrade(c["quantity"], c["price_cents"], c["side"], c["settlement_day"]).events()[0][1]
    prices.add(p)
    flows.add(f)
    assert ok, s
print("valid on all 20 seeds; distinct bond prices:", len(prices), "distinct trade flows:", len(flows))

print("== Lab 1 numbers")
ev1 = events(100000, 500, 3)
exact1 = sum((F(a) / F(104, 100) ** t for t, a in ev1), F(0))
print("events", ev1, "exact PV", float(exact1), repr(float(exact1)), "price", half(exact1))
print("trade", (2, -10 * 9850))

print("== fixtures A-G and rounding case (page lines 186-193)")
print("A events", events(10000, 500, 1), "price@500", price(events(10000, 500, 1), 500))
exactB = F(10500) / F(95, 100)
print("B price@-500", price(events(10000, 500, 1), -500), "exact", float(exactB), "210000/19", F(210000, 19) == exactB)
print("C events", events(10001, 5000, 2))
print("D events", events(1, 5000, 1))
r = events(10000, 500, 3)
print("rounding events", r, "exact", float(sum((F(a) / F(104, 100) ** t for t, a in r), F(0))), "rounded", price(r, 400))
print("rounding per-term", sum(half(F(a) / F(104, 100) ** t) for t, a in r))
print("E", (2, -10 * 9850), "seller", (2, 10 * 9850))
print("F events", events(1, 0, 1), "price@10000", price(events(1, 0, 1), 10000), "exact", F(1, 2))
print("G events", events(10001, 0, 1), "price@10000", price(events(10001, 0, 1), 10000), "exact", F(10001, 2))

print("== round-2 suspected float claims (test docstrings)")
print("13*(1+0.04)**-1 =", repr(13 * (1 + 0.04) ** -1), "13/(1+0.04) =", repr(13 / (1 + 0.04)))
print("1734792/1.0496 float =", repr(1734792 / 1.0496), "exact", F(1734792) / F(10496, 10000))
print("coupon 1704285*179/10000 =", float(F(1704285 * 179, 10000)), "rounded", half(F(1704285 * 179, 10000)))

print("== docstring claim: dropped later coupons at 500 bps")
n, cpn, face = 13, 500, 10000
print("par n=13 at 500:", float(sum((F(a) / F(105, 100) ** t for t, a in events(face, cpn, n)), F(0))))
drop = [(1, cpn), (n, cpn + face)]
print("keep 1 and face at 13 (later coupons dropped) at 500:", float(sum((F(a) / F(105, 100) ** t for t, a in drop), F(0))))
short = events(face, cpn, 12)
print("schedule stopping at 12 (face at 12) at 500:", float(sum((F(a) / F(105, 100) ** t for t, a in short), F(0))))

print("== fixture for the r3 survivors")
print("Bond(10**12+1, 0, 1) at 10000 ->", ref.bond_price_cents(ref.Bond(10**12 + 1, 0, 1), 10000), "(exact half, expected 500000000001)")
print("Bond(10000, 500, 24) at 400 ->", ref.bond_price_cents(ref.Bond(10000, 500, 24), 400), "oracle", price(events(10000, 500, 24), 400))
