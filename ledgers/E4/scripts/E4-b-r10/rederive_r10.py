"""Independent re-derivation of the L04-L06 numbers (round 10). Standard library only, exact Fractions where possible."""

import math
import random
from fractions import Fraction as F

fails: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    print(("OK   " if cond else "FAIL ") + name + (" | " + detail if detail else ""))
    if not cond:
        fails.append(name)


def rank_exact(rows):
    """Rank by row reduction over Fractions (independent implementation)."""
    m = [[F(x) for x in r] for r in rows]
    r = 0
    ncols = len(m[0])
    for c in range(ncols):
        piv = None
        for i in range(r, len(m)):
            if m[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c] / m[r][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
    return r


# ---- L04
inc = [[1, 1, 1], [0, 1, 2]]
com = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 2, 3]]
check("L04 rank incomplete = 2", rank_exact(inc) == 2)
check("L04 rank complete = 3", rank_exact(com) == 3)
check("L04 (1,2,3) augmented rank incomplete = 2", rank_exact(inc + [[1, 2, 3]]) == 2)
check("L04 (0,0,1) augmented rank incomplete = 3", rank_exact(inc + [[0, 0, 1]]) == 3)
check("L04 (5,0,0) augmented rank incomplete = 3", rank_exact(inc + [[5, 0, 0]]) == 3)
check("L04 (1,2,3) augmented rank complete = 3", rank_exact(com + [[1, 2, 3]]) == 3)
check("L04 first three rows rank 3", rank_exact(com[:3]) == 3)
check("L04 misconception rank (1,1,1),(1,1,1),(0,1,2) = 2", rank_exact([[1, 1, 1], [1, 1, 1], [0, 1, 2]]) == 2)
check("L04 M1 rank (1,2,0),(2,4,0) = 1", rank_exact([[1, 2, 0], [2, 4, 0]]) == 1)
check("L04 M3 rank 2", rank_exact([[1, 2, 0], [0, 1, 1], [1, 3, 1], [2, 5, 1]]) == 2)
check("L04 E3 rank 2", rank_exact([[1, 1, 0], [0, 1, 1], [1, 2, 1]]) == 2)
# Replication family for (1,2,3) in the four-security market
ok = True
for t in [F(0), F(1), F(-3, 7), F(5, 2)]:
    z = [1 - t, 2 - 2 * t, 3 - 3 * t, t]
    payoff = [sum(z[j] * com[j][k] for j in range(4)) for k in range(3)]
    ok &= payoff == [1, 2, 3]
check("L04 replication family (1-t,2-2t,3-3t,t) for all tested t", ok)
# R3 nonnegative holdings construction
ok = True
import itertools

for x1, x2 in [(F(-3), F(2)), (F(2), F(-5)), (F(1, 3), F(-1, 7)), (F(0), F(0)), (F(-2), F(-2))]:
    t = max(F(0), -x1, -x2)
    z1, z2, z3 = x1 + t, x2 + t, t
    ok &= z1 >= 0 and z2 >= 0 and z3 >= 0 and (z1 - z3, z2 - z3) == (x1, x2)
check("L04 R3 nonnegative construction on sample payoffs", ok)

# ---- L05
def fp(alpha, beta, vs, dl):
    return (alpha / (beta + vs), -dl / (beta + vs))


def Psi(c, alpha, beta, vs, dl):
    return ((alpha - vs * c[0]) / beta, -(vs * c[1] + dl) / beta)


alpha, beta, vs, dl = F(10), F(2), F(1, 2), F(3, 4)
c = fp(alpha, beta, vs, dl)
check("L05 base fixed point (4, -3/10)", c == (4, F(-3, 10)), str(c))
check("L05 base residual zero", Psi(c, alpha, beta, vs, dl) == c)
path = [(F(0), F(0))]
for _ in range(8):
    path.append(Psi(path[-1], alpha, beta, vs, dl))
