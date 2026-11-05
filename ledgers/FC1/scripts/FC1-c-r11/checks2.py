from fractions import Fraction as F
import math
def half_away(x):
    m = abs(x); w = math.floor(m + F(1, 2)); return w if x >= 0 else -w
# 1704285 bond at 496 bps
coupon = half_away(F(1704285 * 179, 10000)); ev = coupon + 1704285
print("coupon exact", F(1704285*179,10000), float(F(1704285*179,10000)), "rounded", coupon, "event", ev)
pv = F(ev) / (1 + F(496, 10000))
print("pv exact", pv, "=3305625/2?", pv == F(3305625, 2), "half_away", half_away(pv), "float", repr(ev / (1 + 496/10000)), repr(ev * (1 + 0.0496) ** -1))
# 13 at 400 bps
pv13 = F(13) / (1 + F(400, 10000)); print("13/1.04", pv13, "half_away", half_away(pv13), "float", repr((1 + 0.04) ** -1 * 13), round((1+0.04)**-1*13))
# 300075005 at 1 bps, 3 periods
pvz = F(300075005) / (1 + F(1, 10000)) ** 3
claim = 299985000 + F(1, 2) - F(1, 2 * 1000300030001)
print("hair pv", pvz, float(pvz), "claim equal?", pvz == claim, "half_away", half_away(pvz), "frac part", pvz - 299985000)
# face 10**17+4999 at 1 bps
print("big coupon", F((10**17+4999) * 1, 10000), half_away(F((10**17+4999) * 1, 10000)), 10**13)
# 10**9 face
print("10^9 coupon", 10**9*500//10000)
# Lab/docstring check: 10500/101, 10500/1001, 10500/21
print(float(F(10500,101)), half_away(F(10500,101)), half_away(F(10500,1001)), F(10500,21))
# fixture: rounding case term parts
for t,a in [(1,500),(2,500),(3,10500)]:
    print("term", t, float(F(a)/F(104,100)**t))
print("2^53", 2**53, "2^40+1 * 9851", (2**40+1)*9851, (2**40+1)*9851 > 2**53)
print("1e17 check", 10**17+4999 > 2**53)
