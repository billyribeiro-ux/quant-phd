# ruff: noqa: B905, N806, N817, RUF005
"""Slice e (round 2) independent re-derivation of the numbers the E4 cards quote.

Written from the closed forms in the lesson text, not by importing the lab twins.
Usage: python -I indep_checks.py   (stdlib only; prints one line per check, exits 1 on any mismatch)
"""

from __future__ import annotations

import itertools
import math
import sys
from fractions import Fraction as F

FAILS: list[str] = []


def check(label: str, got: object, want: object) -> None:
    ok = got == want
    print(f"{'OK  ' if ok else 'FAIL'} {label}: got {got} want {want}")
    if not ok:
        FAILS.append(label)


def near(label: str, got: float, want: float, tol: float) -> None:
    ok = abs(got - want) <= tol
    print(f"{'OK  ' if ok else 'FAIL'} {label}: got {got:.9f} want {want:.9f} tol {tol}")
    if not ok:
        FAILS.append(label)


# ---- L01: Example 1.5 and Lab 1 numbers (card c011 to c013)
pi1 = (F(1, 8), F(3, 8), F(3, 8), F(1, 8))
q1 = (F(1, 2), F(1, 3), F(1, 4), F(1, 5))
x1 = (F(100), F(40), F(0), F(250))
y1 = (F(0), F(60), F(120), F(30))


def val(x: tuple, q: tuple) -> F:
    return sum((a * b for a, b in zip(x, q)), F(0))


check("L01 value of claim", val(x1, q1), F(340, 3))
check("L01 value of other", val(y1, q1), F(56))
comb = tuple(2 * a - F(1, 2) * b for a, b in zip(x1, y1))
check("L01 combined payoff", comb, (F(200), F(50), F(-60), F(485)))
check("L01 linearity", val(comb, q1), 2 * val(x1, q1) - F(1, 2) * val(y1, q1))
check("L01 expected payoff", val(x1, pi1), F(235, 4))

# ---- L02: Example 2.11 (cards c031 to c038)
pi2 = (F(1, 2), F(1, 4), F(1, 4))
e1, e2 = (F(3), F(4), F(1)), (F(1), F(4), F(3))
ebar = tuple(a + b for a, b in zip(e1, e2))
check("L02 aggregate", ebar, (F(4), F(8), F(4)))
qs = tuple(p / e for p, e in zip(pi2, ebar))
check("L02 prices", qs, (F(1, 8), F(1, 32), F(1, 16)))
w1 = sum(a * b for a, b in zip(qs, e1))
w2 = sum(a * b for a, b in zip(qs, e2))
check("L02 wealth agent 1 (card c038)", w1, F(9, 16))
check("L02 wealth agent 2", w2, F(7, 16))
d1 = tuple(p * w1 / q for p, q in zip(pi2, qs))
d2 = tuple(p * w2 / q for p, q in zip(pi2, qs))
check("L02 demand agent 1", d1, (F(9, 4), F(9, 2), F(9, 4)))
check("L02 demand agent 2", d2, (F(7, 4), F(7, 2), F(7, 4)))
check("L02 clearing", tuple(a + b for a, b in zip(d1, d2)), ebar)
check("L02 ratio agent 1 (card c034)", tuple(p / (x * q) for p, x, q in zip(pi2, d1, qs)), (F(16, 9),) * 3)
check("L02 ratio agent 2", tuple(p / (x * q) for p, x, q in zip(pi2, d2, qs)), (F(16, 7),) * 3)
check("L02 z=(1,-1,0) value (card c037)", F(1) * qs[0] - F(1) * qs[1], F(3, 32))
check("L02 endowment cost (card c038)", val(e1, qs), F(9, 16))
# scaling by 3 with wealth re-valued (card c035)
qs3 = tuple(3 * q for q in qs)
w1s = sum(a * b for a, b in zip(qs3, e1))
check("L02 scaled demand unchanged", tuple(p * w1s / q for p, q in zip(pi2, qs3)), d1)


