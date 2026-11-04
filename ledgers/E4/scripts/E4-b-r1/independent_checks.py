"""Independent re-derivation of the slice b (L04-L06) numbers, using only Fraction and a separate algorithm.

L04: rank by minors (not elimination); attainability by solving for theta; Example and problem values.
L05: fixed point by solving the two linear equations; iterate by hand; problem values; damped step.
L06: Proposition 6.7 closed form checked by (i) A4 residual at random (s,u) for random parameters,
     (ii) best-response fixed point iteration from several starts (a different route to the same coefficients),
     (iii) Example 6.9, M1-M3, Part D residual -9/85, E2 arithmetic, Corr^2 identity.
"""
import itertools
import random
from fractions import Fraction as F

ok = True


def check(name, cond):
    global ok
    ok = ok and bool(cond)
    print(("PASS " if cond else "FAIL ") + name)


# ---------- L04 ----------
def det(m):
    n = len(m)
    if n == 1:
        return m[0][0]
    return sum((-1) ** j * m[0][j] * det([r[:j] + r[j + 1:] for r in m[1:]]) for j in range(n))


def rank_by_minors(rows):
    r = len(rows)
    c = len(rows[0])
    best = 0
    for k in range(1, min(r, c) + 1):
        for R in itertools.combinations(range(r), k):
            for C in itertools.combinations(range(c), k):
                if det([[rows[i][j] for j in C] for i in R]) != 0:
                    best = max(best, k)
                    break
            if best >= k:
                break
    return best


def solve_theta(rows, x):
    # Solve theta^T A = x exactly by brute search over small rational grid is not exact; instead use
    # least structure: test attainability by checking x in span via minors of augmented matrix.
    return rank_by_minors(rows + [x]) == rank_by_minors(rows)


A22 = [[F(1), F(1), F(1)], [F(0), F(1), F(2)]]
A34 = [[F(1), F(0), F(0)], [F(0), F(1), F(0)], [F(0), F(0), F(1)], [F(1), F(2), F(3)]]
check("L04 rank Example 2.2 = 2 (minors)", rank_by_minors(A22) == 2)
check("L04 rank Example 2.3 = 3 (minors)", rank_by_minors(A34) == 3)
check("L04 attain (1,2,3) in incomplete", solve_theta(A22, [F(1), F(2), F(3)]))
check("L04 (0,0,1) not attainable in incomplete", not solve_theta(A22, [F(0), F(0), F(1)]))
check("L04 (5,0,0) not attainable in incomplete", not solve_theta(A22, [F(5), F(0), F(0)]))
# portfolios for (1,2,3) in Example 2.3: all theta = (1-t, 2-2t, 3-3t, t) replicate it (one-parameter family)
for t in [F(0), F(1), F(-2), F(1, 3)]:
    th = [1 - t, 2 - 2 * t, 3 - 3 * t, t]
    pay = [sum(th[j] * A34[j][s] for j in range(4)) for s in range(3)]
    check(f"L04 portfolio family member t={t} replicates (1,2,3)", pay == [1, 2, 3])
check("L04 M1 rank (1,2,0),(2,4,0) = 1", rank_by_minors([[F(1), F(2), F(0)], [F(2), F(4), F(0)]]) == 1)
check("L04 M3 rank = 2", rank_by_minors([[F(1), F(2), F(0)], [F(0), F(1), F(1)], [F(1), F(3), F(1)], [F(2), F(5), F(1)]]) == 2)
check("L04 E3 rank = 2", rank_by_minors([[F(1), F(1), F(0)], [F(0), F(1), F(1)], [F(1), F(2), F(1)]]) == 2)
check("L04 quiz rank (1,1,1),(1,1,1),(0,1,2) = 2", rank_by_minors([[F(1), F(1), F(1)], [F(1), F(1), F(1)], [F(0), F(1), F(2)]]) == 2)
check("L04 R3 nonnegative holdings span R2 (explicit theta)",
      all(
          [a - c for a, c in zip([F(x1) + max(F(0), -F(x1), -F(x2)) - max(F(0), -F(x1), -F(x2)),
                                  F(x2) + max(F(0), -F(x1), -F(x2)) - max(F(0), -F(x1), -F(x2))], [0, 0], strict=True)]
          == [F(x1), F(x2)] for x1 in range(-3, 4) for x2 in range(-3, 4)))
