"""Independent re-derivation of the L04 and L06 prose numbers (round 3). Prints every check with its value."""
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 80
D = Decimal


def p(a):
    return (a + 1).sqrt() - 1


P0 = p(D(120))
DP = 1 / (2 * (D(121)).sqrt())
print("p(120) =", P0, "dp/da exact 1/22 =", DP, "diff", DP - D(1) / D(22))
print("elasticity (a/p)(dp/da) =", D(120) / P0 * DP, "6/11 diff", D(120) / P0 * DP - D(6) / D(11))
print("exact 1% rise change % =", (p(D("121.2")) - P0) / P0 * 100)
print("p(121.2) =", p(D("121.2")))
steps = [D(1), D("0.1"), D("0.01"), D("0.001")]
fe, ce = {}, {}
for h in steps:
    up, lo = p(D(120) + h), p(D(120) - h)
    fwd, cen = (up - P0) / h, (up - lo) / (2 * h)
    fe[h] = abs(fwd - DP)
    ce[h] = abs(cen - DP)
    print("h", h, "fwd", fwd.quantize(D("1e-10")), "fwd_err %.6e" % fe[h], "cen", cen.quantize(D("1e-10")), "cen_err %.6e" % ce[h])
for big, small in [(D(1), D("0.1")), (D("0.1"), D("0.01")), (D("0.01"), D("0.001"))]:
    print("fwd ratio", big, "/", small, "=", fe[big] / fe[small], "| cen ratio =", ce[big] / ce[small])
print("fwd err h=0.01 unrounded =", fe[D("0.01")], "cen err h=0.01 =", ce[D("0.01")])
print("fwd/cen ratio at h=0.01 =", fe[D("0.01")] / ce[D("0.01")])
# Example 3.2 leading terms
lead_f = D("0.001") / D(10648)
lead_c = D("1e-6") / D(2576816)
print("lead fwd h=0.001", lead_f, "fwd err / lead", fe[D("0.001")] / lead_f, "(prose 0.99999587)")
print("lead cen h=0.001", lead_c, "cen err / lead", ce[D("0.001")] / lead_c, "rel diff", abs(ce[D("0.001")] - lead_c) / lead_c)
print("h=1: cen err / lead", ce[D(1)] / (D(1) / D(2576816)), "(prose 1.0000299)")
print("h=1: fwd err / lead", fe[D(1)] / (D(1) / D(10648)), "(prose 0.99589)")
print("E1 ratio cen h=0.1 / h=0.01 =", ce[D("0.1")] / ce[D("0.01")] * 100 / 100, "x100 check", ce[D("0.1")] / ce[D("0.01")])
print("printed-value ratio 3.880759/3.880758*100 =", D("3.880759") / D("3.880758") * 100)
print("forward ratio at h=0.1 vs 0.01 printed 9.387556/0.9391047 =", D("9.387556") / D("0.9391047"))
# Fraction checks on Prop 3.1 constants
pp = -Fraction(1, 4) * Fraction(1, 121 ** 1) ** 0  # placeholder
print("p''(120) = -1/(4*121^(3/2)) = -1/", 4 * 1331, " ; p'''(120) = 3/(8*121^(5/2)) = 3/", 8 * 161051)
print("exact p'' from formula check:", Fraction(-1, 4 * 1331) == Fraction(-1, 5324))
print("remark 3.3 ratio 24198.99998 check:", fe[D("0.01")] / ce[D("0.01")])
