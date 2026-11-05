"""Round 10, slice E4-c: independent numerical check of the L06 price, the L07 closed forms and the L08 gains and roots.

Nothing here imports the lab twins. The equilibrium price is found by solving the market-clearing residual numerically
(Newton on the two residuals at (s, u) = (1, 0) and (0, 1)); the uninformed posterior is taken from the sample covariance
structure of (v, p) (Fact 2.3), not from the tau formulas; the gains use Var(D_I), Var(D_U), V_I and V_U computed from
covariances; the bisection is a different implementation with tolerance 1e-13 on lambda.
"""
import math
import random

def clear_residual(th_s, th_u, prm, s, u):
    sv2, se2, a, lam, su2 = prm["sv2"], prm["se2"], prm["a"], prm["lam"], prm["su2"]
    p = th_s * s - th_u * u
    # informed: E[v|s], Var(v|s) from Fact 2.3
    m_s = sv2 / (sv2 + se2) * s
    V_I = sv2 * se2 / (sv2 + se2)
    x_I = (m_s - p) / (a * V_I)
    # uninformed: Fact 2.3 applied to (v, p) with zero means
    cov_vp = th_s * sv2
    var_p = th_s * th_s * (sv2 + se2) + th_u * th_u * su2
    b = cov_vp / var_p
    V_U = sv2 - cov_vp * cov_vp / var_p
    x_U = (b * p - p) / (a * V_U)
    return lam * x_I + (1 - lam) * x_U - u

def solve_price(prm):
    th = [0.5, 0.5]
    for _ in range(100):
        F = [clear_residual(th[0], th[1], prm, 1.0, 0.0), clear_residual(th[0], th[1], prm, 0.0, 1.0)]
        h = 1e-7
        J = [[0.0, 0.0], [0.0, 0.0]]
        for j in range(2):
            t2 = list(th); t2[j] += h
            F2 = [clear_residual(t2[0], t2[1], prm, 1.0, 0.0), clear_residual(t2[0], t2[1], prm, 0.0, 1.0)]
            for i in range(2):
                J[i][j] = (F2[i] - F[i]) / h
        det = J[0][0] * J[1][1] - J[0][1] * J[1][0]
        d0 = (J[1][1] * F[0] - J[0][1] * F[1]) / det
        d1 = (-J[1][0] * F[0] + J[0][0] * F[1]) / det
        th = [th[0] - d0, th[1] - d1]
        if abs(d0) + abs(d1) < 1e-14:
            break
    return th

def closed_form(prm):
    sv2, se2, a, lam, su2 = prm["sv2"], prm["se2"], prm["a"], prm["lam"], prm["su2"]
    kappa = a * se2 / lam
    se_eta2 = se2 + kappa * kappa * su2
    tau_bar = lam / se2 + (1 - lam) / se_eta2
    th_s = tau_bar / (1 / sv2 + tau_bar)
    return th_s, kappa * th_s, kappa, se_eta2

def check_price(prm):
    th = solve_price(prm)
    cf = closed_form(prm)
    worst = 0.0
    rng = random.Random(1)
    for _ in range(400):
        s, u = rng.uniform(-3, 3), rng.uniform(-3, 3)
        worst = max(worst, abs(clear_residual(th[0], th[1], prm, s, u)))
    return th, cf, worst

# L07 base and an alternative parameter set
BASE7 = {"sv2": 1.0, "se2": 1.0, "a": 1.0, "lam": 0.5, "su2": 0.25}
ALT = {"sv2": 1.2, "se2": 0.64, "a": 2.0, "lam": 0.3, "su2": 2.25}
for name, prm in (("L07 base", BASE7), ("alt", ALT)):
    th, cf, worst = check_price(prm)
    print(f"{name}: numeric theta_s {th[0]:.12f} theta_u {th[1]:.12f} | closed form {cf[0]:.12f} {cf[1]:.12f} | max |residual| on 400 (s,u) {worst:.2e}")

# L07 rho^2 from moments and the closed form along the sweeps (exact closed forms recomputed here)
def rho2_numeric(prm):
    th = solve_price(prm)
    sv2, se2, su2 = prm["sv2"], prm["se2"], prm["su2"]
    cov_vp = th[0] * sv2
    var_p = th[0] ** 2 * (sv2 + se2) + th[1] ** 2 * su2
    return cov_vp ** 2 / (sv2 * var_p), var_p

print("L07 sweep sd (numeric rho2, var_p):")
for sd in (0.25, 0.5, 1.0, 2.0, 4.0):
    prm = dict(BASE7, su2=sd * sd)
    r, vp = rho2_numeric(prm)
    print(f"  sd {sd}: rho2 {r:.9f} var_p {vp:.9f}")
