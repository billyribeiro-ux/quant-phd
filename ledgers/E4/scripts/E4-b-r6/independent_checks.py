"""Independent recomputation of the L04-L06 numbers in prose, cards and problem solutions (exact Fractions).

Run from the repo root: .venv/bin/python ledgers/E4/scripts/E4-b-r6/independent_checks.py
Prints one line per check and 'ALL OK' only if every check holds."""

import math
from fractions import Fraction as F

ok: list[bool] = []


def check(name: str, cond: bool) -> None:
    ok.append(cond)
    print(("OK   " if cond else "FAIL ") + name)


# ---- L05: fixed point, ratios, path, residuals ----
def psi(c, al, be, vs, de):
    return ((al - vs * c[0]) / be, -(vs * c[1] + de) / be)


def fp(al, be, vs, de):
    return (al / (be + vs), -de / (be + vs))


al, be, vs, de = F(10), F(2), F(1, 2), F(3, 4)
t = fp(al, be, vs, de)
check("L05 base fixed point (4, -3/10)", t == (F(4), F(-3, 10)))
check("L05 base residual zero", psi(t, al, be, vs, de) == t)
path = [(F(0), F(0))]
for _ in range(8):
    path.append(psi(path[-1], al, be, vs, de))
check("L05 base c0 path 15/4, 65/16 at k=2,3", path[2][0] == F(15, 4) and path[3][0] == F(65, 16))
check("L05 c0 error ratios all -1/4", all((path[k + 1][0] - t[0]) / (path[k][0] - t[0]) == F(-1, 4) for k in range(8)))
check("L05 c1 error ratios all -1/4", all((path[k + 1][1] - t[1]) / (path[k][1] - t[1]) == F(-1, 4) for k in range(8)))
e5 = path[5][0] - t[0]
check("L05 E1: |e_5| = 1/256 and c0 path[5] = 1025/256", e5 == F(1, 256) and path[5][0] == F(1025, 256))
check("L05 E1: |e_4| = 1/64 > 0.01 and |e_5| < 0.01", F(1, 64) > F(1, 100) and F(1, 256) < F(1, 100))
t2 = fp(al, F(2), F(2), de)
p2 = [(F(0), F(0))]
for _ in range(6):
    p2.append(psi(p2[-1], al, F(2), F(2), de))
check("L05 equal case c0* = 5/2, path alternates 0,5", t2[0] == F(5, 2) and [x[0] for x in p2[:4]] == [0, 5, 0, 5])
check("L05 equal case ratio -1", (p2[1][0] - t2[0]) / (p2[0][0] - t2[0]) == -1)
check("L05 Psi(5/2) = 5/2 (E2)", psi((F(5, 2), F(0)), al, F(2), F(2), de)[0] == F(5, 2))
t3 = fp(al, F(2), F(3), de)
p3 = [(F(0), F(0))]
for _ in range(4):
    p3.append(psi(p3[-1], al, F(2), F(3), de))
check("L05 large case c*=2 and path 0,5,-5/2,35/4", t3[0] == 2 and [x[0] for x in p3[:4]] == [0, 5, F(-5, 2), F(35, 4)])
errs = [x[0] - 2 for x in p3[:4]]
check("L05 E3 errors -2,3,-9/2,27/4 and ratio -3/2", errs == [F(-2), F(3), F(-9, 2), F(27, 4)] and all(errs[k + 1] / errs[k] == F(-3, 2) for k in range(3)))
nu = F(2) / (F(2) + F(2))
check("L05 R1 damped weight 1/2 gives c0*=5/2", (1 - nu) * 0 + nu * psi((F(0), F(0)), F(10), F(2), F(2), F(0))[0] == F(5, 2))
check("L05 M1 fixed point (3, -1/2) at alpha=12,beta=3,sig=1,delta=2", fp(F(12), F(3), F(1), F(2)) == (F(3), F(-1, 2)))
check("L05 M2 Psi(0,0)=(4,-2/3) and ratios -1/3", psi((F(0), F(0)), F(12), F(3), F(1), F(2)) == (F(4), F(-2, 3)))
check("L05 M3 conditional variance 5/4", (F(4) + F(1)) / F(2) ** 2 == F(5, 4))
check("L05 quiz 1/4 ratio and 4/5 weight", F(1, 2) / 2 == F(1, 4) and F(2) / (F(2) + F(1, 2)) == F(4, 5))

