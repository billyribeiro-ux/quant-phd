"""Independent re-derivation for E4-b round 2 (L04-L06). Standard library only, exact Fractions.

Written from the page statements, not from the lab code. Run with: python3 -I independent_checks.py
"""

from fractions import Fraction as F
import random

FAILS: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    print(("PASS " if ok else "FAIL ") + name + (" | " + detail if detail else ""))
    if not ok:
        FAILS.append(name)


# ---------- L04: rank, attainability, redundancy ----------
def rank(rows: list[list[F]]) -> int:
    """Rank by fraction-exact row reduction, independent of the lab's implementation."""
    m = [list(r) for r in rows]
    r = 0
    cols = len(m[0])
    for c in range(cols):
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


A_INC = [[F(1), F(1), F(1)], [F(0), F(1), F(2)]]
A_COM = [[F(1), F(0), F(0)], [F(0), F(1), F(0)], [F(0), F(0), F(1)], [F(1), F(2), F(3)]]
check("L04 rank incomplete = 2", rank(A_INC) == 2)
check("L04 rank complete = 3", rank(A_COM) == 3)
for x, expect in [((1, 2, 3), True), ((0, 0, 1), False), ((5, 0, 0), False)]:
    att = rank(A_INC + [[F(v) for v in x]]) == rank(A_INC)
    check(f"L04 incomplete attain {x} == {expect}", att == expect)
for x in [(1, 2, 3), (0, 0, 1), (5, 0, 0)]:
    check(f"L04 complete attain {x} (Thm 1.4 says True)", rank(A_COM + [[F(v) for v in x]]) == rank(A_COM))
# Remark 3.2 / Example 2.3 family theta = (1-t, 2-2t, 3-3t, t) replicates (1,2,3) for every t
for t in [F(0), F(1), F(-3), F(7, 5)]:
    th = [1 - t, 2 - 2 * t, 3 - 3 * t, t]
    pay = [sum(th[j] * A_COM[j][s] for j in range(4)) for s in range(3)]
    check(f"L04 Example 2.3 family at t={t}", pay == [1, 2, 3], f"payoff {pay}")
# rank-nullity: kernel of theta -> theta^T A has dim J - rank
ker_dim = 4 - rank(A_COM)
check("L04 rank-nullity kernel dim = J - rank = 1", ker_dim == 1)
# Example 2.2 / 2.3 independence arguments
check("L04 Example 2.2 rows independent", rank(A_INC) == 2)

# ---------- L05: fixed point and iteration ----------
def cmap(c, al, be, vs, de):
    c0, c1 = c
    return ((al - vs * c0) / be, -(vs * c1 + de) / be)


def fixed(al, be, vs, de):
    return (F(al) / (be + vs), -F(de) / (be + vs))


base = (F(10), F(2), F(1, 2), F(3, 4))
c_star = fixed(*base)
check("L05 base fixed point (4,-3/10)", c_star == (4, F(-3, 10)), str(c_star))
check("L05 base residual zero", cmap(c_star, *base) == c_star)
path = [(F(0), F(0))]
for _ in range(6):
    path.append(cmap(path[-1], *base))
r0 = [(path[k + 1][0] - c_star[0]) / (path[k][0] - c_star[0]) for k in range(5)]
check("L05 base c0 error ratios -1/4", all(x == F(-1, 4) for x in r0), str([str(x) for x in r0]))
eq = (F(10), F(2), F(2), F(3, 4))
c_eq = fixed(*eq)
check("L05 equal fixed point 5/2", c_eq[0] == F(5, 2))
p = [(F(0), F(0))]
for _ in range(5):
    p.append(cmap(p[-1], *eq))
check("L05 equal path alternates 0,5", [x[0] for x in p] == [0, 5, 0, 5, 0, 5], str([str(x[0]) for x in p]))
check("L05 E2 at 5/2 stays put", cmap((F(5, 2), F(0)), *eq)[0] == F(5, 2))
lg = (F(10), F(2), F(3), F(3, 4))
c_lg = fixed(*lg)
check("L05 large fixed point 2 and -3/20", c_lg == (2, F(-3, 20)))
pl = [(F(0), F(0))]
for _ in range(6):
    pl.append(cmap(pl[-1], *lg))