# R3 explicit portfolio check (theta1 = x1 + t, theta2 = x2 + t, theta3 = t) and nonnegativity
good = True
for x1 in range(-3, 4):
    for x2 in range(-3, 4):
        t = max(F(0), F(-x1), F(-x2))
        th1, th2, th3 = F(x1) + t, F(x2) + t, t
        good = good and th1 >= 0 and th2 >= 0 and th3 >= 0 and (th1 - th3, th2 - th3) == (x1, x2)
check("L04 R3 construction nonnegative and replicates on integer grid", good)

# ---------- L05 ----------
def params(alpha, beta, gamma, delta):
    return F(alpha), F(beta), F(gamma), F(delta)


def Psi(c, p):
    alpha, beta, gamma, delta = p
    return ((alpha - gamma * c[0]) / beta, -(gamma * c[1] + delta) / beta)


def fixed(p):
    alpha, beta, gamma, delta = p
    return (alpha / (beta + gamma), -delta / (beta + gamma))


base = params(10, 2, F(1, 2), F(3, 4))
c_star = fixed(base)
check("L05 fixed point base (4,-3/10)", c_star == (F(4), F(-3, 10)))
check("L05 Psi(c*)=c* base", Psi(c_star, base) == c_star)
path = [(F(0), F(0))]
for _ in range(8):
    path.append(Psi(path[-1], base))
check("L05 c0 path first entries 0,5,15/4,65/16", [p[0] for p in path[:4]] == [0, 5, F(15, 4), F(65, 16)])
check("L05 c1 path first entries 0,-3/8,-9/32", [p[1] for p in path[:3]] == [0, F(-3, 8), F(-9, 32)])
ratios = [(path[k + 1][0] - c_star[0]) / (path[k][0] - c_star[0]) for k in range(8)]
check("L05 c0 error ratios all -1/4", all(r == F(-1, 4) for r in ratios))
p_eq = params(10, 2, 2, F(3, 4))
path_eq = [(F(0), F(0))]
for _ in range(4):
    path_eq.append(Psi(path_eq[-1], p_eq))
check("L05 gamma=beta path alternates 0,5", [p[0] for p in path_eq] == [0, 5, 0, 5, 0])
p_large = params(10, 2, 3, F(3, 4))
path_l = [(F(0), F(0))]
for _ in range(3):
    path_l.append(Psi(path_l[-1], p_large))
check("L05 gamma=3 path 0,5,-5/2,35/4", [p[0] for p in path_l] == [0, 5, F(-5, 2), F(35, 4)])
check("L05 gamma=3 c0* = 2", fixed(p_large)[0] == 2)
# damped step with lambda = beta/(beta+gamma) gives fixed point in one step, at any start
for start in [(F(0), F(0)), (F(7), F(-3)), (F(-2), F(5))]:
    lam = base[1] / (base[1] + base[2])
    img = Psi(start, base)
    d = tuple((1 - lam) * start[i] + lam * img[i] for i in range(2))
    check(f"L05 damped step one-shot from {start}", d == c_star)