# ---- L03: MRS and Example 3.6 (cards c046, c047, c051)
def mrs(x: tuple, s: int, t: int) -> F:
    return (pi2[s] / x[s]) / (pi2[t] / x[t])


check("L03 MRS agent 1, states 1-2", mrs(d1, 0, 1), F(4))
check("L03 MRS agent 1, states 1-3", mrs(d1, 0, 2), F(2))
check("L03 MRS agent 1, states 2-3", mrs(d1, 1, 2), F(1, 2))
check("L03 MRS agent 2, states 1-2", mrs(d2, 0, 1), F(4))
check("L03 price ratio q1/q2", qs[0] / qs[1], F(4))
check("L03 price ratio q1/q3", qs[0] / qs[2], F(2))
check("L03 price ratio q2/q3", qs[1] / qs[2], F(1, 2))


def util(x: tuple) -> float:
    return sum(p * math.log(xi) for p, xi in zip(pi2, x))


# L03 Part B: brute force over the 125 grid allocations (card c048)
grid = (0.0, 0.25, 0.5, 0.75, 1.0)
u1_end = util(tuple(float(v) for v in e1))
u2_end = util(tuple(float(v) for v in e2))
u1_eq = util(tuple(float(v) for v in d1))
u2_eq = util(tuple(float(v) for v in d2))
eb = [float(v) for v in ebar]


def count_improvements(u1_ref: float, u2_ref: float) -> tuple[int, int]:
    total = 0
    improvements = 0
    for f in itertools.product(grid, repeat=3):
        total += 1
        b1 = [f[s] * eb[s] for s in range(3)]
        b2 = [(1 - f[s]) * eb[s] for s in range(3)]
        if min(b1) <= 0 or min(b2) <= 0:
            continue  # log is -infinity at zero, never an improvement over a finite reference
        v1, v2 = util(tuple(b1)), util(tuple(b2))
        if v1 >= u1_ref - 1e-12 and v2 >= u2_ref - 1e-12 and (v1 > u1_ref + 1e-12 or v2 > u2_ref + 1e-12):
            improvements += 1
    return total, improvements


tot, imp_end = count_improvements(u1_end, u2_end)
check("L03 grid allocations (card c048)", tot, 125)
check("L03 Pareto improvements of endowment on grid (card c048)", imp_end, 2)
tot, imp_eq = count_improvements(u1_eq, u2_eq)
check("L03 Pareto improvements of equilibrium on grid (card c048)", imp_eq, 0)


# ---- L04: rank facts (cards c062 to c065)
def rank(rows: list[list[F]]) -> int:
    m = [list(r) for r in rows]
    r = 0
    ncols = len(m[0])
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


A2 = [[F(1), F(1), F(1)], [F(0), F(1), F(2)]]
check("L04 rank Example 2.2 (card c062)", rank(A2), 2)
check("L04 augmented rank (1,2,3) (card c065)", rank(A2 + [[F(1), F(2), F(3)]]), 2)
check("L04 augmented rank (0,0,1) (card c065)", rank(A2 + [[F(0), F(0), F(1)]]), 3)
check("L04 augmented rank (5,0,0) (card c065)", rank(A2 + [[F(5), F(0), F(0)]]), 3)
A4 = [[F(1), F(0), F(0)], [F(0), F(1), F(0)], [F(0), F(0), F(1)], [F(1), F(2), F(3)]]
check("L04 rank Example 2.3 (card c064)", rank(A4), 3)
check("L04 misconception 2 rank (card c071)", rank([[F(1), F(1), F(1)], [F(1), F(1), F(1)], [F(0), F(1), F(2)]]), 2)


# ---- L05: fixed points and error ratios (cards c090 to c094)
def run_map(alpha, beta, vs, delta, steps, start=(F(0), F(0))):
    c = start
    path = [c]
    for _ in range(steps):
        c = ((alpha - vs * c[0]) / beta, -(vs * c[1] + delta) / beta)
        path.append(c)
    return path


