"""Verifier FC1-c round 9: re-derive every number in project.html, test docstrings and cards with exact Fractions."""
from fractions import Fraction as F
from decimal import Decimal, getcontext
import math

def half_away(x):
    m = abs(x)
    w = math.floor(m + F(1, 2))
    return w if x >= 0 else -w

def events(face, cbps, n):
    c = half_away(F(face * cbps, 10000))
    rows = [(t, c) for t in range(1, n + 1)]
    rows[-1] = (n, c + face)
    return rows

def price(ev, ybps):
    y = F(ybps, 10000)
    return sum((F(a) / (1 + y) ** t for t, a in ev), F(0))

print("L1 events", events(100000, 500, 3))
pv = price(events(100000, 500, 3), 400)
print("L1 exact PV", pv, float(pv), f"{float(pv):.6f}", half_away(pv))
print("L1 trade", (2, -10 * 9850))
print("Lab3 A events", events(10000, 500, 1), "price", half_away(price(events(10000, 500, 1), 500)))
print("Lab3 B exact 10500/0.95", F(10500) / F(95, 100), float(F(10500)/F(95,100)), "price", half_away(price(events(10000,500,1), -500)))
print("Lab3 C", events(10001, 5000, 2))
print("Lab3 D", events(1, 5000, 1))
rc = events(10000, 500, 3)
print("rounding events", rc, "exact", price(rc, 400), float(price(rc, 400)), "once", half_away(price(rc, 400)))
print("rounding termwise", sum(half_away(F(a) / (1 + F(400, 10000)) ** t) for t, a in rc), [half_away(F(a) / (1 + F(400,10000)) ** t) for t, a in rc], [float(F(a) / (1 + F(400,10000)) ** t) for t, a in rc])
print("Lab3 E", (2, -10 * 9850))
print("Lab3 F", events(1, 0, 1), half_away(price(events(1, 0, 1), 10000)), price(events(1,0,1),10000))
print("Lab3 G", events(10001, 0, 1), half_away(price(events(10001, 0, 1), 10000)), price(events(10001,0,1),10000))
print("fixture A price 10500/1.05", F(10500)/F(105,100))
print("hours-lab-tests 10500/21", F(10500)/21, "10500/2.5", F(10500)/F(5,2), "10500/4", F(10500)/4)
print("test 15000 bps: 10500/2.5", half_away(F(10500)/F(5,2)))
print("test 30000 bps", half_away(F(10000+0)/1))
# test_bond_price_exact_half_cent_at_496
ev = events(1704285, 179, 1)
print("496 bps events", ev, "coupon exact", F(1704285*179, 10000), float(F(1704285*179,10000)))
ex = price(ev, 496)
print("496 exact", ex, ex == F(3305625, 2), half_away(ex))
v = 1734792.0 / 1.0496
print("496 float naive", repr(v), "float discount", repr(1734792 * (1 + 496/10000) ** -1))
# 13 at 400
print("13/1.04 exact", F(13)/F(104,100), "float", repr((1 + 0.04) ** -1 * 13), round((1 + 0.04) ** -1 * 13))
print("float 13 at 400", repr(13 / 1.04))
# 300075005 at 1 bps, 3 periods
ex3 = F(300075005) / (1 + F(1, 10000)) ** 3
claim = 299985000 + F(1, 2) - F(1, 2 * 1000300030001)
print("just-under claim", ex3 == claim, float(ex3), ex3 - 299985000, half_away(ex3))
print("(1.0001)^3", (1 + F(1,10000))**3, "denominator 1000300030001 check", (F(10001,10000))**3 == F(1000300030001, 10**12))
# 10**10+1 and 10**12+1
print("10**10+1", half_away(price(events(10**10+1, 0, 1)[:0] or [(1, 10**10+1)], 10000)), price([(1,10**10+1)],10000))
print("10**12+1", half_away(price([(1,10**12+1)],10000)), price([(1,10**12+1)],10000))
print("prec10 Decimal", Decimal(5000000000.5) if False else '')
getcontext().prec = 10
d = (Decimal(10**10 + 1) / Decimal(2))
print("decimal prec10 of 5000000000.5 ->", d, "rounds to", d.to_integral_value())
d40 = F(10**40 + 1, 2)
print("40 digit exact", d40, half_away(d40) == 5 * 10**39 + 1)
print("10**17+4999 coupon", F((10**17 + 4999) * 1, 10000), half_away(F((10**17+4999)*1, 10000)) == 10**13)
print("10**9 coupon", half_away(F(10**9 * 500, 10000)))
print("2**40+1 * 9851 > 2**53", (2**40+1)*9851 > 2**53, 2**53)
print("fixture C", half_away(F(10001*5000, 10000)))
print("fixture 1000 periods exact", "n/a")
print("Bond(10000,500,1) at 15000", half_away(price([(1, 10500)], 15000)))
print("1+y at 200000 -> 21; 10500/21", price([(1,10500)], 200000), half_away(price([(1,10500)], 200000)))
print("1+y at 30000 -> 4; 10500/4", price([(1,10500)], 30000))
print("par 500 bps periods 13..15", [half_away(price(events(10000,500,n), 500)) for n in (13,14,15)])