# ---- L06: Example 6.9, Prop 6.7, Cor 6.8, Lemma 6.3/6.4 ----
sv, se, a, lam, su = F(1), F(1), F(1), F(1, 2), F(1, 4)
tv, te = 1 / sv, 1 / se
kap = a * se / lam
seta2 = se + kap * kap * su
taue = 1 / seta2
taubar = lam * te + (1 - lam) * taue
ths = taubar / (tv + taubar)
thu = kap * ths
check("L06 Ex 6.9 kappa=2, sig_eta^2=2, tau_eta=1/2, taubar=3/4", (kap, seta2, taue, taubar) == (2, 2, F(1, 2), F(3, 4)))
check("L06 Ex 6.9 theta_s=3/7, theta_u=6/7", (ths, thu) == (F(3, 7), F(6, 7)))
var_p = ths**2 * (sv + se) + thu**2 * su
cov = ths * sv
b = cov / var_p
vu = sv - b * cov
check("L06 Part B: Var(p)=27/49, Cov=3/7, b=7/9, Var(v|p)=2/3", (var_p, cov, b, vu) == (F(27, 49), F(3, 7), F(7, 9), F(2, 3)))
check("L06 b equals tau_eta/(theta_s(tau_v+tau_eta))", b == taue / (ths * (tv + taue)))
check("L06 Var(v|p)=1/(tau_v+tau_eta)", vu == 1 / (tv + taue))
rho2 = cov**2 / (sv * var_p)
check("L06 rho^2 = 1/3 = sig_v^2/(sig_v^2+sig_eta^2)", rho2 == F(1, 3) == sv / (sv + seta2))
w = sv / (sv + se)
vI = sv * se / (sv + se)
xI = (w * 1 - F(3, 7)) / (a * vI)
xU = (b * F(3, 7) - F(3, 7)) / (a * vu)
check("L06 Ex 6.9 x_I(1,0)=1/7, x_U=-1/7, clear", xI == F(1, 7) and xU == F(-1, 7) and lam * xI + (1 - lam) * xU == 0)


def resid(s, uu, thsv, thuv):
    price = thsv * s - thuv * uu
    vp = thsv * thsv * (sv + se) + thuv * thuv * su
    cv = thsv * sv
    sl = cv / vp
    rv = sv - sl * cv
    dinf = (w * s - price) / (a * vI)
    dunf = (sl * price - price) / (a * rv)
    return lam * dinf + (1 - lam) * dunf - uu


grid_s = [F(-1), F(0), F(1), F(2)]
grid_u = [F(-1), F(0), F(1, 2), F(2)]
zeros = sum(1 for s in grid_s for uu in grid_u if resid(s, uu, ths, thu) == 0)
check("L06 Part C: 16 of 16 grid residuals zero", zeros == 16)
check("L06 Part D: residual at (1,0) with theta_s=1/2 is -9/85", resid(F(1), F(0), F(1, 2), thu) == F(-9, 85))
check("L06 Part C informed demand at (1,0) is 1/7", (w * 1 - ths * 1) / (a * vI) == F(1, 7))
# Remark 6.10 and R1 limit identity: Corr(v,p)^2 = sig_v^2/(sig_v^2+sig_eta^2)
check("L06 Corr(v,p)^2 = sig_v^2/(sig_v^2+sig_eta^2) at base", cov**2 / (sv * var_p) == sv / (sv + seta2))

# M1-M3 at a new instance
kap2 = F(2) * 1 / F(1, 2)
se2 = 1 + kap2**2 * F(1, 4)
te2 = 1 / se2
tb2 = F(1, 2) * 1 + F(1, 2) * te2
th2 = tb2 / (1 + tb2)
tu2 = kap2 * th2
check("L06 M1 (a=2): kappa=4, sig_eta^2=5, tau_eta=1/5, taubar=3/5, theta_s=3/8, theta_u=3/2", (kap2, se2, te2, tb2, th2, tu2) == (4, 5, F(1, 5), F(3, 5), F(3, 8), F(3, 2)))
var_p2 = th2**2 * 2 + tu2**2 * F(1, 4)
cov2 = th2
b2 = cov2 / var_p2
vu2 = 1 - b2 * cov2
check("L06 M2: Var(p)=27/32, b=4/9, Var(v|p)=5/6, rho^2=1/6", (var_p2, b2, vu2, cov2**2 / var_p2) == (F(27, 32), F(4, 9), F(5, 6), F(1, 6)))
p_m3 = th2 * 2 - tu2 * 1
Y = p_m3 / th2
xi3 = (2 - (1 + 1) * p_m3) / 2
xu3 = (te2 * Y - (1 + te2) * p_m3) / 2
check("L06 M3: p=-3/4, x_I=7/4, x_U=1/4, clears to u=1", (p_m3, xi3, xu3) == (F(-3, 4), F(7, 4), F(1, 4)) and F(1, 2) * xi3 + F(1, 2) * xu3 == 1)

