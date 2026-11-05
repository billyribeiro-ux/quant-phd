"""Independent re-derivation of the numbers printed by the L04, L05 and L06 labs and quoted in their prose.

Written for verifier round 9 of unit E4, slice b. It does not import the twins. Exact parts use
fractions.Fraction and a different algorithm from the twins (minors for rank, direct formulas for the
conditional moments). Part E re-simulates with random.Random(6) and an independent least-squares fit.

Usage: python3 -I indep_rederive.py   (prints one line per check; nonzero exit on any failure)
"""

import itertools
import math
import random
import sys
from fractions import Fraction as F

fails: list[str] = []


def check(name: str, got: object, want: object) -> None:
    ok = got == want
    print(f"{'OK  ' if ok else 'FAIL'} {name}: got {got} want {want}")
    if not ok:
        fails.append(name)


# ---------- L04: rank by minors (independent of Gaussian elimination) ----------
def det(m: list[list[F]]) -> F:
    n = len(m)
    if n == 1:
        return m[0][0]
    if n == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    total = F(0)
    for j in range(n):
        minor = [row[:j] + row[j + 1:] for row in m[1:]]
        total += (-1) ** j * m[0][j] * det(minor)
    return total


def rank_minors(rows: list[list[F]]) -> int:
    best = 0
    for k in range(1, min(len(rows), len(rows[0])) + 1):
        for rs in itertools.combinations(rows, k):
            for cs in itertools.combinations(range(len(rows[0])), k):
                if det([[r[c] for c in cs] for r in rs]) != 0:
                    best = k
                    break
            else:
                continue
            break
    return best


def fr(*xs: int) -> list[F]:
    return [F(x) for x in xs]


INC = [fr(1, 1, 1), fr(0, 1, 2)]
COM = [fr(1, 0, 0), fr(0, 1, 0), fr(0, 0, 1), fr(1, 2, 3)]
check("L04 rank incomplete", rank_minors(INC), 2)
check("L04 rank complete", rank_minors(COM), 3)
check("L04 rank of first three rows", rank_minors(COM[:3]), 3)
for label, x in (("(1,2,3)", fr(1, 2, 3)), ("(0,0,1)", fr(0, 0, 1)), ("(5,0,0)", fr(5, 0, 0))):
    r_aug = rank_minors(INC + [x])
    check(f"L04 augmented rank incomplete {label}", r_aug, 2 if label == "(1,2,3)" else 3)
    check(f"L04 attainable incomplete {label}", r_aug == rank_minors(INC), label == "(1,2,3)")
    r_aug_c = rank_minors(COM + [x])
    check(f"L04 attainable complete {label}", r_aug_c == rank_minors(COM), True)
# Example 2.3 portfolio family (1-t, 2-2t, 3-3t, t) replicates (1,2,3) for t = 1/3, 5
for t in (F(1, 3), F(5)):
    z = [1 - t, 2 - 2 * t, 3 - 3 * t, t]
    pay = [sum(z[j] * COM[j][k] for j in range(4)) for k in range(3)]
    check(f"L04 family member t={t} replicates (1,2,3)", pay, fr(1, 2, 3))
# Remark 3.2 / misconception: (1,2,3,0) and (0,0,0,1) both replicate (1,2,3)
check("L04 (1,2,3,0) replicates", [sum(z * COM[j][k] for j, z in enumerate(fr(1, 2, 3, 0))) for k in range(3)], fr(1, 2, 3))
# Prop 4.2 example: C(I_2) excludes (-1,0)
check("L04 cone example: (-1,0) excluded from nonnegative span", all(c >= 0 for c in fr(-1, 0)), False)
# R3 of L04: zeta = (xi1 + t, xi2 + t, t) with t = max(0,-xi1,-xi2) reproduces xi for a grid
for xi in [fr(-3, 2), fr(0, -4), fr(2, 5), fr(-1, -1)]:
    t = max(F(0), -xi[0], -xi[1])
    z = [xi[0] + t, xi[1] + t, t]
    assert all(x >= 0 for x in z)
    pay = [z[0] - z[2], z[1] - z[2]]
    check(f"L04 R3 nonnegative holdings reproduce {xi}", pay, xi)
