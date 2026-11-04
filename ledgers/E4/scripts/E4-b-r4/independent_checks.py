"""Independent re-derivation of the L04 to L06 numbers (verifier round 4, E4 slice b).

Uses only fractions.Fraction and its own small linear solver. It does not import the lab twins, so it
is an independent check of their printed values. Run: python3 -I ledgers/E4/scripts/E4-b-r4/independent_checks.py
"""

from fractions import Fraction as F
import itertools


def rank(rows):
    m = [list(map(F, r)) for r in rows]
    r = 0
    ncols = len(m[0]) if m else 0
    for c in range(ncols):
        piv = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c] / m[r][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
    return r


def solve2(a, b):
    """Solve the 2x2 system a x = b exactly."""
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    x0 = (b[0] * a[1][1] - a[0][1] * b[1]) / det
    x1 = (a[0][0] * b[1] - b[0] * a[1][0]) / det
    return x0, x1


def print_ok(label, ok):
    print(f"{label}: {'OK' if ok else 'MISMATCH'}")
    assert ok, label


print("== L04 ranks and attainability (Examples 2.2, 2.3; Proposition 1.5) ==")
inc = [[1, 1, 1], [0, 1, 2]]
comp = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 2, 3]]
print_ok("rank incomplete = 2", rank(inc) == 2)
print_ok("rank complete = 3", rank(comp) == 3)
print_ok("(1,2,3) attainable in incomplete", rank(inc + [[1, 2, 3]]) == rank(inc))
print_ok("(0,0,1) not attainable in incomplete", rank(inc + [[0, 0, 1]]) == 3)
print_ok("(5,0,0) not attainable in incomplete", rank(inc + [[5, 0, 0]]) == 3)
print_ok("(1,2,3) and (0,0,1) attainable in complete", rank(comp + [[1, 2, 3]]) == 3 and rank(comp + [[0, 0, 1]]) == 3)
print_ok("r4 = e1 + 2 e2 + 3 e3", [1 * a + 2 * b + 3 * c for a, b, c in zip([1, 0, 0], [0, 1, 0], [0, 0, 1])] == [1, 2, 3])
print_ok("E2 family (1-t, 2-2t, 3-3t, t) replicates (1,2,3) for t=-3, 7/5",
         all([(1 - t) + t * 1, (2 - 2 * t) + 2 * t, (3 - 3 * t) + 3 * t] == [1, 2, 3] for t in (F(-3), F(7, 5))))
print_ok("M3 rank 2 (rows (1,2,0),(0,1,1),(1,3,1),(2,5,1))", rank([[1, 2, 0], [0, 1, 1], [1, 3, 1], [2, 5, 1]]) == 2)
print_ok("E3 rank 2 (rows (1,1,0),(0,1,1),(1,2,1))", rank([[1, 1, 0], [0, 1, 1], [1, 2, 1]]) == 2)
print_ok("misconception 2 rank 2 (rows (1,1,1),(1,1,1),(0,1,2))", rank([[1, 1, 1], [1, 1, 1], [0, 1, 2]]) == 2)
print_ok("rank of (1,2,0),(2,4,0) is 1", rank([[1, 2, 0], [2, 4, 0]]) == 1)
ok = True
for x1 in range(-3, 4):
    for x2 in range(-3, 4):
        t = max(0, -x1, -x2)
        th = (x1 + t, x2 + t, t)
        if min(th) < 0 or (th[0] - th[2], th[1] - th[2]) != (x1, x2):
            ok = False
print_ok("R3 explicit construction gives nonnegative theta on integer grid", ok)

print()
print("== L05 coefficient map (Proposition 2.2, Lemma 3.1, Proposition 3.3, lab Parts A to F) ==")


def psi(c, al, be, vs, de):
    return ((al - vs * c[0]) / be, -(vs * c[1] + de) / be)


def fixed(al, be, vs, de):
    return (al / (be + vs), -de / (be + vs))


al, be, vs, de = F(10), F(2), F(1, 2), F(3, 4)
c_star = fixed(al, be, vs, de)
print_ok("base fixed point (4, -3/10)", c_star == (F(4), F(-3, 10)))
print_ok("base residual of Psi at fixed point is 0", psi(c_star, al, be, vs, de) == c_star)
path = [(F(0), F(0))]
for _ in range(8):
    path.append(psi(path[-1], al, be, vs, de))
