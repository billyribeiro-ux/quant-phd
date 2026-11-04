"""Re-derive every hand number quoted in grader/test_project.py docstrings and asserts (FC1-c round 7). Stdlib only."""
from fractions import Fraction as F
import math
import random


def half_away(x):
    m = abs(x)
    whole = math.floor(m + F(1, 2))
    return whole if x >= 0 else -whole


# test_bond_price_exact_half_cent_at_496_bps_is_exact_not_float
coupon_exact = F(1_704_285 * 179, 10_000)
print("496: coupon exact", coupon_exact, float(coupon_exact), "rounded", half_away(coupon_exact))
ev = 1_734_792
pv = F(ev) / (1 + F(496, 10_000))
print("496: pv exact", pv, float(pv), "2*pv", 2 * pv, "is 3305625/2?", pv == F(3305625, 2), "half_away", half_away(pv))
print("496: float discount", ev * (1 + 496 / 10_000) ** -1, "float exact-ish", repr(ev / (1 + 496 / 10_000)))
print("496: test claims 1652812.4999999998 in binary floats; computed:", repr(ev * (1 + 0.0496) ** -1))

# test_bond_price_just_under_a_half_cent_rounds_down
face = 300_075_005
pv3 = sum(F(0) for _ in [])  # placeholder
p = F(face) / (1 + F(1, 10_000)) ** 3
claim = F(299_985_000) + F(1, 2) - F(1, 2 * 1_000_300_030_001)
print("hair: exact", float(p), "claim", float(claim), "equal?", p == claim, "half_away", half_away(p))
print("hair: frac part of exact", p - 299_985_000, "vs 1/2 =", F(1, 2), "gap", F(1, 2) - (p - 299_985_000))

# test_bond_price_exact_half_cent_at_400_bps_uses_the_exact_yield
print("13 at 400:", F(13) / F(104, 100), "float", 13 * (1 + 0.04) ** -1, repr(13 * (1 + 0.04) ** -1), "round", round(13 * (1 + 0.04) ** -1))

# test_trade_cash_flow_is_exact_above_two_to_the_fifty_three
q = 2**40 + 1
print("trade product", q * 9851, "odd", (q * 9851) % 2, "> 2^53", q * 9851 > 2**53)

# fixture numbers quoted in the docstrings
print("rounding fixture terms", float(F(500) / F(104, 100)), float(F(500) / F(104, 100) ** 2), float(F(10500) / F(104, 100) ** 3))
print("fixture 1e17 coupon", F((10**17 + 4999) * 1, 10_000), half_away(F((10**17 + 4999) * 1, 10_000)), 10**13)

# seeds: distinctness of the instance answers for seeds 0..19 (bond price, trade amount, events)
import sys
sys.path.insert(0, "course/modules/FC/FC1/grader")
import importlib.util
spec = importlib.util.spec_from_file_location("instance", "course/modules/FC/FC1/grader/instance.py")
inst = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inst)


def events(face, cbps, n):
    c = half_away(F(face * cbps, 10_000))
    ev = [(t, c) for t in range(1, n + 1)]
    ev[-1] = (n, ev[-1][1] + face)
    return ev


def price(ev, ybps):
    y = F(ybps, 10_000)
    return half_away(sum((F(a) / (1 + y) ** t for t, a in ev), F(0)))


seen = []
for s in range(20):
    c = inst.make_instance(s)
    e = events(c["face_cents"], c["coupon_bps"], c["periods"])
    pr = price(e, c["yield_bps"])
    tr = -c["side"] * c["quantity"] * c["price_cents"]
    seen.append((pr, tr, tuple(e)))
    print("seed", s, "periods", c["periods"], "yield", c["yield_bps"], "price", pr, "trade", (c["settlement_day"], tr), "side", c["side"])
print("distinct (price, trade) pairs over seeds 0-19:", len({(a, b) for a, b, _ in seen}), "of 20")
print("distinct events over seeds 0-19:", len({x for _, _, x in seen}))