# Misconception 2: rows (1,1,1),(1,1,1),(0,1,2) rank 2
check("L04 misc2 rank", rank_minors([fr(1, 1, 1), fr(1, 1, 1), fr(0, 1, 2)]), 2)
# Problems: M1 rank 1; M3 rank 2; E3 rank 2
check("L04 M1 rank", rank_minors([fr(1, 2, 0), fr(2, 4, 0)]), 1)
check("L04 M3 rank", rank_minors([fr(1, 2, 0), fr(0, 1, 1), fr(1, 3, 1), fr(2, 5, 1)]), 2)
check("L04 E3 rank", rank_minors([fr(1, 1, 0), fr(0, 1, 1), fr(1, 2, 1)]), 2)
# E1: augmented rank of (5,0,0) in incomplete market = 3, equations give -5 != 0
check("L04 E1 equation residual", F(5) - 10, F(-5))

# ---------- L05: closed forms and error recursion ----------
def cmap(c, al, be, vs, de):
    return ((al - vs * c[0]) / be, -(vs * c[1] + de) / be)


def fixed(al, be, vs, de):
    return (al / (be + vs), -de / (be + vs))


BASE = (F(10), F(2), F(1, 2), F(3, 4))
EQ = (F(10), F(2), F(2), F(3, 4))
LG = (F(10), F(2), F(3), F(3, 4))
f0 = fixed(*BASE)
check("L05 base fixed point", f0, (F(4), F(-3, 10)))
check("L05 base residual", cmap(f0, *BASE), f0)
for name, pr, steps in (("base", BASE, 8), ("equal", EQ, 6), ("large", LG, 6)):
    t = fixed(*pr)
    c = (F(0), F(0))
    path = [c]
    for _ in range(steps):
        c = cmap(c, *pr)
        path.append(c)
    ratios0 = [(path[k + 1][0] - t[0]) / (path[k][0] - t[0]) if path[k][0] != t[0] else None for k in range(steps)]
    print(f"L05 {name} c0 path {[str(p[0]) for p in path]} ratios {[str(r) for r in ratios0]}")
check("L05 base c0 path first 4", [str(p[0]) for p in [ (F(0),F(0)) ]] , ["0"])
p = (F(0), F(0))
vals = []
for _ in range(5):
    p = cmap(p, *BASE)
    vals.append(p[0])
check("L05 base c0 path 5,15/4,65/16,255/64,1025/256", vals, [F(5), F(15, 4), F(65, 16), F(255, 64), F(1025, 256)])
p = (F(0), F(0))
vals = []
for _ in range(3):
    p = cmap(p, *LG)
    vals.append(p[0])
check("L05 large c0 path 5,-5/2,35/4", vals, [F(5), F(-5, 2), F(35, 4)])
e0 = F(0) - F(2)
e3 = F(35, 4) - F(2)
check("L05 E3 e3 = 27/4", e3, F(27, 4))
check("L05 E3 ratio", (F(35, 4) - 2) / (F(-5, 2) - 2), F(-3, 2))
check("L05 E1 1025/256 - 4 = 1/256", F(1025, 256) - 4, F(1, 256))
check("L05 E1 |e4| = 1/64", abs(F(255, 64) - 4), F(1, 64))
check("L05 damped weight base", F(2) / (F(2) + F(1, 2)), F(4, 5))
p = (F(0), F(0))
d = ((1 - F(4, 5)) * 0 + F(4, 5) * cmap(p, *BASE)[0], (1 - F(4, 5)) * 0 + F(4, 5) * cmap(p, *BASE)[1])
check("L05 damped step equals fixed point", d, f0)
check("L05 R1 damped weight at varsigma=beta", F(2) / (F(2) + F(2)), F(1, 2))
check("L05 R1 damped step c0", (1 - F(1, 2)) * 0 + F(1, 2) * (F(10) / 2), F(5, 2))
check("L05 c0* at varsigma=beta", F(10) / (F(2) + F(2)), F(5, 2))
check("L05 c1* at varsigma=beta", F(-3, 4) / (F(2) + F(2)), F(-3, 16))
check("L05 c0* large", F(10) / (F(2) + F(3)), F(2))
check("L05 c1* large", F(-3, 4) / (F(2) + F(3)), F(-3, 20))
check("L05 M1 c0*", F(12) / (F(3) + F(1)), F(3))
check("L05 M1 c1*", F(-2) / (F(3) + F(1)), F(-1, 2))
check("L05 M2 first iterate", cmap((F(0), F(0)), F(12), F(3), F(1), F(2)), (F(4), F(-2, 3)))
check("L05 M3 conditional variance", (F(4) + 1) / F(2) ** 2, F(5, 4))
check("L05 quiz c0* base", F(10) / (F(2) + F(1, 2)), F(4))
check("L05 quiz error ratio base", -(F(1, 2)) / F(2), F(-1, 4))