check("L05 large c0 path 0,5,-5/2,35/4", [x[0] for x in pl[:4]] == [0, 5, F(-5, 2), F(35, 4)])
e = [x[0] - 2 for x in pl[:4]]
check("L05 E3 errors -2,3,-9/2,27/4", e == [-2, 3, F(-9, 2), F(27, 4)], str([str(x) for x in e]))
check("L05 E3 ratio -3/2", (e[1] / e[0]) == F(-3, 2) and (e[2] / e[1]) == F(-3, 2))
# damped step nu = beta/(beta+vs)
nu = base[1] / (base[1] + base[2])
check("L05 Prop 3.3 weight 4/5", nu == F(4, 5))
st = (F(0), F(0))
im = cmap(st, *base)
dmp = ((1 - nu) * st[0] + nu * im[0], (1 - nu) * st[1] + nu * im[1])
check("L05 damped step equals fixed point", dmp == c_star, str(dmp))
# R1 damped weight at vs=beta=2, al=10 gives c0* 5/2 after one step from 0
rr = F(2) / (F(2) + F(2))
check("L05 R1 weight 1/2 and c0*=5/2", rr == F(1, 2) and F(1, 2) * F(5) == F(5, 2))
# M1, M2
c1m = fixed(12, 3, 1, 2)
check("L05 M1 (3,-1/2)", c1m == (3, F(-1, 2)))
check("L05 M1 Psi fixes c*", cmap(c1m, 12, 3, 1, 2) == c1m)
im2 = cmap((F(0), F(0)), 12, 3, 1, 2)
check("L05 M2 Psi(0,0)=(4,-2/3)", im2 == (4, F(-2, 3)))
check("L05 M2 ratios -1/3", (im2[0] - 3) / (0 - 3) == F(-1, 3) and (im2[1] + F(1, 2)) / (0 + F(1, 2)) == F(-1, 3))
# Lemma 2.1 exact check with random affine forecasts and identity of forecast fixed point
rng = random.Random(1)
okf = True
for _ in range(200):
    al = F(rng.randint(-9, 9))
    be = F(rng.randint(1, 9))
    vs = F(rng.randint(0, 9), rng.randint(1, 5))
    de = F(rng.randint(-9, 9), rng.randint(1, 5))
    cs = fixed(al, be, vs, de)
    # forecast of price given z: E[p|z] = (al - vs*m(z) - de*z)/be at m = cs
    for z in [F(-2), F(0), F(3, 2)]:
        m = cs[0] + cs[1] * z
        if m != (al - vs * m - de * z) / be:
            okf = False
    if cmap(cs, al, be, vs, de) != cs:
        okf = False
    # uniqueness of affine fixed point: any other fixed point would solve the same linear equations
    if (be + vs) * cs[0] != al or (be + vs) * cs[1] != -de:
        okf = False
check("L05 random-parameter fixed point identities (200 draws)", okf)

# ---------- L06: Example 6.9, Prop 6.7, Cor 6.8, M1-M3 ----------
def closed(sv, se, a, lam, su):
    tv, te = 1 / sv, 1 / se
    kap = a / (lam * te)
    s_eta = se + kap * kap * su
    t_eta = 1 / s_eta
    tb = lam * te + (1 - lam) * t_eta
    ths = tb / (tv + tb)
    return dict(kappa=kap, s_eta=s_eta, t_eta=t_eta, tb=tb, ths=ths, thu=kap * ths)


ex = closed(F(1), F(1), F(1), F(1, 2), F(1, 4))
check("L06 Ex6.9 kappa=2, sig_eta2=2, tau_eta=1/2, tau_bar=3/4", (ex["kappa"], ex["s_eta"], ex["t_eta"], ex["tb"]) == (2, 2, F(1, 2), F(3, 4)))
check("L06 Ex6.9 theta_s=3/7 theta_u=6/7", (ex["ths"], ex["thu"]) == (F(3, 7), F(6, 7)))


def residual(s, u, ths, thu, sv, se, a, lam, su):
    pr = ths * s - thu * u
    var_p = ths * ths * (sv + se) + thu * thu * su
    cov = ths * sv
    b = cov / var_p
    vu = sv - b * cov
    vi = sv * se / (sv + se)
    om = sv / (sv + se)
    xi = (om * s - pr) / (a * vi)
    xu = (b * pr - pr) / (a * vu)
    return lam * xi + (1 - lam) * xu - u


sv, se, a, lam, su = F(1), F(1), F(1), F(1, 2), F(1, 4)
grid = [(F(s), F(u)) for s in (-3, -1, 0, 1, 2, 5) for u in (-2, -1, 0, F(1, 2), 1, 3)]
check("L06 equilibrium residual zero on independent 36-point grid",
      all(residual(s, u, ex["ths"], ex["thu"], sv, se, a, lam, su) == 0 for s, u in grid))