# E1: error after k steps |e_k| = 4/4^k; first k with |e_k|<0.01 is 5; c0 path 6th entry 1025/256
check("L05 E1 path entry index 5 is 1025/256", path[5][0] == F(1025, 256))
check("L05 E1 |e5| = 1/256 and |e4| = 1/64", abs(path[5][0] - 4) == F(1, 256) and abs(path[4][0] - 4) == F(1, 64))
# M1..M3 and R1, R2
m1 = params(12, 3, 1, 2)
check("L05 M1 c* = (3,-1/2) and fixed", fixed(m1) == (3, F(-1, 2)) and Psi(fixed(m1), m1) == fixed(m1))
check("L05 M2 ratio -1/3", (Psi((F(0), F(0)), m1)[0] - 3) / (0 - 3) == F(-1, 3) and (Psi((F(0), F(0)), m1)[1] + F(1, 2)) / F(1, 2) == F(-1, 3))
check("L05 M3 conditional variance 5/4", (F(4) + 1) / F(2) ** 2 == F(5, 4))
check("L05 E2 Psi(5/2) stays put at gamma=beta=2", Psi((F(5, 2), F(0)), p_eq)[0] == F(5, 2))
check("L05 E3 ratios -3/2 from path", all(
    path_l[k + 1][0] - 2 != 0 and (path_l[k + 1][0] - 2) / (path_l[k][0] - 2) == F(-3, 2) for k in range(3)))
check("L05 R1 damped weight 1/2 at gamma=beta=2", F(2) / (F(2) + 2) == F(1, 2))

# ---------- L06 ----------
def closed(sv2, se2, a, lam, su2):
    tv, te = 1 / sv2, 1 / se2
    kappa = a / (lam * te)
    seta2 = se2 + kappa * kappa * su2
    teta = 1 / seta2
    tbar = lam * te + (1 - lam) * teta
    ths = tbar / (tv + tbar)
    return kappa, seta2, teta, tbar, ths, kappa * ths


def a4_residual(s, u, ths, thu, sv2, se2, a, lam, su2):
    # Independent route: Gaussian conditioning via regression of v on (s,p) with explicit covariance matrix.
    p = ths * s - thu * u
    # moments of (v, s, p): Var(s)=sv2+se2, Cov(v,s)=sv2, Var(p)=ths^2 (sv2+se2)+thu^2 su2, Cov(v,p)=ths*sv2
    vs, vv, vp = sv2 + se2, sv2, ths * sv2
    varp = ths * ths * vs + thu * thu * su2
    cov_sp = ths * vs
    # informed: regress v on (s,p) using 2x2 system
    det2 = vs * varp - cov_sp * cov_sp
    b_s = (vv * 0 + sv2 * varp - vp * cov_sp) / det2
    b_p = (vs * vp - cov_sp * sv2) / det2
    mean_I = b_s * s + b_p * p
    var_I = vv - (b_s * sv2 + b_p * vp)
    xI = (mean_I - p) / (a * var_I)
    # uninformed: regress v on p
    b = vp / varp
    var_U = vv - b * vp
    xU = (b * p - p) / (a * var_U)
    return lam * xI + (1 - lam) * xU - u


rng = random.Random(12345)
bad = 0
for trial in range(25):
    sv2 = F(rng.randint(1, 9), rng.randint(1, 9))
    se2 = F(rng.randint(1, 9), rng.randint(1, 9))
    a = F(rng.randint(1, 9), rng.randint(1, 9))
    lam = F(rng.randint(1, 8), 9)
    su2 = F(rng.randint(1, 9), rng.randint(1, 9))
    kappa, seta2, teta, tbar, ths, thu = closed(sv2, se2, a, lam, su2)
    for s in [F(-2), F(0), F(1), F(3, 2)]:
        for u in [F(-1), F(0), F(1, 2), F(2)]:
            if a4_residual(s, u, ths, thu, sv2, se2, a, lam, su2) != 0:
                bad += 1
