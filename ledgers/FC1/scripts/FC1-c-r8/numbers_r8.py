"""Round-8 verifier (FC1-c): re-derive every number in project.html, the grader docstrings and cards with exact Fractions."""
from fractions import Fraction as F
from decimal import Decimal, getcontext, ROUND_HALF_UP, ROUND_HALF_EVEN
import math

def half_away(x):
    m = abs(x)
    w = math.floor(m + F(1, 2))
    return w if x >= 0 else -w

def price(events, bps):
    y = F(bps, 10000)
    return sum((F(a) / (1 + y) ** t for t, a in events), F(0))

print("Lab1 exact PV:", float(price([(1, 5000), (2, 5000), (3, 105000)], 400)), "rounded", half_away(price([(1,5000),(2,5000),(3,105000)],400)))
ev = [(1, 500), (2, 500), (3, 10500)]
print("rounding fixture exact PV:", float(price(ev, 400)), "rounded once", half_away(price(ev, 400)))
terms = [F(a) / (F(1) + F(400, 10000)) ** t for t, a in ev]
print("terms:", [float(t) for t in terms], "rounded each", [half_away(t) for t in terms], "sum", sum(half_away(t) for t in terms))
print("Fixture B exact 210000/19 =", float(F(210000, 19)), "half_away", half_away(F(210000, 19)), "exact 10500/0.95 =", float(F(10500) / F(95, 100)))
print("Fixture A 10500/1.05 =", F(10500) / F(105, 100), "price(-500)", half_away(price([(1, 10500)], -500)))
print("Fixture C coupon 10001*5000/10000 =", F(10001 * 5000, 10000), "->", half_away(F(10001*5000, 10000)))
print("Fixture G exact", F(10001, 2), "->", half_away(F(10001, 2)))
print("Fixture F exact", F(1, 2), "->", half_away(F(1, 2)), " python round(0.5)=", round(0.5))

# hand-check: coupon at 496 bps test
face, cb = 1_704_285, 179
coupon_exact = F(face * cb, 10000)
print("496 test coupon exact:", coupon_exact, float(coupon_exact), "rounded", half_away(coupon_exact))
ev496 = [(1, 1_734_792)]
pv496 = price(ev496, 496)
print("496 test exact PV:", pv496, "=", float(pv496), "is 3305625/2:", pv496 == F(3305625, 2), "rounded", half_away(pv496))
print("496 float discount:", (1 + 496/10000) ** -1 * 1734792, repr((1 + 0.0496) ** -1 * 1734792), repr(1734792 * (1 + 0.0496) ** -1))
print("13/1.04 exact:", F(13) / F(104, 100))
print("400 float discount:", repr((1 + 0.04) ** -1 * 13), half_away(F(13) / F(104,100)))
# just-under-half test
pv = price([(1, 0), (2, 0), (3, 300075005)], 1)
print("just-under-half exact:", pv, "float", float(pv), "minus 299985000:", pv - 299985000, "expected 1/2 - 1/(2*1000300030001) =", F(1,2) - F(1, 2 * 1000300030001), "equal:", pv - 299985000 == F(1,2) - F(1, 2 * 1000300030001), "rounded", half_away(pv))
# 10**10+1, 10**12+1
print("10^10+1 half:", half_away(price([(1, 10**10 + 1)], 10000)), " 10^12+1:", half_away(price([(1, 10**12 + 1)], 10000)))
getcontext().prec = 10
print("decimal prec10 of 5000000000.5:", Decimal(5000000000) + Decimal("0.5"), "->", +(Decimal("5000000000.5")), "round half up quantize:", Decimal("5000000000.5").quantize(Decimal(1), rounding=ROUND_HALF_UP))
getcontext().prec = 10
print("prec10 division 10000000001/2:", Decimal(10**10 + 1) / Decimal(2))
print("forty-digit:", half_away(price([(1, 10**40 + 1)], 10000)), 5 * 10**39 + 1, "exact PV", price([(1, 10**40+1)], 10000) == F(10**40 + 1, 2))
print("10^17 fixture coupon:", F(10**17 + 4999, 10000), float(F(10**17+4999, 10000)), "rounded", half_away(F(10**17 + 4999, 10000)), "=10**13:", half_away(F(10**17 + 4999, 10000)) == 10**13)
print("2^40+1 times 9851:", (2**40 + 1) * 9851, " > 2^53:", (2**40+1)*9851 > 2**53, " 2^53=", 2**53)
print("300% yield price:", half_away(price([(1, 10500)], 30000)), "150%:", half_away(price([(1, 10500)], 15000)))
print("par 13..15 periods at 500 bps:", [half_away(price([(t, 500) for t in range(1, n)] + [(n, 500 + 10000)], 500)) for n in (13,14,15)])
print("1 bps just-under price exact:", float(price([(1,0),(2,0),(3,300075005)],1)))
print("trade docstring -side*q*p for 9850*10 buy:", -1*10*9850)
print("1001 bond coupon 500 bps periods 1001 first event:", half_away(F(10000*500, 10000)))
print("A  7/0 check: 1.0001^3:", F(10001, 10000)**3)