check("L06 alt slope 1/2 nonzero at (1,0)", residual(F(1), F(0), F(1, 2), ex["thu"], sv, se, a, lam, su) != 0)
r_alt = residual(F(1), F(0), F(1, 2), ex["thu"], sv, se, a, lam, su)
print("      alt residual at (1,0):", r_alt)
# Example 6.9 demands at s=1,u=0
price = F(3, 7)
xi = (F(1, 2) * 1 - price) / (1 * F(1, 2))
b = F(7, 9)
xu = (b * price - price) / (F(2, 3))
check("L06 Ex6.9 x_I=1/7 x_U=-1/7", xi == F(1, 7) and xu == F(-1, 7), f"xi={xi} xu={xu}")
check("L06 Ex6.9 clearing 1/2*(1/7)+1/2*(-1/7)=0", F(1, 2) * xi + F(1, 2) * xu == 0)
# b and V_U from closed form
b_cf = ex["t_eta"] / (ex["ths"] * (1 + ex["t_eta"]))
check("L06 slope b closed form = 7/9", b_cf == F(7, 9), str(b_cf))
check("L06 V_U = 2/3", 1 / (1 + ex["t_eta"]) == F(2, 3))
# hypothesis figure: slope of v on p from moments
var_p = F(3, 7) ** 2 * 2 + F(6, 7) ** 2 * F(1, 4)
check("L06 Var(p)=27/49", var_p == F(27, 49))
check("L06 Cov(v,p)=3/7", F(3, 7) * 1 == F(3, 7))
check("L06 rho^2 = 1/3", (F(3, 7)) ** 2 / var_p == F(1, 3))
# M1: a=2, lam 1/2, su 1/4 => kappa 4, s_eta 5, tau_eta 1/5, tau_bar 3/5, ths 3/8, thu 3/2
m1 = closed(F(1), F(1), F(2), F(1, 2), F(1, 4))
check("L06 M1 values", (m1["kappa"], m1["s_eta"], m1["t_eta"], m1["tb"], m1["ths"], m1["thu"]) == (4, 5, F(1, 5), F(3, 5), F(3, 8), F(3, 2)))
vp = F(9, 64) * 2 + F(9, 4) * F(1, 4)
cov = F(3, 8)
bb = cov / vp
check("L06 M2 Var(p)=27/32, b=4/9, Var(v|p)=5/6, rho^2=1/6",
      vp == F(27, 32) and bb == F(4, 9) and 1 - bb * cov == F(5, 6) and cov * cov / (1 * vp) == F(1, 6))
# M3 at (s,u)=(2,1)
pm3 = F(3, 8) * 2 - F(3, 2) * 1
xi3 = (2 - 2 * pm3) / 2  # tau_e s - (tau_v+tau_e) p over a, tau=1
Y = pm3 / F(3, 8)
xu3 = (F(1, 5) * Y - F(6, 5) * pm3) / 2
check("L06 M3 price -3/4, x_I 7/4, x_U 1/4, clears to u=1",
      pm3 == F(-3, 4) and xi3 == F(7, 4) and xu3 == F(1, 4) and F(1, 2) * xi3 + F(1, 2) * xu3 == 1)
# Corollary 6.8: E[v|p] coefficient and Var(v|p) equal Prop 6.7 step-2 formula
ok8 = True
for _ in range(100):
    sv_ = F(rng.randint(1, 9), rng.randint(1, 5))
    se_ = F(rng.randint(1, 9), rng.randint(1, 5))
    a_ = F(rng.randint(1, 9), rng.randint(1, 5))
    lam_ = F(rng.randint(1, 9), 10)
    su_ = F(rng.randint(1, 9), rng.randint(1, 5))
    c = closed(sv_, se_, a_, lam_, su_)
    tv_ = 1 / sv_
    # Corollary 6.8 variance = 1/(tau_v+tau_eta) = sv*se_eta/(sv+se_eta)
    v_cor = 1 / (tv_ + c["t_eta"])
    v_alt = sv_ * c["s_eta"] / (sv_ + c["s_eta"])
    if v_cor != v_alt:
        ok8 = False
    # rho^2 at equilibrium: Corr(v,p)^2 = sv/(sv+s_eta) (as in R1/M2)
    vp_ = c["ths"] ** 2 * (sv_ + se_) + c["thu"] ** 2 * su_
    cov_ = c["ths"] * sv_
    if cov_ * cov_ / (sv_ * vp_) != sv_ / (sv_ + c["s_eta"]):
        ok8 = False
    # residual zero at random pairs for random parameters
    for _k in range(3):
        s_ = F(rng.randint(-5, 5))
        u_ = F(rng.randint(-5, 5))
        if residual(s_, u_, c["ths"], c["thu"], sv_, se_, a_, lam_, su_) != 0:
            ok8 = False
check("L06 Prop 6.7 closed form clears and Cor 6.8 identities (100 random params)", ok8)

# R1 limit: lambda small -> kappa large, theta_s small (numeric monotone check)
prev = None
mono = True
for lam_v in [F(1, 2), F(1, 5), F(1, 20), F(1, 100), F(1, 1000)]:
    c = closed(F(1), F(1), F(1), lam_v, F(1, 4))
    if prev is not None and not (c["ths"] < prev["ths"] and c["kappa"] > prev["kappa"]):
        mono = False
    prev = c
check("L06 R1 kappa increases and theta_s decreases as lambda falls", mono)

# Assumption G usage: Var(p) > 0 for (theta_s,theta_u) != 0 under A1 (sigma_u^2>0)
check("L06 Var(p)>0 when theta=(0,1) and sigma_u^2=1/4", (F(0) * F(0) * 2 + F(1) * F(1, 4)) > 0)

# Units check of L06 docstring: kappa = a sig_e2 / lam has units (1/P)(P/Q)^2 = P/Q^2
# (here by exponents: a has exponent -1 in P, sig_e2 exponent +2 in P and -2 in Q, lam dimensionless)
exp_P = -1 + 2
exp_Q = -2
check("L06 units: kappa exponents P^1 Q^-2 (docstring claims P^1 Q^-1 )", (exp_P, exp_Q) == (1, -2), "docstring wrong by one power of Q")

print("FAILS:", FAILS)