# E1, E2 of L06 (decimal prose)
check("L06 E1: 0.80 - 7/9 = 0.0222, /0.05 = 0.44 SE", abs((0.80 - 7 / 9) / 0.05 - 0.444) < 0.01)
diff = 0.426617 - 3 / 7
check("L06 E2: diff -0.001954, /tol -0.30, SE 0.002166, /SE -0.90", abs(diff + 0.001954) < 1e-6 and abs(diff / 0.006497 + 0.30) < 0.005 and abs(0.006497 / 3 - 0.002166) < 1e-6 and abs(diff / (0.006497 / 3) + 0.90) < 0.01)

# ---- L04: rank examples and Remark 3.2 / Prop 4.2 ----
def rank(M):
    rows = [list(r) for r in M]
    nr, nc = len(rows), len(rows[0])
    used = 0
    for col in range(nc):
        piv = next((i for i in range(used, nr) if rows[i][col] != 0), None)
        if piv is None:
            continue
        rows[used], rows[piv] = rows[piv], rows[used]
        for i in range(nr):
            if i != used and rows[i][col] != 0:
                f = rows[i][col] / rows[used][col]
                rows[i] = [x - f * y for x, y in zip(rows[i], rows[used])]
        used += 1
    return used


inc = [[F(1), F(1), F(1)], [F(0), F(1), F(2)]]
com = [[F(1), F(0), F(0)], [F(0), F(1), F(0)], [F(0), F(0), F(1)], [F(1), F(2), F(3)]]
check("L04 ranks 2 (incomplete) and 3 (complete)", rank(inc) == 2 and rank(com) == 3)
check("L04 M1 rank of (1,2,0),(2,4,0) is 1", rank([[F(1), F(2), F(0)], [F(2), F(4), F(0)]]) == 1)
check("L04 M3 rank of r1..r4 is 2", rank([[F(1), F(2), F(0)], [F(0), F(1), F(1)], [F(1), F(3), F(1)], [F(2), F(5), F(1)]]) == 2)
check("L04 E3 rank of three securities is 2", rank([[F(1), F(1), F(0)], [F(0), F(1), F(1)], [F(1), F(2), F(1)]]) == 2)
check("L04 misconception rows rank 2", rank([[F(1), F(1), F(1)], [F(1), F(1), F(1)], [F(0), F(1), F(2)]]) == 2)
check("L04 Example 2.2 (1,2,3) attainable, (0,0,1) not", rank(inc + [[F(1), F(2), F(3)]]) == 2 and rank(inc + [[F(0), F(0), F(1)]]) == 3)
check("L04 E2 identity: (1-t,2-2t,3-3t,t) replicates (1,2,3)", all(
    [(1 - t) * com[0][k] + (2 - 2 * t) * com[1][k] + (3 - 3 * t) * com[2][k] + t * com[3][k] for k in range(3)] == [1, 2, 3]
    for t in (F(0), F(1), F(7, 3))))
check("L04 R3 construction: t=max(0,-x1,-x2) gives nonneg zeta with payoff xi", all(
    (lambda x1, x2: (lambda tt: (x1 + tt >= 0 and x2 + tt >= 0 and (x1 + tt - tt, x2 + tt - tt) == (x1, x2) and max(0, -x1, -x2) >= 0)))(F(x1), F(x2)) for x1 in range(-3, 4) for x2 in range(-3, 4)))
check("L04 Remark 3.2 kernel dim J - rank", 4 - rank(com) == 1)

print("ALL OK" if all(ok) else f"SOME FAILED: {ok.count(False)}")
print("sqrt sanity", round(math.sqrt(2), 4))