for label, (al, be, vs, de), steps in (
    ("base", (F(10), F(2), F(1, 2), F(3, 4)), 8),
    ("equal", (F(10), F(2), F(2), F(3, 4)), 6),
    ("large", (F(10), F(2), F(3), F(3, 4)), 6),
):
    fp = (al / (be + vs), -de / (be + vs))
    path = run_map(al, be, vs, de, steps)
    c0p = [p[0] for p in path]
    print(f"     L05 {label} c0 path {[str(x) for x in c0p]}")
    if label == "base":
        check("L05 base c0 path head (card c091)", [str(x) for x in c0p[:4]], ["0", "5", "15/4", "65/16"])
        check("L05 base fixed point (card c090)", fp, (F(4), F(-3, 10)))
        ratios = [(c0p[k + 1] - fp[0]) / (c0p[k] - fp[0]) for k in range(7)]
        check("L05 base error ratio (card c091)", set(ratios), {F(-1, 4)})
    if label == "equal":
        check("L05 equal fixed point (card c092)", fp, (F(5, 2), F(-3, 16)))
        check("L05 equal path (card c092)", [str(x) for x in c0p[:4]], ["0", "5", "0", "5"])
    if label == "large":
        check("L05 large fixed point c0 (card c093)", fp[0], F(2))
        check("L05 large path head (card c093)", [str(x) for x in c0p[:4]], ["0", "5", "-5/2", "35/4"])
        ratios = [(c0p[k + 1] - fp[0]) / (c0p[k] - fp[0]) for k in range(5)]
        check("L05 large error ratio (card c093)", set(ratios), {F(-3, 2)})
# damped step, card c094
be, vs, al, de = F(2), F(1, 2), F(10), F(3, 4)
nu = be / (be + vs)
check("L05 damped weight (card c094)", nu, F(4, 5))
c = (F(0), F(0))
img = ((al - vs * c[0]) / be, -(vs * c[1] + de) / be)
dmp = ((1 - nu) * c[0] + nu * img[0], (1 - nu) * c[1] + nu * img[1])
check("L05 damped step (card c094)", dmp, (F(4), F(-3, 10)))

# ---- L06: base instance (cards c118 to c123, c126, c129)
sv, se, a, lam, su = F(1), F(1), F(1), F(1, 2), F(1, 4)
tv, te = 1 / sv, 1 / se
kap = a / (lam * te)
sig_eta2 = se + kap * kap * su
tau_eta = 1 / sig_eta2
tau_bar = lam * te + (1 - lam) * tau_eta
th_s = tau_bar / (tv + tau_bar)
th_u = kap * th_s
check("L06 kappa", kap, F(2))
check("L06 sigma_eta2 (card c126)", sig_eta2, F(2))
check("L06 theta_s (card c118)", th_s, F(3, 7))
check("L06 theta_u (card c118)", th_u, F(6, 7))
var_p = th_s**2 * (sv + se) + th_u**2 * su
cov_vp = th_s * sv
b = cov_vp / var_p
check("L06 slope v on p (card c119)", b, F(7, 9))
check("L06 posterior variance (card c119)", sv - b * cov_vp, F(2, 3))
check("L06 V_I (card c_none)", sv * se / (sv + se), F(1, 2))


def resid(s: F, u: F, ts: F) -> F:
    p = ts * s - th_u * u
    vp = ts**2 * (sv + se) + th_u**2 * su
    cv = ts * sv
    bb = cv / vp
    rv = sv - bb * cv
    vi = sv * se / (sv + se)
    xi = (sv * s / (sv + se) - p) / (a * vi)
    xu = (bb * p - p) / (a * rv)
    return lam * xi + (1 - lam) * xu - u


check(
    "L06 informed demand at (1,0) (card c120)",
    (sv * F(1) / (sv + se) - th_s * F(1)) / (a * sv * se / (sv + se)),
    F(1, 7),
)
check("L06 residual at (1,0) with slope 1/2 (cards c123)", resid(F(1), F(0), F(1, 2)), F(-9, 85))
check("L06 residual at base (card c122)", resid(F(1), F(0), th_s), F(0))
grid_pts = [(F(s), F(u)) for s in (-1, 0, 1, 2) for u in (-1, 0, 1, 2)]
check("L06 residual zero on 16 points (card c122)", all(resid(s, u, th_s) == 0 for s, u in grid_pts), True)


