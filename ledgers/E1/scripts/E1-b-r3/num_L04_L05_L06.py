"""Independent recomputation of the displayed numbers in E1 L04, L05 and L06 (round 3, slice E1-b)."""
from decimal import Decimal as D, getcontext
from fractions import Fraction as F
getcontext().prec = 60

def p(a):
    return D(-2) * 0 + (D(-2) + (D(4) + 4 * a).sqrt()) / 2 if False else (D(-2)*0) + ((D(4) + 4*a).sqrt() - 2) / 2

# L04: demand a-2p, supply p^2  => p(a) = sqrt(1+a)-1 ; the lab uses b=2, d=1: p=(-b+sqrt(b^2+4ad))/(2d)
def pe(a):
    return (D(-2) + (D(4) + 4 * a).sqrt()) / 2
p0 = pe(D(120))
dp = 1 / (D(2) + 2 * p0)
print("p0", p0, "dp", dp)
h_list = [D(1), D("0.1"), D("0.01"), D("0.001")]
rows = []
for h in h_list:
    fwd = (pe(D(120) + h) - p0) / h
    cen = (pe(D(120) + h) - pe(D(120) - h)) / (2 * h)
    rows.append((h, fwd - dp, cen - dp))
    print("h", h, "fwd_err", fwd - dp, "cen_err", cen - dp)
for i in range(1, 4):
    print("fwd ratio step", i, rows[i-1][1] / rows[i][1])
    print("cen ratio step", i, rows[i-1][2] / rows[i][2])
# Remark 3.3 ratio at h=0.01
fe = rows[2][1]; ce = rows[2][2]
print("Remark3.3 fwd", fe, "cen", ce, "ratio", fe / ce)
# Example 3.2 leading terms
lead_fwd = lambda h: -h / D(10648)
lead_cen = lambda h: h * h / D(2576816)
h = D("0.001")
print("E3.2 h=0.001 leading fwd", lead_fwd(h), "ratio fwd_err/lead", rows[3][1] / lead_fwd(h))
print("E3.2 h=0.001 leading cen", lead_cen(h), "ratio cen_err/lead", rows[3][2] / lead_cen(h))
print("E3.2 h=1 ratio cen_err/lead", rows[0][2] / lead_cen(D(1)), "fwd_err/lead", rows[0][1] / lead_fwd(D(1)))
print("E3.2 leading fwd at 0.001 printed as 9.3914350e-8:", lead_fwd(h))
print("E3.2 leading cen at 0.001 printed as 3.8807583e-13:", lead_cen(h))
# E1 ratio central 0.1 vs 0.01
print("E1 central ratio 0.1/0.01", rows[1][2] / rows[2][2])
# interpretation: exact change for a 120->121.2 and the percent
p1 = pe(D("121.2"))
print("p(121.2)", p1, "pct change", (p1 - p0) / p0 * 100, "elasticity", D(120) / p0 * dp, "pct for 1% a", (D(12)/D(10)))
print("elasticity 6/11", D(6)/D(11))