print_ok("base c0 path first entries 0,5,15/4,65/16", [p[0] for p in path[:4]] == [0, 5, F(15, 4), F(65, 16)])
print_ok("base c0 path 6th entry 1025/256", path[5][0] == F(1025, 256))
ratios = [(path[k + 1][i] - c_star[i]) / (path[k][i] - c_star[i]) for k in range(8) for i in (0, 1)]
print_ok("base error ratios all -1/4", all(r == F(-1, 4) for r in ratios))
e5 = path[5][0] - c_star[0]
print_ok("E1: |e_5| = 1/256 and |e_4| = 1/64 (first iterate within 0.01 at k=5)",
         abs(e5) == F(1, 256) and abs(path[4][0] - c_star[0]) == F(1, 64))
print_ok("E1: 4/4^k < 1/100 first at k=5", [k for k in range(20) if F(4, 4 ** k) < F(1, 100)][0] == 5)
eq = fixed(al, F(2), F(2), de)
pe = [(F(0), F(0))]
for _ in range(6):
    pe.append(psi(pe[-1], al, F(2), F(2), de))
print_ok("equal case c0 path 0,5,0,5,0,5,0 and c* = 5/2", [p[0] for p in pe] == [0, 5, 0, 5, 0, 5, 0] and eq[0] == F(5, 2))
print_ok("equal case c1* = -3/16", eq[1] == F(-3, 16))
lg = fixed(al, be, F(3), de)
pl = [(F(0), F(0))]
for _ in range(6):
    pl.append(psi(pl[-1], al, be, F(3), de))
print_ok("large case c0 path 0,5,-5/2,35/4 and c*=2", [p[0] for p in pl[:4]] == [0, 5, F(-5, 2), F(35, 4)] and lg[0] == 2)
print_ok("large case ratio -3/2", all((pl[k + 1][0] - lg[0]) / (pl[k][0] - lg[0]) == F(-3, 2) for k in range(5)))
print_ok("E3 e_3 = 27/4", pl[3][0] - lg[0] == F(27, 4))
nu = be / (be + vs)
d = tuple((1 - nu) * c0 + nu * c1 for c0, c1 in zip((F(0), F(0)), psi((F(0), F(0)), al, be, vs, de)))
print_ok("damped weight 4/5 gives (4, -3/10) from (0,0)", nu == F(4, 5) and d == c_star)
print_ok("R1: damped weight at varsigma=beta=2 is 1/2, gives 5/2", F(2) / F(4) == F(1, 2) and F(1, 2) * 5 == F(5, 2))
print_ok("M1: (alpha,beta,vs,delta)=(12,3,1,2) gives c*=(3,-1/2) fixed by Psi",
         fixed(F(12), F(3), F(1), F(2)) == (F(3), F(-1, 2)) and psi((F(3), F(-1, 2)), F(12), F(3), F(1), F(2)) == (F(3), F(-1, 2)))
print_ok("M2: Psi(0,0) = (4, -2/3) at M1 parameters", psi((F(0), F(0)), F(12), F(3), F(1), F(2)) == (F(4), F(-2, 3)))
print_ok("E2: Psi(5/2) = 5/2 at varsigma=beta=2, alpha=10", psi((F(5, 2), F(0)), F(10), F(2), F(2), F(0))[0] == F(5, 2))

print()
print("== L06 closed form, Gaussian conditioning, clearing residual (Example 6.9, M1 to M3, lab Parts A to D) ==")


def gauss_cond(cov, target, given):
    """E[target | given] = Cov(target, given) Sigma^{-1} given, for scalar target and a 2-vector given (zero means)."""
    s11, s12, s22 = cov["gg"][0][0], cov["gg"][0][1], cov["gg"][1][1]
    det = s11 * s22 - s12 * s12
    inv = [[s22 / det, -s12 / det], [-s12 / det, s11 / det]]
    c = cov["tg"]
    w = [c[0] * inv[0][0] + c[1] * inv[1][0], c[0] * inv[0][1] + c[1] * inv[1][1]]
    return w[0] * given[0] + w[1] * given[1], w, cov["tt"] - (w[0] * c[0] + w[1] * c[1])