for lam in (0.25, 0.5, 0.75):
    r, _ = rho2_numeric(dict(BASE7, lam=lam)); print(f"  lam {lam}: rho2 {r:.9f}")
for a in (0.5, 1.0, 2.0):
    r, _ = rho2_numeric(dict(BASE7, a=a)); print(f"  a {a}: rho2 {r:.9f}")
r, _ = rho2_numeric(dict(BASE7, su2=1e-4)); print(f"  sd 0.01 (su2 1e-4): rho2 {r:.9f} benchmark {1/2:.9f}")

# L07 Part F: replicate the seeded draw exactly as the lab does (seed 7, 20000 draws, theta from numeric solve)
th = solve_price(BASE7)
rng = random.Random(7)
vs, ps = [], []
for _ in range(20000):
    v = rng.gauss(0.0, 1.0); eps = rng.gauss(0.0, 1.0); u = rng.gauss(0.0, 0.5)
    vs.append(v); ps.append(th[0] * (v + eps) - th[1] * u)
n = len(vs); mv = sum(vs) / n; mp = sum(ps) / n
cov = sum((x - mv) * (y - mp) for x, y in zip(vs, ps)); vv = sum((x - mv) ** 2 for x in vs); vp = sum((y - mp) ** 2 for y in ps)
print(f"L07 Part F recomputed sample rho2 {cov * cov / (vv * vp):.6f} vs population {1/3:.6f}")

# L08: gains from covariance-based moments (v bar = 0, Example 1.1: a=2, sv2=se2=su2=1)
def gain_numeric(lam, prm):
    prm = dict(prm, lam=lam)
    th = solve_price(prm) if lam > 0 else None
    sv2, se2, a, su2 = prm["sv2"], prm["se2"], prm["a"], prm["su2"]
    # beta and clearing coefficients of the price: p = th_s * s - th_u * u
    th_s, th_u = th
    # informed: D_I = E[v|s] - p, variance from covariance of (s, u)
    b_s = sv2 / (sv2 + se2)
    varD_I = (b_s * 1.0 - th_s) ** 2 * (sv2 + se2) + th_u ** 2 * su2
    V_I = sv2 * se2 / (sv2 + se2)
    # uninformed: D_U = E[v|p] - p, Var from Fact 2.3 on (v, p)
    var_p = th_s ** 2 * (sv2 + se2) + th_u ** 2 * su2
    cov_vp = th_s * sv2
    bU = cov_vp / var_p
    varD_U = (bU - 1.0) ** 2 * var_p
    V_U = sv2 - cov_vp ** 2 / var_p
    g = math.log((1 + varD_I / V_I) / (1 + varD_U / V_U)) / (2 * a)
    corr2 = cov_vp ** 2 / (sv2 * var_p)
    return g, corr2

EX = {"sv2": 1.0, "se2": 1.0, "a": 2.0, "lam": 1.0, "su2": 1.0}
g1, _ = gain_numeric(1.0, EX)
print(f"L08 numeric G(1) = {g1:.9f} closed ln(5/3)/4 = {math.log(5/3)/4:.9f}")
g0 = math.log(2) / 4
print(f"L08 G(0) closed ln2/4 = {g0:.9f}")
g05, _ = gain_numeric(0.5, EX)
print(f"L08 numeric G(0.5) = {g05:.9f} (lab prints 0.158997)")
# lambda -> 0 limit check of the numeric gain (small lambda)
for lam in (1e-3, 1e-5):
    gl, _ = gain_numeric(lam, EX)
    print(f"L08 numeric G({lam}) = {gl:.9f}, minus G(0) = {gl - g0:.3e}")
# no-noise check at 0.15 on a 999 grid: all gains 0 (sigma_u^2 = 0)
EXN = dict(EX, su2=0.0)
mx = 0.0
for k in range(1, 1000):
    gk, _ = gain_numeric(k / 1000, EXN)
    mx = max(mx, abs(gk))
print(f"L08 sigma_u^2=0 numeric max |G| on 999 grid {mx:.3e}; G(0)={math.log(2)/4:.6f}")

# L08 Part C: bisection on N(lam) = G(lam) - cost, own implementation, tolerance 1e-13 on lambda
def G(lam):
    return gain_numeric(lam, EX)[0]

def root(cost):
    if cost >= math.log(2) / 4:
        return 0.0, math.log(2) / 4 - cost
    if cost <= G(1.0):
        return 1.0, G(1.0) - cost
    lo, hi = 1e-12, 1.0
    while hi - lo > 1e-13:
        mid = (lo + hi) / 2
        if G(mid) - cost > 0:
            lo = mid
        else:
            hi = mid
    lam = (lo + hi) / 2
    return lam, G(lam) - cost

for c in (0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18):
    lam, gap = root(c)
    print(f"cost {c:.2f}: lam* {lam:.9f} gap {gap:.2e}")
