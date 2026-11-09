"""Round-14 independent check of L03 prose numbers and the lab's printed CE values (decimal, 50 digits)."""
from decimal import Decimal, getcontext
from fractions import Fraction
getcontext().prec = 50
X = [(5000, Fraction(1, 4)), (10000, Fraction(1, 2)), (20000, Fraction(1, 4))]
def ce(g):
    s = 1 - Decimal(str(g))
    if Decimal(str(g)) == 1:
        m = sum(Decimal(p.numerator) / p.denominator * Decimal(x).ln() for x, p in X)
        return m.exp()
    M = sum(Decimal(p.numerator) / p.denominator * Decimal(x) ** s for x, p in X)
    return M ** (1 / s)
for g in ("0", "0.25", "0.5", "1", "2", "4"):
    v = ce(g)
    print("gamma", g, "CE", v.quantize(Decimal("0.0001")), "rounded_half_up", (v + Decimal("0.5")).to_integral_value(rounding="ROUND_FLOOR"))
print("gamma 2 exact", Fraction(1, 1) / sum(p / x for x, p in X), float(Fraction(80000, 9)))
print("Example 2.5 gamma2", Fraction(1, 1) / (Fraction(1, 2) * Fraction(1, 1000) + Fraction(1, 2) * Fraction(1, 4000)))
print("Example 2.5 gamma1", (Decimal(1000).ln() / 2 + Decimal(4000).ln() / 2).exp())
print("E1 rounding 10615.8009 -> 10616 check", Decimal("10615.8009") + Decimal("0.5"))
print("M1 mech 1/8 check: -u''/u' at 4 for u_{1/2}:", Fraction(1, 2) * Fraction(1, 4) / Fraction(1, 2) * Fraction(1, 1) / 1)