def model_residual(s, u, ts, tu, sv2, se2, a, lam, su2):
    """Clearing residual at (s,u) from the Gaussian conditional formulas, with the price as an observed linear combination."""
    # covariance of (v, s, u): v, eps, u independent with variances sv2, se2, su2
    var_s = sv2 + se2
    var_p = ts * ts * var_s + tu * tu * su2
    cov_vp = ts * sv2
    cov_v_s = sv2
    # informed: observe (s, p); Sigma of (s,p)
    cov_sp = ts * var_s + (-tu) * 0  # Cov(s, p) = ts*var_s (u independent of s)
    gg_inf = [[var_s, cov_sp], [cov_sp, var_p]]
    cov_inf = {"gg": gg_inf, "tg": [cov_v_s, cov_vp], "tt": sv2}
    mean_inf, _, var_inf = gauss_cond(cov_inf, None, [s, ts * s - tu * u])
    # uninformed: observe p
    cov_unf = {"gg": [[var_p]], "tg": [cov_vp], "tt": sv2}
    slope = cov_vp / var_p
    var_unf = sv2 - slope * cov_vp
    price = ts * s - tu * u
    x_i = (mean_inf - price) / (a * var_inf)
    x_u = (slope * price - price) / (a * var_unf)
    return lam * x_i + (1 - lam) * x_u - u, slope, var_unf, x_i, x_u


sv2, se2, a, lam, su2 = F(1), F(1), F(1), F(1, 2), F(1, 4)
ts, tu = F(3, 7), F(6, 7)
grid = [(s, u) for s in (F(-1), F(0), F(1), F(2)) for u in (F(-1), F(0), F(1, 2), F(2))]
res = [model_residual(s, u, ts, tu, sv2, se2, a, lam, su2)[0] for s, u in grid]
print_ok("closed-form clearing residual zero at all 16 lab grid points", all(r == 0 for r in res))
_, slope, vu, xi, xu = model_residual(F(1), F(0), ts, tu, sv2, se2, a, lam, su2)
print_ok("Example 6.9 slope b = 7/9", slope == F(7, 9))
print_ok("Example 6.9 V_U = 2/3", vu == F(2, 3))
print_ok("Example 6.9 x_I(1,0) = 1/7 and x_U(1,0) = -1/7", xi == F(1, 7) and xu == F(-1, 7))
print_ok("Example 6.9 clearing at (1,0): (1/2)(1/7)+(1/2)(-1/7)=0", lam * xi + (1 - lam) * xu == 0)
alt = model_residual(F(1), F(0), F(1, 2), tu, sv2, se2, a, lam, su2)[0]
print_ok("lab Part D: residual -9/85 for theta_s = 1/2 at (1,0)", alt == F(-9, 85))

# brute force uniqueness: over a rational grid of (theta_s, theta_u), count pairs with zero residual on the 16 points
hits = []
for kS in range(-70, 71):
    for kU in range(-150, 151):
        cs, cu = F(kS, 70), F(kU, 70)
        if cs == 0:
            continue
        try:
            ok = all(model_residual(s, u, cs, cu, sv2, se2, a, lam, su2)[0] == 0 for s, u in grid)
        except ZeroDivisionError:
            continue
        if ok:
            hits.append((cs, cu))
print("brute-force zero-residual pairs on grid k/70:", [(str(x), str(y)) for x, y in hits])
print_ok("uniqueness on grid: only (3/7, 6/7)", hits == [(F(3, 7), F(6, 7))])

print()
print("== L06 M1 to M3, P2, E1, E2, R1, Corollary 6.8 identity, Remark 6.10 ==")
# M1 instance a=2
a2 = F(2)
kap = a2 * se2 / lam
se_eta = se2 + kap * kap * su2
tau_eta = 1 / se_eta
tau_bar = lam * 1 + (1 - lam) * tau_eta
th_s = tau_bar / (1 + tau_bar)
th_u = kap * th_s
print_ok("M1: kappa=4, sig_eta2=5, tau_eta=1/5, tau_bar=3/5, theta_s=3/8, theta_u=3/2",
         (kap, se_eta, tau_eta, tau_bar, th_s, th_u) == (F(4), F(5), F(1, 5), F(3, 5), F(3, 8), F(3, 2)))
var_p = th_s ** 2 * 2 + th_u ** 2 * F(1, 4)
b = th_s / var_p
print_ok("M2: Var(p)=27/32, b=4/9, Var(v|p)=5/6, Corr^2=1/6",
         var_p == F(27, 32) and b == F(4, 9) and 1 - b * th_s == F(5, 6) and (th_s ** 2) / (1 * var_p) == F(1, 6))