# ---- L07: sweeps (cards c142 to c145, c143 Var(p))
def informativeness(sigu: F, lamb: F, aa: F) -> tuple[F, F]:
    k = aa * se / lamb
    seta = se + k * k * sigu * sigu
    teta = 1 / seta
    tb = lamb * te + (1 - lamb) * teta
    ts = tb / (tv + tb)
    tu = k * ts
    varp = ts * ts * (sv + se) + tu * tu * sigu * sigu
    rho2 = sv / (sv + seta)
    return rho2, varp


for sd, want_r, want_v in (
    (F(1, 4), F(4, 9), F(729, 1444)),
    (F(1, 2), F(1, 3), F(27, 49)),
    (F(1), F(1, 6), F(27, 32)),
    (F(2), F(1, 18), F(729, 338)),
    (F(4), F(1, 66), F(35937, 4802)),
):
    r2, vp = informativeness(sd, F(1, 2), F(1))
    check(f"L07 rho2 at sd {sd} (card c142)", r2, want_r)
    check(f"L07 Var(p) at sd {sd} (card c143)", vp, want_v)
for lamb, want in ((F(1, 4), F(1, 6)), (F(1, 2), F(1, 3)), (F(3, 4), F(9, 22))):
    check(f"L07 rho2 at lam {lamb} (card c144)", informativeness(F(1, 2), lamb, F(1))[0], want)
for aa, want in ((F(1, 2), F(4, 9)), (F(1), F(1, 3)), (F(2), F(1, 6))):
    check(f"L07 rho2 at a {aa} (card c145)", informativeness(F(1, 2), F(1, 2), aa)[0], want)
check("L07 Part A rho2 (card c141)", informativeness(F(1, 2), F(1, 2), F(1))[0], F(1, 3))


# ---- L08: Example 1.1 gains and the cost-0.15 root (cards c180 to c184)
def gain_terms(lamb: float, aa: float, vv: float, ee: float, uu: float) -> tuple[float, float, float, float]:
    tv_, te_ = 1 / vv, 1 / ee
    kap_ = aa * ee / lamb
    teta = 1 / (ee + kap_ * kap_ * uu)
    A = lamb * te_ + (1 - lamb) * teta
    beta = A / (tv_ + A)
    bs = vv / (vv + ee)
    by = teta / (tv_ + teta)
    VI = 1 / (tv_ + te_)
    VU = 1 / (tv_ + teta)
    varDI = (bs - beta) ** 2 * (vv + ee) + kap_ * kap_ * beta * beta * uu
    varDU = (by - beta) ** 2 * (vv + ee + kap_ * kap_ * uu)
    gain = (1 / (2 * aa)) * math.log((1 + varDI / VI) / (1 + varDU / VU))
    corr2 = teta / (tv_ + teta)
    return gain, corr2, beta, by