c0p = [str(p[0]) for p in path]
check("L05 base c0 path matches printed", c0p == ['0', '5', '15/4', '65/16', '255/64', '1025/256', '4095/1024', '16385/4096', '65535/16384'], str(c0p))
ratios = [(path[k + 1][0] - c[0]) / (path[k][0] - c[0]) for k in range(8)]
check("L05 base c0 ratios all -1/4", all(r == F(-1, 4) for r in ratios))
ratios1 = [(path[k + 1][1] - c[1]) / (path[k][1] - c[1]) for k in range(8)]
check("L05 base c1 ratios all -1/4", all(r == F(-1, 4) for r in ratios1))
# equal parameters
a2, b2, s2, d2 = F(10), F(2), F(2), F(3, 4)
c_eq = fp(a2, b2, s2, d2)
p2 = [(F(0), F(0))]
for _ in range(6):
    p2.append(Psi(p2[-1], a2, b2, s2, d2))
check("L05 equal: fixed point 5/2, -3/16", c_eq == (F(5, 2), F(-3, 16)), str(c_eq))
check("L05 equal: c0 path alternates 0,5", [str(p[0]) for p in p2] == ['0', '5', '0', '5', '0', '5', '0'])
# large parameters
a3, b3, s3, d3 = F(10), F(2), F(3), F(3, 4)
c_l = fp(a3, b3, s3, d3)
p3 = [(F(0), F(0))]
for _ in range(6):
    p3.append(Psi(p3[-1], a3, b3, s3, d3))
check("L05 large: fixed point 2, -3/20", c_l == (2, F(-3, 20)), str(c_l))
check("L05 large: c0 path", [str(p[0]) for p in p3] == ['0', '5', '-5/2', '35/4', '-65/8', '275/16', '-665/32'], str([str(p[0]) for p in p3]))
e = [p[0] - c_l[0] for p in p3]
check("L05 large: E3 errors e3 = 27/4 and ratios -3/2", e[3] == F(27, 4) and all(e[k + 1] / e[k] == F(-3, 2) for k in range(5)))
nu = b3 / (b3 + s3)
check("L05 damped weight at base = 4/5", beta / (beta + vs) == F(4, 5))
check("L05 R1 damped weight at beta=varsigma=2 is 1/2 and gives 5/2", (F(2) / F(4)) == F(1, 2) and (1 - F(1, 2)) * 0 + F(1, 2) * (alpha - 0) / 2 == F(5, 2))
# E1 threshold
k = next(k for k in range(0, 20) if abs(F(-4) * F(-1, 4) ** k) < F(1, 100))
check("L05 E1 first k within 0.01 is 5 and path value 1025/256", k == 5 and path[5][0] == F(1025, 256))
check("L05 E1 residual 1/256", path[5][0] - 4 == F(1, 256))

# M1..M3 L05
c_m1 = fp(F(12), F(3), F(1), F(2))
check("L05 M1 (3,-1/2)", c_m1 == (3, F(-1, 2)))
check("L05 M2 ratio -1/3", (Psi((F(0), F(0)), F(12), F(3), F(1), F(2))[0] - 3) / (0 - 3) == F(-1, 3) and (Psi((F(0), F(0)), F(12), F(3), F(1), F(2))[1] + F(1, 2)) / (F(1, 2)) == F(-1, 3))
check("L05 M3 variance 5/4", (F(4) + F(1)) / F(2) ** 2 == F(5, 4))

# ---- L06
def closed(sv2, se2, a, lam, su2):
    tv, te = 1 / sv2, 1 / se2
    kappa = a / (lam * te)
    seta2 = se2 + kappa * kappa * su2
    teta = 1 / seta2
    tbar = lam * te + (1 - lam) * teta
    ths = tbar / (tv + tbar)
    thu = kappa * ths
    return kappa, seta2, teta, tbar, ths, thu


def clears(ths, thu, sv2, se2, a, lam, su2, s, u):
    p = ths * s - thu * u
    varp = ths * ths * (sv2 + se2) + thu * thu * su2
    covvp = ths * sv2
    slope = covvp / varp
    rv = sv2 - slope * covvp
    vI = sv2 * se2 / (sv2 + se2)
    om = sv2 / (sv2 + se2)
    xI = (om * s - p) / (a * vI)
    xU = (slope * p - p) / (a * rv)
    return lam * xI + (1 - lam) * xU - u