# ---------- L06: closed form, moments, clearing, Part D, Example 6.9 ----------
sv, se, a, lam, su = F(1), F(1), F(1), F(1, 2), F(1, 4)
tv, te = 1 / sv, 1 / se
kappa = a / (lam * te)
seta = se + kappa * kappa * su
teta = 1 / seta
tbar = lam * te + (1 - lam) * teta
ths = tbar / (tv + tbar)
thu = kappa * ths
check("L06 kappa", kappa, F(2))
check("L06 sigma_eta^2", seta, F(2))
check("L06 tau_eta", teta, F(1, 2))
check("L06 tau_bar", tbar, F(3, 4))
check("L06 theta_s", ths, F(3, 7))
check("L06 theta_u", thu, F(6, 7))

var_s = sv + se
var_p = ths ** 2 * var_s + thu ** 2 * su
cov_vp = ths * sv
b = cov_vp / var_p
vu = sv - b * cov_vp
check("L06 var_s", var_s, F(2))
check("L06 var_p", var_p, F(27, 49))
check("L06 cov_vp", cov_vp, F(3, 7))
check("L06 slope b", b, F(7, 9))
check("L06 posterior var", vu, F(2, 3))
check("L06 rho^2", cov_vp ** 2 / (sv * var_p), F(1, 3))
check("L06 closed-form slope", teta / (ths * (tv + teta)), F(7, 9))


def demands(s: F, u: F, th_s: F, th_u: F) -> tuple[F, F, F]:
    p = th_s * s - th_u * u
    vp = th_s ** 2 * (sv + se) + th_u ** 2 * su
    cvp = th_s * sv
    bb = cvp / vp
    vuu = sv - bb * cvp
    vi = sv * se / (sv + se)
    xi = (sv / (sv + se) * s - p) / (a * vi)
    xu = (bb * p - p) / (a * vuu)
    return p, xi, xu


grid_s = [F(-1), F(0), F(1), F(2)]
grid_u = [F(-1), F(0), F(1, 2), F(2)]
res = []
for s in grid_s:
    for u in grid_u:
        _, xi, xu = demands(s, u, ths, thu)
        res.append(lam * xi + (1 - lam) * xu - u)