g1, _, _, _ = gain_terms(1.0, 2.0, 1.0, 1.0, 1.0)
near("L08 G(1) = ln(5/3)/4 (card c180)", g1, math.log(5 / 3) / 4, 1e-12)
near("L08 G(1) printed 0.127706 (card c180)", round(g1, 6), 0.127706, 1e-12)
near("L08 G(0) = ln2/4 (card c180)", math.log(2) / 4, 0.173287, 5e-7)
g05, _, beta05, by05 = gain_terms(0.5, 2.0, 1.0, 1.0, 1.0)
near("L08 Part A slope formula b_y/beta at lam 0.5 (card c181)", by05 / beta05, 0.1605, 5e-5)
_, c_star_corr, _, _ = gain_terms(0.657828572, 2.0, 1.0, 1.0, 1.0)
near("L08 N at lam* for cost 0.15 (card c182)", gain_terms(0.657828572, 2.0, 1.0, 1.0, 1.0)[0] - 0.15, 0.0, 2e-8)
near("L08 Corr^2 at lam* (card c182)", c_star_corr, 0.088941, 5e-7)
near("L08 Corr^2 at lam=1 (card c183)", gain_terms(1.0, 2.0, 1.0, 1.0, 1.0)[1], 1 / 6, 1e-12)
near("L08 Corr^2 at lam 0.231615819 (card c187)", gain_terms(0.231615819, 2.0, 1.0, 1.0, 1.0)[1], 0.013061, 5e-7)
near("L08 Corr^2 at lam 0.5 = 1/18 (lesson quiz)", gain_terms(0.5, 2.0, 1.0, 1.0, 1.0)[1], 1 / 18, 1e-12)
near("L08 boundary gap at cost 0.12 (card c183)", g1 - 0.12, 0.007706, 1e-6)
near("L08 boundary gap at cost 0.18 (card c183)", math.log(2) / 4 - 0.18, -0.006713, 1e-6)

# ---- L09: bets on six states (cards c200, c201, c202, c203)
P1 = [{1, 2}, {3}, {4, 5, 6}]
P2 = [{1, 2, 3}, {4, 5}, {6}]
states = range(1, 7)
vals = (-2, -1, 0, 1, 2)
strict_both_s1 = 0
for xs in itertools.product(vals, repeat=6):
    x = dict(zip(states, xs))
    g1_1 = sum(x[w] for w in (1, 2)) / 2
    g2_1 = -sum(x[w] for w in (1, 2, 3)) / 3
    if g1_1 > 0 and g2_1 > 0:
        strict_both_s1 += 1
check("L09 total bets (card c204)", len(vals) ** 6, 15625)
check("L09 strictly positive for both at state 1 (card c201)", strict_both_s1, 500)
zero_set = sum(1 for xs in itertools.product(vals, repeat=6) if xs[2] == 0 and xs[1] == -xs[0])
check("L09 zero-posterior bets (card c203)", zero_set, 625)
# recount nonneg on meet directly
cnt = 0
bad_nonzero = 0
for xs in itertools.product(vals, repeat=6):
    x = dict(zip(states, xs))
    meet = {1, 2, 3}
    g1_m = [sum(x[w] for w in cell) / len(cell) for cell in P1 if cell <= meet]
    g2_m = [-sum(x[w] for w in cell) / len(cell) for cell in P2 if cell <= meet]
    if all(v >= 0 for v in g1_m + g2_m):
        cnt += 1
        if any(v != 0 for v in g1_m + g2_m):
            bad_nonzero += 1
check("L09 nonnegative on meet count (card c202)", cnt, 625)
check("L09 nonnegative on meet with nonzero posterior (card c202)", bad_nonzero, 0)
# two priors (card c211) over several p, r
ok_two = True
for p, r in ((F(7, 10), F(2, 5)), (F(1, 5), F(3, 4)), (F(1, 3), F(1, 2)), (F(9, 10), F(1, 10))):
    if p > r:
        pp, rr, flip = p, r, False
    else:
        pp, rr, flip = 1 - p, 1 - r, True
    th = (pp + rr) / 2
    t = th / (1 - th)
    recv1 = pp - (1 - pp) * t
    recv2 = -rr + (1 - rr) * t
    if not (recv1 > 0 and recv2 > 0):
        ok_two = False
    print(f"     L09 two-prior check p={p} r={r} flip={flip} recv1={recv1} recv2={recv2}")
check("L09 two-prior bet strictly positive (card c211)", ok_two, True)
# card c205 numbers
check("L09 trader1 receipt (card c205)", F(7, 10) * 1 + F(3, 10) * (-1), F(2, 5))
check("L09 trader2 receipt of -x (card c205)", F(4, 10) * (-1) + F(6, 10) * 1, F(1, 5))

print("FAILS:", len(FAILS), FAILS)
sys.exit(1 if FAILS else 0)