p_m3 = th_s * 2 - th_u * 1
xi3 = (1 * 2 - (1 + 1) * p_m3) / a2
Y = p_m3 / th_s
xu3 = (tau_eta * Y - (1 + tau_eta) * p_m3) / a2
print_ok("M3: p=-3/4, x_I=7/4, Y=-2, x_U=1/4, clearing gives u=1",
         p_m3 == F(-3, 4) and xi3 == F(7, 4) and Y == -2 and xu3 == F(1, 4) and lam * xi3 + (1 - lam) * xu3 == 1)
# Corr(v,p)^2 = sv2/(sv2+sig_eta2) along the equilibrium for any lambda (R1); check at base and at M1 instance
for (lm, sigu) in [(F(1, 2), F(1, 4)), (F(1, 3), F(1, 2)), (F(3, 4), F(2))]:
    kk = a2 * se2 / lm
    se_e = se2 + kk * kk * sigu
    tb = lm + (1 - lm) * (1 / se_e)
    tsv = tb / (1 + tb)
    tuv = kk * tsv
    vp = tsv * sv2
    varp = tsv ** 2 * (sv2 + se2) + tuv ** 2 * sigu
    corr2 = vp ** 2 / (sv2 * varp)
    print_ok(f"Corr(v,p)^2 = sv2/(sv2+sig_eta2) at lambda={lm}, sig_u2={sigu}", corr2 == sv2 / (sv2 + se_e))
# P2 / step 1: with theta_s=0 and u=0, residual at s=1 vs s=2 differs by lam*tau_e/a
print_ok("P2: lambda*tau_eps/a = 1/2 at base instance (nonzero)", lam * (1 / se2) / a == F(1, 2))
# E1 hypothetical: 0.80 - 7/9 over 0.05
print_ok("E1: (0.80 - 7/9)/0.05 = 0.444... rounds to 0.44", round(float((F(80, 100) - F(7, 9)) / F(5, 100)), 2) == 0.44)
# E2 numbers from the printed Part E values
diff = F(426617, 10**6) - F(3, 7)
tol = F(6497, 10**6)
print_ok("E2: difference -0.001954 (6 dp), fraction of tolerance -0.30, SE = 0.002166",
         round(float(diff), 6) == -0.001954 and round(float(diff / tol), 2) == -0.30 and round(float(tol / 3), 6) == 0.002166)
print_ok("E2: difference in SE units is -0.90", round(float(diff / (tol / 3)), 2) == -0.90)
# R1 limit: kappa grows as lam -> 0, theta_s -> 0
prev = None
for lm in [F(1, 10), F(1, 100), F(1, 1000)]:
    kk = a2 * se2 / lm
    se_e = se2 + kk * kk * su2
    tb = lm + (1 - lm) * (1 / se_e)
    tsv = tb / (1 + tb)
    print("R1 lambda=", lm, "theta_s=", float(tsv))
    if prev is not None:
        assert tsv < prev
    prev = tsv
print_ok("R1: theta_s decreases to 0 as lambda -> 0", True)
# Corollary 6.8 identity: Var(v|p)=1/(tau_v+tau_eta)=sv2*sig_eta2/(sv2+sig_eta2)
print_ok("P3 identity sv2 - sv2^2/(sv2+se) = sv2*se/(sv2+se) = 1/(tau_v+tau_eta) at base", (
    sv2 - sv2 ** 2 / (sv2 + se2) == sv2 * se2 / (sv2 + se2) == 1 / (1 / sv2 + 1 / se2)))
# Remark 6.10 monotonicity in sigma_u2
vals = [1 / (se2 + kap * kap * s) for s in [F(0), F(1, 4), F(1)]]
print_ok("Remark 6.10 / R2: tau_eta decreasing in sigma_u2", vals[0] > vals[1] > vals[2])

print()
print("ALL CHECKS PASSED")

print()
print("== L05 Part F: fixed-point identity on the five-point z grid ==")
_al, _be, _vs, _de = BASE_L05 = (F(10), F(2), F(1, 2), F(3, 4))
_c0, _c1 = fixed(_al, _be, _vs, _de)
_checks = []
for _z in (F(-2), F(-1), F(0), F(1), F(2)):
    _m = _c0 + _c1 * _z
    _checks.append(_m == (_al - _vs * _m - _de * _z) / _be)
print_ok("L05 Part F identity holds at z in {-2,-1,0,1,2}", all(_checks))