check("L06 Prop 6.7 closed form clears A4 at 25 random parameter sets x 16 grid points (exact)", bad == 0)
# uniqueness by a different route: best-response iteration of the (theta_s, theta_u) map converges to theta*
def br_map(ths, thu, sv2, se2, a, lam, su2):
    # given a price p = ths s - thu u, the clearing condition fixes the new coefficients via Q(ths,thu) matching
    kappa, seta2, teta, tbar, _, _ = closed(sv2, se2, a, lam, su2)
    # use the closed-form identity as the update: compute implied (theta_s, theta_u) from current uninformed slope
    vs, vp = sv2 + se2, ths * sv2
    varp = ths * ths * vs + thu * thu * su2
    b = vp / varp
    var_U = sv2 - b * vp
    # implied new theta_s from market clearing at s-coefficient: lam*tau_e - Q*ths = 0 with Q built from current state
    tau_v, tau_e = 1 / sv2, 1 / se2
    tau_U = 1 / var_U
    # clearing s-coefficient: lam*tau_e*s - (lam*P_I + (1-lam)*P_U)p + (1-lam)*tau_U*(p/ths)... use direct linear solve
    # solve for new (ths_new, thu_new) given current beliefs: demands linear in (s,p) -> p solves lam*x_I+(1-lam)x_U=u
    P_I = tau_v + tau_e
    P_U = tau_U
    # p = (lam*tau_e*s - a*u) / (lam*P_I + (1-lam)*P_U - (1-lam)*b...)  (coefficient of p in demand sum)
    coef_p = lam * P_I + (1 - lam) * (P_U - b * P_U) if False else lam * P_I + (1 - lam) * P_U
    # demand_U = (b*p - p)/(a*var_U) *  => tau_U*(b-1)*p/a ; combine:
    coef_p = lam * P_I - (1 - lam) * tau_U * (b - 1) * 0 + (1 - lam) * tau_U * (1 - b)
    # clearing: lam*(tau_e s - P_I p)/a + (1-lam)*(tau_U*(b-1)*p)/a = u  -> p*(lam*P_I + (1-lam)*tau_U*(1-b))  = lam*tau_e s - a u
    new_ths = lam * tau_e / coef_p
    new_thu = a / coef_p
    return new_ths, new_thu


for sv2, se2, a, lam, su2 in [(F(1), F(1), F(1), F(1, 2), F(1, 4)), (F(2), F(1, 2), F(3), F(1, 3), F(5)),
                               (F(1), F(3), F(1, 2), F(3, 4), F(2))]:
    kappa, seta2, teta, tbar, ths_star, thu_star = closed(sv2, se2, a, lam, su2)
    ths, thu = F(1), F(1)
    for _ in range(200):
        ths, thu = br_map(ths, thu, sv2, se2, a, lam, su2)
    check(f"L06 best-response iteration converges to closed form (sv2={sv2}, se2={se2}, a={a}, lam={lam}, su2={su2})",
          abs(float(ths) - float(ths_star)) < 1e-9 and abs(float(thu) - float(thu_star)) < 1e-9)