# Example 6.9 base
kap, seta2, teta, tbar, ths, thu = closed(F(1), F(1), F(1), F(1, 2), F(1, 4))
check("L06 base kappa=2 sig_eta2=2 tau_eta=1/2 tau_bar=3/4 theta_s=3/7 theta_u=6/7",
      (kap, seta2, teta, tbar, ths, thu) == (2, 2, F(1, 2), F(3, 4), F(3, 7), F(6, 7)))
check("L06 base clears at grid 16 points exact", all(clears(ths, thu, F(1), F(1), F(1), F(1, 2), F(1, 4), s, u) == 0 for s in [F(-1), F(0), F(1), F(2)] for u in [F(-1), F(0), F(1, 2), F(2)]))
check("L06 base alt slope 1/2 residual at (1,0) = -9/85", clears(F(1, 2), thu, F(1), F(1), F(1), F(1, 2), F(1, 4), F(1), F(0)) == F(-9, 85))
check("L06 base informed demand at (1,0) = 1/7", (F(1, 2) * 1 - F(3, 7)) / (F(1, 2)) == F(1, 7))
# M1..M3
kap, seta2, teta, tbar, ths, thu = closed(F(1), F(1), F(2), F(1, 2), F(1, 4))
check("L06 M1 (kappa,sig_eta2,tau_eta,tau_bar,theta_s,theta_u)=(4,5,1/5,3/5,3/8,3/2)",
      (kap, seta2, teta, tbar, ths, thu) == (4, 5, F(1, 5), F(3, 5), F(3, 8), F(3, 2)))
varp = ths * ths * 2 + thu * thu * F(1, 4)
check("L06 M2 Var(p) = 27/32", varp == F(27, 32))
b = (ths) / varp
check("L06 M2 b = 4/9", b == F(4, 9))
check("L06 M2 posterior 5/6", 1 - b * ths == F(5, 6))
check("L06 M2 squared corr 1/6", ths * ths / (1 * varp) == F(1, 6))
p = ths * 2 - thu * 1
check("L06 M3 price -3/4", p == F(-3, 4))
xI = (2 + F(3, 2)) / 2
check("L06 M3 xI=7/4 via formula (tau_e s - (tau_v+tau_e) p)/a", xI == F(7, 4))
Y = p / ths
xU = (F(1, 5) * Y - F(6, 5) * p) / 2
check("L06 M3 Y=-2, xU=1/4", Y == -2 and xU == F(1, 4))
check("L06 M3 clearing = u = 1", F(1, 2) * xI + F(1, 2) * xU == 1)
check("L06 M3 clears via general residual", clears(ths, thu, F(1), F(1), F(2), F(1, 2), F(1, 4), F(2), F(1)) == 0)
# Clearing and uniqueness (Prop 6.7(b)) on random instances: closed form clears; and any (ths,thu) that clears must equal closed form.
rng = random.Random(10)
okc = True
for _ in range(20):
    sv2 = F(rng.randint(1, 9), rng.randint(1, 9))
    se2 = F(rng.randint(1, 9), rng.randint(1, 9))
    a = F(rng.randint(1, 9), rng.randint(1, 9))
    lam = F(rng.randint(1, 8), 9)
    su2 = F(rng.randint(1, 9), rng.randint(1, 9))
    _, _, _, _, ths_, thu_ = closed(sv2, se2, a, lam, su2)
    for s_, u_ in [(F(1), F(0)), (F(0), F(1)), (F(2), F(-3)), (F(-1, 2), F(5, 3))]:
        okc &= clears(ths_, thu_, sv2, se2, a, lam, su2, s_, u_) == 0
