"""Independent re-derivation of every number in L04 prose and in the L04 lab (own code, mpmath-free, Decimal 60 digits)."""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60
D = Decimal


def p_of(a: Decimal) -> Decimal:
    # positive root of a - 2p = p^2  ->  p = sqrt(1 + a) - 1
    return (1 + a).sqrt() - 1


a0 = D(120)
p0 = p_of(a0)
dp = 1 / (2 * (1 + a0).sqrt())
print("p*(120) =", p0, " dp/da =", dp, " 1/22 diff =", abs(dp - D(1) / D(22)))

# Example 2.4
print("dQ/da =", D(20) * dp, " 10/11 diff =", abs(D(20) * dp - D(10) / D(11)))
print("1 - 2/22 =", D(1) - D(2) / D(22))
print("Prop 2.3 formula D_a/(S'-D_p) =", D(1) / (D(20) + 2))

# Lab Part B
print("elasticity (a/p)dp =", a0 / p0 * dp, " 6/11 =", D(6) / D(11))

# Lab Part C
errs_f = {}
errs_c = {}
for h in [D(1), D("0.1"), D("0.01"), D("0.001")]:
    fwd = (p_of(a0 + h) - p0) / h
    cen = (p_of(a0 + h) - p_of(a0 - h)) / (2 * h)
    errs_f[h] = abs(fwd - dp)
    errs_c[h] = abs(cen - dp)
    print("h", h, "fwd", fwd, "fwd_err", errs_f[h], "cen", cen, "cen_err", errs_c[h])

hs = [D(1), D("0.1"), D("0.01"), D("0.001")]
for i in range(3):
    print("fwd ratio", hs[i], "/", hs[i + 1], "=", errs_f[hs[i]] / errs_f[hs[i + 1]])
for i in range(3):
    print("cen ratio", hs[i], "/", hs[i + 1], "=", errs_c[hs[i]] / errs_c[hs[i + 1]])

# Remark 3.3
print("fwd/cen at h=0.01:", errs_f[D("0.01")] / errs_c[D("0.01")], " printed 24199 claim; 24198.99998 claim")
print("fwd err h=0.01 unrounded:", errs_f[D("0.01")])
print("cen err h=0.01 unrounded:", errs_c[D("0.01")])

# Example 3.2 leading terms
print("leading fwd at h=0.001 =", D("0.001") / 10648, " ratio to printed-unrounded:", errs_f[D("0.001")] / (D("0.001") / 10648))
print("leading cen at h=0.001 =", D("1e-6") / 2576816, " ratio:", errs_c[D("0.001")] / (D("1e-6") / 2576816))
print("h=1 cen ratio to leading:", errs_c[D(1)] / (D(1) / 2576816))
print("h=1 fwd ratio to leading:", errs_f[D(1)] / (D(1) / 10648))

# Proposition 3.1 constants (exact)
pp = -D(1) / (4 * D(1331))  # p''(120): (1+a)^{3/2} = 1331
ppp = D(3) / (8 * D(161051))  # (1+a)^{5/2} = 161051
print("p'' =", pp, " -1/5324 diff", abs(pp + D(1) / 5324))
print("p''' =", ppp, " 3/1288408 diff", abs(ppp - D(3) / 1288408))
print("fwd lead coefficient h/2 p'' =", pp / 2, " -1/10648 check", D(-1) / 10648)
print("cen lead coefficient h^2/6 p''' =", ppp / 6, " 1/2576816 check", D(1) / 2576816)

# Numerical check of p''' with exact Fraction-free numeric derivative is covered by closed form.

# E2 exact 1% rise: a from 120 to 121.2
p_new = p_of(D("121.2"))
print("p(121.2) =", p_new, " change % =", (p_new / p0 - 1) * 100)
print("p(121.2) printed claim 10.0544109:", p_new)

# Remark 1.2 / Example 1.3 / M1-M3 / P1 / R1-R3 exact
print("eps(10) Q=120-2p:", -D(2) * 10 / (120 - 2 * 10), " eps(40):", -D(2) * 40 / (120 - 80))
print("M1 eps(10) Q=100-4p:", -D(4) * 10 / (100 - 40), " 2/3 =", D(2) / 3)
print("M3 eps(20) with D=50e^{-0.1p}: -0.1p =", -D("0.1") * 20)
print("R1 dp/da formula:", D(1) / (D(-3) + 1))
print("R2 dp/da:", D(1) / (2 * D(120).sqrt()) , "at a=120 p*=", D(120).sqrt())
print("R3 at a=120:", D(120) / (2 * 10 * 11), " 6/11 =", D(6) / D(11))
print("a/(2b) for M1:", D(100) / 8)

# Lab docstring: 1 - 2/22 etc done. Lab part B elasticity check 12/22
print("12/22 =", Fraction(12, 22), float(Fraction(12, 22)))
