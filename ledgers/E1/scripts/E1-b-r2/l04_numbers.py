"""Recompute every number in L04 prose and problems, independently, at 80 significant digits (Decimal)."""
from decimal import Decimal as D, getcontext

getcontext().prec = 80
A, B, DS = D(120), D(2), D(1)


def p_of(a):
    return (-B + (B * B + 4 * a * DS).sqrt()) / (2 * DS)


p0 = p_of(A)
dp_exact = 1 / (2 * (1 + A).sqrt())  # d/da sqrt(1+a)
print("p0", p0)
print("dp/da exact", dp_exact, "1/22 diff", dp_exact - D(1) / D(22))
print("elasticity of p* in a", A / p0 * dp_exact, "6/11 diff", A / p0 * dp_exact - D(6) / D(11))
# exact change for a 120 -> 121.2 (1% rise in a)
p1 = p_of(D("121.2"))
print("p(121.2)", p1, "pct change", (p1 - p0) / p0 * 100)
print("pct change to 10 dp", (p1 - p0) / p0 * 100)
hs = [D(1), D("0.1"), D("0.01"), D("0.001")]
rows = []
for h in hs:
    up, lo = p_of(A + h), p_of(A - h)
    fwd = (up - p0) / h
    cen = (up - lo) / (2 * h)
    rows.append((h, abs(fwd - dp_exact), abs(cen - dp_exact), fwd, cen))
    print("h", h, "fwd", fwd, "fwd_err", abs(fwd - dp_exact), "cen", cen, "cen_err", abs(cen - dp_exact))
for i in range(3):
    print("forward error ratio h", rows[i][0], "/", rows[i + 1][0], "=", rows[i][1] / rows[i + 1][1])
for i in range(3):
    print("central error ratio h", rows[i][0], "/", rows[i + 1][0], "=", rows[i][2] / rows[i + 1][2])
# leading terms
pp2 = -1 / (4 * (1 + A).sqrt() ** 3)
pp3 = D(3) / (8 * (1 + A).sqrt() ** 5)
print("p''(120)", pp2, "-1/5324 diff", pp2 + D(1) / D(5324))
print("p'''(120)", pp3, "3/1288408 diff", pp3 - D(3) / D(1288408))
lead_fwd_001 = D("0.001") / D(10648)
lead_cen_001 = D("1e-6") / D(2576816)
print("lead fwd h=.001", lead_fwd_001, "printed-ish ratio fwd_err/lead", rows[3][1] / lead_fwd_001)
print("lead cen h=.001", lead_cen_001, "ratio cen_err/lead", rows[3][2] / lead_cen_001, "rel diff", abs(rows[3][2] / lead_cen_001 - 1))
print("ratio fwd_err/lead at h=1", rows[0][1] / (D(1) / D(10648)), "cen_err/lead at h=1", rows[0][2] / (D(1) / D(2576816)))
print("ratio fwd err to cen err at h=0.01", rows[2][1] / rows[2][2])
print("leading fwd at h=0.01", D("0.01") / D(10648), "fwd err at 0.01", rows[2][1])
print("fwd err at h=0.1 / 0.01", rows[1][1] / rows[2][1], "from printed 9.387556e-6/9.391047e-7", D("9.387556e-6") / D("9.391047e-7"))
print("central 0.1/0.01 printed ratio", D("3.880759e-9") / D("3.880758e-11") * 1, "times 100 ->", D("3.880759") / D("3.880758") * 100)
print("central 0.1/0.01 unrounded ratio", rows[1][2] / rows[2][2])
print("p(121.2) exact vs derivative pct 0.5454545", (p1 - p0) / p0 * 100 - D("0.5454545455"))
