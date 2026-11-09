"""Round-4 re-derivation of the numbers changed or cited on L04 and L06 (exact Fractions and Decimal)."""
from fractions import Fraction as F
from decimal import Decimal, getcontext

getcontext().prec = 80
# L04: p(a) = sqrt(1+a) - 1 at a = 120
a = 120
p = Decimal(121).sqrt() - 1
print("L04 p(120) =", p.quantize(Decimal("1e-30")))
dpda = Decimal(1) / (2 * Decimal(121).sqrt())
print("L04 dp/da - 1/22 =", (dpda - Decimal(1) / 22).quantize(Decimal("1e-60")))
print("L04 (a/p)(dp/da) - 6/11 =", ((Decimal(120) / p) * dpda - Decimal(6) / 11).quantize(Decimal("1e-60")))
print("L04 p''(120) == -1/5324:", F(-1, 5324) == F(-1, 4 * 1331))
print("L04 (1+a)^(3/2)=1331:", 121 ** 3 == 1331 ** 2, " (1+a)^(5/2)=161051:", 11 ** 5 == 161051)
print("L04 p'''(120) = 3/(8*161051) = 3/1288408:", F(3, 8 * 161051) == F(3, 1288408))
# Taylor coefficients: symbolic check by series of sqrt(1+x) around a=0 is not needed; use exact derivatives
def d_p(n, x):  # n-th derivative of sqrt(1+x) at x
    c = F(1, 2)
    val = F(1)
    coeff = F(1)
    for k in range(n):
        coeff *= (c - k)
    return coeff  # placeholder, not used
# Central and forward expansion coefficients (structure only): forward quotient error h/2 p'' ; central error h^2/6 p'''
print("L04 central: (p(a+h)-p(a-h))/(2h) = p' + h^2/6 p''' + O(h^4): coefficient of h^3 in difference is p'''/3 ->", F(1, 3), "per 2h gives", F(1, 6))
# L04 Example 1.3 at p=10, Q=120-2p; p=40
for pr in (10, 40):
    Q = 120 - 2 * pr
    b = 2
    eps = F(-b * pr, Q)
    print("L04 eps at p =", pr, "=", eps)
# L04 Remark 2.5 case
print("L04 dp/da (D=a-p, S=c-3p) = D_a/(S'-D_p) = ", F(1, -3 + 1))

# L06 reference case (a,b,c) = (120,1,20)
a_, b_, c_ = F(120), F(1), F(20)
d = a_ - b_ * c_
print("L06 d =", d)
print("L06 monopoly: vol", d / 2, "fee", (a_ + b_ * c_) / (2 * b_), "profit", d * d / (4 * b_))
print("L06 Cournot: each", d / 3, "total", 2 * d / 3, "fee", (a_ + 2 * b_ * c_) / (3 * b_), "each profit", d * d / (9 * b_), "industry", 2 * d * d / (9 * b_))
print("L06 Cournot each-profit decimal", float(d * d / (9 * b_)), "industry decimal", float(2 * d * d / (9 * b_)))
def half_up(x, places):
    q = Decimal(x.numerator) / Decimal(x.denominator)
    return q.quantize(Decimal(1).scaleb(-places), rounding="ROUND_HALF_UP")
print("L06 rounding: 200/3 ->", half_up(F(200, 3), 2), " 160/3 ->", half_up(F(160, 3), 2), " 20000/9 whole cents ->", half_up(F(20000, 9), 0), " 10000/9 whole cents ->", half_up(F(10000, 9), 0))
print("L06 Bertrand: vol", d, "fee", c_, "profit 0")
print("L06 Prop 4.1 differences: d/6 =", F(d) / 6, "vs", (F(2) * d / 3 - d / 2), "; d/3 =", d / 3, "vs", d - 2 * d / 3)
print("L06 fee diffs:", (a_ + b_ * c_) / (2 * b_) - (a_ + 2 * b_ * c_) / (3 * b_), "=? d/(6b)", d / (6 * b_), "| ", (a_ + 2 * b_ * c_) / (3 * b_) - c_, "=? d/(3b)", d / (3 * b_))
print("L06 profit diff:", d * d / (4 * b_) - 2 * d * d / (9 * b_), "=? d^2/(36b)", d * d / (36 * b_))
# Prop 2.8 error and iteration
x = F(0)
xs = [x]
for t in range(40):
    x = (d - x) / 2 if d - x > 0 else F(0)
    xs.append(x)
ok = all(xs[t] == d / 3 * (1 - F(-1, 2) ** t) for t in range(31))
print("L06 Prop 2.8 closed form matches iteration t=0..30:", ok)
print("L06 error at t=30 (x_30 - d/3) =", xs[30] - d / 3, "; equals -25/805306368:", xs[30] - d / 3 == F(-25, 805306368))
first = next(t for t in range(60) if abs(xs[t] - d / 3) <= F(1, 10**6))
print("L06 first t within 1e-6 (reference) =", first)
for aa, bb, cc in ((90, 3, 10), (200, 4, 5)):
    dd = F(aa) - F(bb) * cc
    xx = F(0); ff = None
    for t in range(60):
        if abs(xx - dd / 3) <= F(1, 10**6):
            ff = t; break
        xx = (dd - xx) / 2 if dd - xx > 0 else F(0)
    print("L06 first t within 1e-6 for", (aa, bb, cc), "=", ff)
# Part C undercut numbers (lab twin output): undercut by 1/1000 at rival fee r, own fee r-1/1000 takes a-b*f
for r in (F(25), F(45), F(70), F(95)):
    f = r - F(1, 1000)
    print("L06 undercut at rival", r, "profit", float((f - c_) * (a_ - b_ * f)), "sharing", float((r - c_) * (a_ - b_ * r) / 2))