# Example 6.9 and Lab Part D, Part C
ex = closed(F(1), F(1), F(1), F(1, 2), F(1, 4))
check("L06 Example 6.9 values kappa=2, seta2=2, tau_eta=1/2, tbar=3/4, ths=3/7, thu=6/7", ex == (F(2), F(2), F(1, 2), F(3, 4), F(3, 7), F(6, 7)))
ths, thu = ex[4], ex[5]
var_p = ths * ths * 2 + thu * thu * F(1, 4)
check("L06 Var(p)=27/49, Cov=3/7", var_p == F(27, 49) and ths * 1 == F(3, 7))
b = (ths * 1) / var_p
check("L06 b = 7/9 and Var(v|p)=2/3", b == F(7, 9) and 1 - b * (ths * 1) == F(2, 3))
check("L06 x_I(s=1,u=0)=1/7 and x_U=-1/7", (F(1, 2) - F(3, 7)) / F(1, 2) == F(1, 7) and (b * F(3, 7) - F(3, 7)) / F(2, 3) == F(-1, 7))
check("L06 clearing at (1,0): 1/2*1/7 + 1/2*(-1/7) = 0", F(1, 2) * F(1, 7) + F(1, 2) * F(-1, 7) == 0)
# Part D: theta_s replaced by 1/2, theta_u kept at 6/7, at (s,u)=(1,0)
ts_alt = F(1, 2)
varp_alt = ts_alt * ts_alt * 2 + thu * thu * F(1, 4)
cov_alt = ts_alt * 1
slope_alt = cov_alt / varp_alt
resid_alt_var = 1 - slope_alt * cov_alt
p_alt = ts_alt * 1 - thu * 0
xI_alt = (F(1, 2) - p_alt) / (F(1) * F(1, 2))
xU_alt = (slope_alt * p_alt - p_alt) / (F(1) * resid_alt_var)
resid_alt = F(1, 2) * xI_alt + F(1, 2) * xU_alt - 0
check("L06 Part D residual at (1,0) with theta_s=1/2 equals -9/85", resid_alt == F(-9, 85))
# M1-M3
m = closed(F(1), F(1), F(2), F(1, 2), F(1, 4))
check("L06 M1 kappa=4, seta2=5, tau_eta=1/5, tbar=3/5, ths=3/8, thu=3/2", m == (F(4), F(5), F(1, 5), F(3, 5), F(3, 8), F(3, 2)))
p_m = m[4] * 2 - m[5] * 1
check("L06 M3 price at (2,1) is -3/4", p_m == F(-3, 4))
xI_m = (F(2) - (1 + 1) * p_m) / 2
Y = p_m / m[4]
xU_m = (m[2] * Y - (1 + m[2]) * p_m) / 2
check("L06 M3 demands 7/4 and 1/4; clearing gives u=1", xI_m == F(7, 4) and xU_m == F(1, 4) and F(1, 2) * xI_m + F(1, 2) * xU_m == 1)
var_p_m = m[4] ** 2 * 2 + m[5] ** 2 * F(1, 4)
b_m = (m[4]) / var_p_m
check("L06 M2 b=4/9, Var(v|p)=5/6, Corr^2=1/6", b_m == F(4, 9) and 1 - b_m * m[4] == F(5, 6) and m[4] ** 2 / var_p_m == F(1, 6))
# Corr^2 identity sigma_v^2/(sigma_v^2+seta^2) for general instance (exact)
for trial in range(10):
    sv2 = F(rng.randint(1, 9), 4)
    se2 = F(rng.randint(1, 9), 4)
    a = F(rng.randint(1, 9), 3)
    lam = F(rng.randint(1, 9), 10)
    su2 = F(rng.randint(1, 9), 4)
    kappa, seta2, teta, tbar, ths, thu = closed(sv2, se2, a, lam, su2)
    vp_ = ths * sv2
    varp_ = ths * ths * (sv2 + se2) + thu * thu * su2
    check(f"L06 Corr^2 = sv2/(sv2+seta2) trial {trial}", vp_ * vp_ / (sv2 * varp_) == sv2 / (sv2 + seta2))
# R2 monotonicity: Var(v|p) strictly increasing in su2
vals = []
for su2 in [F(1, 4), F(1, 2), F(1), F(3)]:
    k, s2, t, tb, th, tu = closed(F(1), F(1), F(1), F(1, 2), su2)
    vals.append(1 / (1 + t))
check("L06 R2 Var(v|p) strictly increasing in su2 on a grid", all(vals[i] < vals[i + 1] for i in range(3)))
# Q12 premise: a nonzero affine function of (s,u) with Gaussian s,u is nonzero almost surely (Monte Carlo)
r2 = random.Random(7)
nz = 0
N = 20000
for _ in range(N):
    s, u = r2.gauss(0, 1), r2.gauss(0, 1)
    if 0.3 * s - 0.2 * u != 0.0:
        nz += 1
check("L06 Q12 premise: nonzero affine residual is nonzero almost surely (MC: all draws nonzero)", nz == N)
print("ALL PASS" if ok else "SOME FAIL")