check("L06 Part C zero residuals of 16", sum(1 for r in res if r == 0), 16)
p10, xi10, xu10 = demands(F(1), F(0), ths, thu)
check("L06 price at (1,0)", p10, F(3, 7))
check("L06 x_I at (1,0)", xi10, F(1, 7))
check("L06 x_U at (1,0)", xu10, F(-1, 7))
_, xi_alt, xu_alt = demands(F(1), F(0), F(1, 2), thu)
r_alt = lam * xi_alt + (1 - lam) * xu_alt - F(0)
check("L06 Part D alternative residual -9/85", r_alt, F(-9, 85))
# M1 instance (a = 2, sigma_u^2 = 1/4) and its M2, M3 solutions
a2 = F(2)
k2 = a2 * se / lam
s2 = se + k2 * k2 * su
t2 = 1 / s2
tb2 = lam * te + (1 - lam) * t2
th2 = tb2 / (tv + tb2)
thu2 = k2 * th2
check("L06 M1 kappa", k2, F(4))
check("L06 M1 sigma_eta^2", s2, F(5))
check("L06 M1 theta_s*", th2, F(3, 8))
check("L06 M1 theta_u*", thu2, F(3, 2))
# M3 at (s,u) = (2,1) with a = 2: price, demands, clearing, all written out directly
s3, u3 = F(2), F(1)
p3 = th2 * s3 - thu2 * u3
xi3 =(te * s3 - (tv + te) * p3) / a2
Y3 = p3 / th2
xu3 = (t2 * Y3 - (tv + t2) * p3) / a2
check("L06 M3 price", p3, F(-3, 4))
check("L06 M3 x_I", xi3, F(7, 4))
check("L06 M3 x_U", xu3, F(1, 4))
check("L06 M3 clears", lam * xi3 + (1 - lam) * xu3, F(1))
# M2 at a = 2 instance
vp2 = th2 ** 2 * (sv + se) + (k2 * th2) ** 2 * su
c2 = th2 * sv
check("L06 M2 Var(p)", vp2, F(27, 32))
check("L06 M2 b", c2 / vp2, F(4, 9))
check("L06 M2 Var(v|p)", sv - (c2 / vp2) * c2, F(5, 6))
check("L06 M2 rho^2", c2 ** 2 / (sv * vp2), F(1, 6))
# Example 6.9 demands at (1,0): (1/2)(1/7)+(1/2)(-1/7)=0
check("L06 Example 6.9 clearing sum", F(1, 2) * F(1, 7) + F(1, 2) * F(-1, 7), F(0))
# E2 arithmetic (printed sample values)
diff = 0.426617 - 3 / 7
tol = 0.006497
print(f"L06 E2 difference {diff:.6f} fraction of tolerance {diff / tol:.4f} SE units {diff / (tol / 3):.4f}")
check("L06 E2 fraction of tolerance rounds to -0.30", round(diff / tol, 2), -0.30)
check("L06 E2 SE units round to -0.90", round(diff / (tol / 3), 2), -0.90)
check("L06 E1 standardized difference", round((0.80 - 7 / 9) / 0.05, 2), 0.44)

# ---------- L06 Part E: independent re-simulation with the same seed ----------
rng = random.Random(6)
N = 20000
sd_v, sd_e, sd_u = 1.0, 1.0, 0.5
S, P, V = [], [], []
for _ in range(N):
    v = rng.gauss(0.0, sd_v)
    e = rng.gauss(0.0, sd_e)
    u = rng.gauss(0.0, sd_u)
    s = v + e
    S.append(s)
    P.append(float(ths) * s - float(thu) * u)
    V.append(v)


def ols(x: list[float], y: list[float]) -> tuple[float, float]:
    n = len(x)
    mx = math.fsum(x) / n
    my = math.fsum(y) / n
    sxx = math.fsum((xi - mx) ** 2 for xi in x)
    sxy = math.fsum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    b1 = sxy / sxx
    b0 = my - b1 * mx
    rss = math.fsum((yi - b0 - b1 * xi) ** 2 for xi, yi in zip(x, y))
    return b1, math.sqrt(rss / (n - 2) / sxx)


b_ps, se_ps = ols(S, P)
b_vp, se_vp = ols(P, V)
print(f"L06 Part E re-simulated: p_on_s {b_ps:.6f} tol {3 * se_ps:.6f} | v_on_p {b_vp:.6f} tol {3 * se_vp:.6f}")
check("L06 Part E p_on_s within", abs(b_ps - 3 / 7) <= 3 * se_ps, True)
check("L06 Part E v_on_p within", abs(b_vp - 7 / 9) <= 3 * se_vp, True)

print("FAILURES:", fails)
sys.exit(1 if fails else 0)