check("L06 Prop 6.7(a) closed form clears on 20 random instances x 4 points (exact)", okc)
# Uniqueness: clearing residual is a linear function of (s,u); solve coefficient equations numerically for random
# instances over a fine scan of theta_s, theta_u -> at most one solution up to closure. Here check that a
# perturbed theta_s (scaled) gives nonzero residual.
okp = True
for _ in range(20):
    sv2 = F(rng.randint(1, 9), rng.randint(1, 9))
    se2 = F(rng.randint(1, 9), rng.randint(1, 9))
    a = F(rng.randint(1, 9), rng.randint(1, 9))
    lam = F(rng.randint(1, 8), 9)
    su2 = F(rng.randint(1, 9), rng.randint(1, 9))
    _, _, _, _, ths_, thu_ = closed(sv2, se2, a, lam, su2)
    okp &= clears(ths_ * F(1, 2), thu_, sv2, se2, a, lam, su2, F(1), F(0)) != 0 or ths_ == 0
check("L06 perturbed theta_s not an equilibrium on 20 random instances", okp)

# Part E re-simulation: same call order as the twin
SEED, N = 6, 20000
rng = random.Random(SEED)
sd_v, sd_e, sd_u = 1.0, 1.0, 0.5
ths_f, thu_f = 3 / 7, 6 / 7
sd, sp, sv = [], [], []
for _ in range(N):
    v = rng.gauss(0.0, sd_v)
    eps = rng.gauss(0.0, sd_e)
    u = rng.gauss(0.0, sd_u)
    s = v + eps
    sd.append(s)
    sp.append(ths_f * s - thu_f * u)
    sv.append(v)


def ols(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxx = sum((xi - mx) ** 2 for xi in x)
    sxy = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    slope = sxy / sxx
    icpt = my - slope * mx
    rss = sum((yi - icpt - slope * xi) ** 2 for xi, yi in zip(x, y))
    return slope, math.sqrt(rss / (n - 2) / sxx)


s1, se1 = ols(sd, sp)
s2_, se2_ = ols(sp, sv)
print(f"E-resim p_on_s {s1:.6f} tol {3*se1:.6f} ; v_on_p {s2_:.6f} tol {3*se2_:.6f}")
check("L06 Part E printed p_on_s 0.426617 tol 0.006497", f"{s1:.6f}" == "0.426617" and f"{3*se1:.6f}" == "0.006497")
check("L06 Part E printed v_on_p 0.761928 tol 0.023538", f"{s2_:.6f}" == "0.761928" and f"{3*se2_:.6f}" == "0.023538")
check("L06 E2 difference -0.001954 and tolerance ratio -0.30", round(0.426617 - 3 / 7, 6) == -0.001954 and round((0.426617 - 3 / 7) / 0.006497, 2) == -0.30)
check("L06 E2 SE = tol/3 = 0.002166, z = -0.90", round(0.006497 / 3, 6) == 0.002166 and round((0.426617 - 3 / 7) / (0.006497 / 3), 2) == -0.90)
check("L06 E1: (0.80-7/9)/0.05 = 0.44", round((0.80 - 7 / 9) / 0.05, 2) == 0.44)

# Remark 6.10 and R1: corr^2 = sigma_v^2/(sigma_v^2+sigma_eta^2) for general parameters
for sv2, se2, a, lam, su2 in [(F(1), F(1), F(1), F(1, 2), F(1, 4)), (F(2), F(3), F(5), F(1, 3), F(7))]:
    kap, seta2, teta, tbar, ths_, thu_ = closed(sv2, se2, a, lam, su2)
    varp_ = ths_ * ths_ * (sv2 + se2) + thu_ * thu_ * su2
    cov_ = ths_ * sv2
    corr2 = cov_ * cov_ / (sv2 * varp_)
    check("L06 corr^2 identity sigma_v^2/(sigma_v^2+sigma_eta^2) on instance", corr2 == sv2 / (sv2 + seta2), str(corr2))
# P3 identity
sv2, seta2 = F(3), F(5)
check("L06 P3 identity", sv2 - sv2 * sv2 / (sv2 + seta2) == sv2 * seta2 / (sv2 + seta2) == 1 / (1 / sv2 + 1 / seta2))

print("FAILURES:", fails)
