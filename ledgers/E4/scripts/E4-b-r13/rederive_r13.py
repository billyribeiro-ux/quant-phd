"""Round-13 independent re-derivation of L06 and L04/L05 numbers in exact Fractions (no lab code imported)."""
from fractions import Fraction as F

# Base instance of Example 6.9 (a = 1) and Problems M1-M3 (a = 2)
def closed(sv2, se2, a, lam, su2):
    tv, te = 1 / F(sv2), 1 / F(se2)
    kap = F(a) / (lam * te)
    seta2 = F(se2) + kap * kap * F(su2)
    teta = 1 / seta2
    tbar = lam * te + (1 - lam) * teta
    ths = tbar / (tv + tbar)
    return kap, seta2, teta, tbar, ths, kap * ths

k, s2, t, tb, ts, tu = closed(1, 1, 1, F(1, 2), F(1, 4))
print("Ex6.9 kappa", k, "sig_eta2", s2, "tau_eta", t, "tau_bar", tb, "theta_s", ts, "theta_u", tu)
varp = ts**2 * 2 + tu**2 * F(1, 4)
cov = ts * 1
b = cov / varp
print("Ex6.9 Var(p)", varp, "Cov(v,p)", cov, "b", b, "closed b", t / (ts * (1 + t)), "V_U", 1 - b * cov, "1/(tau_v+tau_eta)", 1 / (1 + t))
# Lab grid residual, independent implementation
def resid(s, u, ths_, thu, a=F(1), lam=F(1, 2), sv2=F(1), se2=F(1), su2=F(1, 4)):
    p = ths_ * s - thu * u
    varp_ = ths_**2 * (sv2 + se2) + thu**2 * su2
    cvp = ths_ * sv2
    slope = cvp / varp_
    vu = sv2 - slope * cvp
    vi = sv2 * se2 / (sv2 + se2)
    di = (sv2 * s / (sv2 + se2) - p) / (a * vi)
    du = (slope * p - p) / (a * vu)
    return lam * di + (1 - lam) * du - u
grid_s = [F(-1), F(0), F(1), F(2)]
grid_u = [F(-1), F(0), F(1, 2), F(2)]
res = [resid(s, u, ts, tu) for s in grid_s for u in grid_u]
print("grid points", len(res), "zeros", sum(1 for r in res if r == 0))
print("alt slope 1/2 residual at (1,0):", resid(F(1), F(0), F(1, 2), tu), "=", resid(F(1), F(0), F(1, 2), tu) == F(-9, 85))
print("residual at (1,0) with equilibrium:", resid(F(1), F(0), ts, tu))
# Part E floats: tolerance and sample check are re-run by the twin; here only the population values
print("3/7 =", float(F(3, 7)), " 7/9 =", float(F(7, 9)))
print("Part E difference / tolerance", (0.426617 - 3 / 7) / 0.006497, " difference in SE units", (0.426617 - 3 / 7) / (0.006497 / 3))
print("Example 6.9 hypothetical: (0.80 - 7/9)/0.05 =", (0.80 - 7 / 9) / 0.05)

# Problems M1-M3, a = 2
k2, s22, t2, tb2, ts2, tu2 = closed(1, 1, 2, F(1, 2), F(1, 4))
print("M1 kappa", k2, "sig_eta2", s22, "tau_eta", t2, "tau_bar", tb2, "theta_s", ts2, "theta_u", tu2)
varp2 = ts2**2 * 2 + tu2**2 * F(1, 4)
b2 = (ts2) / varp2
print("M2 Var(p)", varp2, "b", b2, "Var(v|p)", 1 - b2 * ts2, "1/(1+tau_eta)", 1 / (1 + t2), "corr^2", ts2**2 / varp2, "sv2/(sv2+seta2)", F(1) / (1 + s22))
p3 = ts2 * 2 - tu2 * 1
xi = (2 + F(3, 2) * 0 + 1 * 2 - 0) / 2  # placeholder overwritten below
tau_v, tau_e = F(1), F(1)
xi = (tau_e * 2 - (tau_v + tau_e) * p3) / 2
Y = p3 / ts2
xu = (t2 * Y - (tau_v + t2) * p3) / 2
print("M3 p", p3, "x_I", xi, "Y", Y, "x_U", xu, "clear", F(1, 2) * xi + F(1, 2) * xu)
# E1 and E2 arithmetic in the page
print("E2 (sample - 3/7)", 0.426617 - 3 / 7, "SE units", (0.426617 - 3 / 7) / (0.006497 / 3))
# R1: corr^2 limit form, symbolic check at one lambda (lam = 1/10)
sv2, se2, a, su2 = F(1), F(1), F(1), F(1, 4)
for lam in (F(1, 10), F(1, 1000)):
    kap, s2_, te_, tb_, ts_, tu_ = closed(1, 1, a, lam, su2)
    varp_ = ts_**2 * (sv2 + se2) + tu_**2 * su2
    corr2 = (ts_ * sv2) ** 2 / (sv2 * varp_)
    print("R1 lam", lam, "corr^2", corr2, "sv2/(sv2+seta2)", sv2 / (sv2 + s2_))
# R2 monotonic check numerically
vals = [1 / (1 + closed(1, 1, 1, F(1, 2), su)[2]) for su in (F(1, 8), F(1, 4), F(1, 2), F(1))]
print("R2 Var(v|p) over sigma_u^2 in 1/8,1/4,1/2,1:", [float(v) for v in vals], "increasing", all(vals[i] < vals[i + 1] for i in range(3)))
# P3 identity
sv, sn = F(3), F(5)
print("P3 lhs", sv - sv**2 / (sv + sn), "rhs", sv * sn / (sv + sn), "1/(tau_v+tau_eta)", 1 / (1 / sv + 1 / sn))
# Quiz values
print("quiz numeric: theta_s 3/7 =", float(F(3, 7)), " b 7/9 =", float(F(7, 9)), " V_I =", F(1, 2), " x_I =", (F(1, 2) - F(3, 7)) / F(1, 2))
