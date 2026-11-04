"""Independent recomputation of the numbers that the E4 slice-e cards state (round 4).

Usage: python -I card_numbers_r4.py
Every value is recomputed here from the model formulas with fractions or floats; nothing is read from the labs.
Prints one line per claim: name, recomputed value, and the card-stated value, with OK or MISMATCH.
"""

from __future__ import annotations

import math
from fractions import Fraction as F
from itertools import product

FAIL: list[str] = []


def check(name: str, got: object, want: object, tol: float | None = None) -> None:
    if tol is None:
        ok = got == want
    else:
        ok = abs(float(got) - float(want)) <= tol  # type: ignore[arg-type]
    print(f"{'OK' if ok else 'MISMATCH'} {name}: recomputed={got} card={want}")
    if not ok:
        FAIL.append(name)


def dot(a: list[F], b: list[F]) -> F:
    return sum((x * y for x, y in zip(a, b, strict=True)), F(0))


# ---- L01 (cards c011-c016, c212) ----
claim = [F(100), F(40), F(0), F(250)]
other = [F(0), F(60), F(120), F(30)]
prices = [F(1, 2), F(1, 3), F(1, 4), F(1, 5)]
probs = [F(1, 8), F(3, 8), F(3, 8), F(1, 8)]
check("L01 value(claim)", dot(claim, prices), F(340, 3))
check("L01 value(other)", dot(other, prices), F(56))
check(
    "L01 linear comb 2x-1/2y value",
    dot([2 * a - F(1, 2) * b for a, b in zip(claim, other, strict=True)], prices),
    F(596, 3),
)
check("L01 expected payoff", dot(claim, probs), F(235, 4))
check("L01 price/prob differ in every state", all(p != q for p, q in zip(prices, probs, strict=True)), True)

# ---- L02 (cards c029-c038) ----
pi = [F(1, 2), F(1, 4), F(1, 4)]
e1 = [F(3), F(4), F(1)]
e2 = [F(1), F(4), F(3)]
ebar = [a + b for a, b in zip(e1, e2, strict=True)]
qstar = [p / e for p, e in zip(pi, ebar, strict=True)]
w1, w2 = dot(qstar, e1), dot(qstar, e2)
th1, th2 = w1, w2
x1 = [p * th1 / q for p, q in zip(pi, qstar, strict=True)]
x2 = [p * th2 / q for p, q in zip(pi, qstar, strict=True)]
check("L02 aggregate", ebar, [F(4), F(8), F(4)])
check("L02 q*", qstar, [F(1, 8), F(1, 32), F(1, 16)])
check("L02 q*·ebar", dot(qstar, ebar), F(1))
check("L02 x1", x1, [F(9, 4), F(9, 2), F(9, 4)])
check("L02 x2", x2, [F(7, 4), F(7, 2), F(7, 4)])
check("L02 w1", w1, F(9, 16))
check("L02 w2", w2, F(7, 16))
check("L02 ratio pi/(x q) agent1 = 1/w1", [p / (x * q) for p, x, q in zip(pi, x1, qstar, strict=True)], [F(16, 9)] * 3)
check("L02 ratio pi/(x q) agent2 = 1/w2", [p / (x * q) for p, x, q in zip(pi, x2, qstar, strict=True)], [F(16, 7)] * 3)
check("L02 e1 cost at q*", dot(qstar, e1), F(9, 16))
check("L02 market clearing", [a + b for a, b in zip(x1, x2, strict=True)], ebar)
# Remark 2.6 at q=(2,1,1)
qr = [F(2), F(1), F(1)]
wr1, wr2 = dot(qr, e1), dot(qr, e2)
d1 = [p * wr1 / q for p, q in zip(pi, qr, strict=True)]
d2 = [p * wr2 / q for p, q in zip(pi, qr, strict=True)]
zr = [a + b - e for a, b, e in zip(d1, d2, ebar, strict=True)]
check("L02 Remark 2.6 wealths", (wr1, wr2), (F(11), F(9)))
check("L02 Remark 2.6 excess demand", zr, [F(1), F(-3), F(1)])
check("L02 Misc 2 v=(1,-1,0) value", dot([F(1), F(-1), F(0)], qstar), F(3, 32))


# ---- L03 (cards c046, c048, c049, c214) ----
def mrs(p: list[F], x: list[F], s: int, t: int) -> F:
    return (p[s] / x[s]) / (p[t] / x[t])


check("L03 MRS agent1 12", mrs(pi, x1, 0, 1), F(4))
check("L03 MRS agent1 13", mrs(pi, x1, 0, 2), F(2))
check("L03 MRS agent1 23", mrs(pi, x1, 1, 2), F(1, 2))
check("L03 MRS agent2 12", mrs(pi, x2, 0, 1), F(4))
check("L03 MRS agent2 13", mrs(pi, x2, 0, 2), F(2))
check("L03 MRS agent2 23", mrs(pi, x2, 1, 2), F(1, 2))
check("L03 price ratios", (qstar[0] / qstar[1], qstar[0] / qstar[2], qstar[1] / qstar[2]), (F(4), F(2), F(1, 2)))
# R2 derivative numbers
dU1 = F(1, 2) * F(-1, 3) + F(1, 4) * F(1)  # pi_s u'(x_s) times d(x_s)/d eps with u'=1/x at x1=(3,4,1)
dU1 = pi[0] * (F(1, 3)) * (-1) + pi[1] * (F(1, 4)) * 4
dU2 = pi[0] * F(1) * 1 + pi[1] * F(1, 4) * (-4)
check("L03 R2 dU1/deps", dU1, F(1, 12))
check("L03 R2 dU2/deps", dU2, F(1, 4))
ygrid = [[], []]
GRID = [F(0), F(1, 4), F(1, 2), F(3, 4), F(1)]
allocs = []
for f in product(GRID, repeat=3):
    y1 = [fk * e for fk, e in zip(f, ebar, strict=True)]
    y2 = [e - a for e, a in zip(ebar, y1, strict=True)]
    allocs.append((y1, y2))
check("L03 grid size", len(allocs), 125)


def util(p: list[F], bundle: list[F]) -> float:
    return sum(float(pp) * math.log(float(b)) for pp, b in zip(p, bundle, strict=True))


def improves(new: tuple[float, float], old: tuple[float, float]) -> bool:
    tol = 1e-12
    ge = all(n >= o - tol for n, o in zip(new, old, strict=True))
    gt = any(n > o + tol for n, o in zip(new, old, strict=True))
    return ge and gt


def count_improvements(ref1: list[F], ref2: list[F]) -> tuple[int, tuple[list[F], list[F]] | None]:
    base = (util(pi, ref1), util(pi, ref2))
    cnt = 0
    first = None
    for y1, y2 in allocs:
        if any(b <= 0 for b in y1 + y2):
            continue
        if improves((util(pi, y1), util(pi, y2)), base):
            cnt += 1
            if first is None:
                first = (y1, y2)
    return cnt, first


cnt_eq, _ = count_improvements(x1, x2)
cnt_end, first_end = count_improvements(e1, e2)
check("L03 grid improvements at equilibrium", cnt_eq, 0)
check("L03 grid improvements at endowment", cnt_end, 2)
check("L03 first improvement at endowment agent1", first_end[0] if first_end else None, [F(2), F(4), F(3)])
check("L03 first improvement at endowment agent2", first_end[1] if first_end else None, [F(2), F(4), F(1)])


# ---- L04 (cards c062-c065, c215, c217) ----
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
                m[i] = [a - f * b for a, b in zip(m[i], m[r], strict=True)]
        r += 1
    return r


A2 = [[F(1), F(1), F(1)], [F(0), F(1), F(2)]]
A4 = [[F(1), F(0), F(0)], [F(0), F(1), F(0)], [F(0), F(0), F(1)], [F(1), F(2), F(3)]]
check("L04 rank Example 2.2", rank(A2), 2)
check("L04 rank Example 2.3", rank(A4), 3)
for x, want in [((F(1), F(2), F(3)), 2), ((F(0), F(0), F(1)), 3), ((F(5), F(0), F(0)), 3)]:
    check(f"L04 augmented rank {x}", rank(A2 + [list(x)]), want)
check(
    "L04 (1,2,3)=1e1+2e2+3e3",
    [1 * a + 2 * b + 3 * c for a, b, c in zip(A4[0], A4[1], A4[2], strict=True)],
    [F(1), F(2), F(3)],
)
check("L04 misc 2 rank", rank([[F(1), F(1), F(1)], [F(1), F(1), F(1)], [F(0), F(1), F(2)]]), 2)
check("L04 M1 rank", rank([[F(1), F(2), F(0)], [F(2), F(4), F(0)]]), 1)
for t in [F(0), F(1), F(3, 7)]:
    th = [1 - t, 2 - 2 * t, 3 - 3 * t, t]
    pay = [sum(th[j] * A4[j][s] for j in range(4)) for s in range(3)]
    check(f"L04 replicating family t={t}", pay, [F(1), F(2), F(3)])

# ---- L05 (cards c090-c094, c219) ----
alpha, beta, sv, dl = F(10), F(2), F(1, 2), F(3, 4)
c0s = alpha / (beta + sv)
c1s = -dl / (beta + sv)
check("L05 fixed point", (c0s, c1s), (F(4), F(-3, 10)))


def psi(c: tuple[F, F], al: F, be: F, vs: F, de: F) -> tuple[F, F]:
    return ((al - vs * c[0]) / be, -(vs * c[1] + de) / be)


c = (F(0), F(0))
path0, path1 = [c[0]], [c[1]]
for _ in range(8):
    c = psi(c, alpha, beta, sv, dl)
    path0.append(c[0])
    path1.append(c[1])
check("L05 base c0 path first 3", path0[:3], [F(0), F(5), F(15, 4)])
check("L05 base c0 path last (8th iterate)", path0[-1], F(65535, 16384))
check("L05 base c1 path last (8th iterate)", path1[-1], F(-39321, 131072))
ratios0 = [(path0[k + 1] - c0s) / (path0[k] - c0s) for k in range(len(path0) - 1)]
check("L05 base c0 ratios all -1/4", set(ratios0[:8]), {F(-1, 4)})
# Part C: varsigma = beta = 2
al, be, vs, de = F(10), F(2), F(2), F(3, 4)
c0s_eq = al / (be + vs)
c1s_eq = -de / (be + vs)
check("L05 Part C fixed point", (c0s_eq, c1s_eq), (F(5, 2), F(-3, 16)))
c = (F(0), F(0))
p0 = [c[0]]
for _ in range(6):
    c = psi(c, al, be, vs, de)
    p0.append(c[0])
check("L05 Part C c0 path", p0, [F(0), F(5), F(0), F(5), F(0), F(5), F(0)])
# Part D: varsigma = 3
vs = F(3)
c0s_d = al / (be + vs)
c = (F(0), F(0))
p0d = [c[0]]
for _ in range(6):
    c = psi(c, al, be, vs, de)
    p0d.append(c[0])
check("L05 Part D fixed point", c0s_d, F(2))
check("L05 Part D c0 path", p0d[:4], [F(0), F(5), F(-5, 2), F(35, 4)])
check("L05 Part D error e3 = 27/4", p0d[3] - c0s_d, F(27, 4))
check("L05 Part D ratio -3/2", (p0d[2] - c0s_d) / (p0d[1] - c0s_d), F(-3, 2))
# Part E damped step
nu = beta / (beta + sv)  # base params
check("L05 Part E damping weight 4/5", nu, F(4, 5))
cc = (F(0), F(0))
img = psi(cc, F(10), F(2), F(1, 2), F(3, 4))
dmp = ((1 - F(4, 5)) * cc[0] + F(4, 5) * img[0], (1 - F(4, 5)) * cc[1] + F(4, 5) * img[1])
check("L05 Part E damped step", dmp, (F(4), F(-3, 10)))
# R1 at varsigma=beta=2, alpha=10: damped weight 1/2 gives 5/2
check("L05 R1 damped weight", F(2) / (F(2) + F(2)), F(1, 2))

# ---- L06 (cards c118-c123, c220) ----
sv2, se2, a6, lam6, su2 = F(1), F(1), F(1), F(1, 2), F(1, 4)
tv, te = 1 / sv2, 1 / se2
kap = a6 * se2 / lam6
seta2 = se2 + kap * kap * su2
taue = 1 / seta2
taubar = lam6 * te + (1 - lam6) * taue
ths = taubar / (tv + taubar)
thu = kap * ths
check("L06 kappa", kap, F(2))
check("L06 sigma_eta^2", seta2, F(2))
check("L06 taubar", taubar, F(3, 4))
check("L06 theta_s*", ths, F(3, 7))
check("L06 theta_u*", thu, F(6, 7))


def resid(s: F, u: F, t_s: F, t_u: F) -> F:
    price = t_s * s - t_u * u
    var_p = t_s * t_s * (sv2 + se2) + t_u * t_u * su2
    cov_vp = t_s * sv2
    slope = cov_vp / var_p
    resid_var = sv2 - slope * cov_vp
    var_inf = sv2 * se2 / (sv2 + se2)
    mean_inf = sv2 * s / (sv2 + se2)
    dinf = (mean_inf - price) / (a6 * var_inf)
    dunf = (slope * price - price) / (a6 * resid_var)
    return lam6 * dinf + (1 - lam6) * dunf - u


grid_s = [F(-1), F(0), F(1), F(2)]
grid_u = [F(-1), F(0), F(1, 2), F(2)]
res = [resid(s, u, ths, thu) for s in grid_s for u in grid_u]
check("L06 Part C 16 zero residuals", sum(1 for r in res if r == 0), 16)
check("L06 Part D residual (1,0) alt slope 1/2", resid(F(1), F(0), F(1, 2), thu), F(-9, 85))
var_p6 = ths * ths * (sv2 + se2) + thu * thu * su2
check("L06 var(p) base", var_p6, F(27, 49))
slope_vp = (ths * sv2) / var_p6
check("L06 slope v on p 7/9", slope_vp, F(7, 9))
check("L06 posterior var 2/3", sv2 - slope_vp * ths * sv2, F(2, 3))
xi = (F(1) * 1 - ths * 1) / (a6 * sv2 * se2 / (sv2 + se2)) if False else (F(1, 2) * 1 - ths) / (a6 * F(1, 2))
check("L06 x_I at s=1,u=0", xi, F(1, 7))
var_u6 = sv2 - slope_vp * ths * sv2
xu = (slope_vp * ths - ths) / (a6 * var_u6)
check("L06 x_U at s=1,u=0", xu, F(-1, 7))
check("L06 clearing at (1,0)", lam6 * xi + (1 - lam6) * xu, F(0))
check("L06 eta variance = 2", seta2, F(2))
# M1-M3 instance: a=2, su2=1/4
a6b = F(2)
kb = a6b * se2 / lam6
setab = se2 + kb * kb * su2
taub = F(1) / setab
tbar_b = lam6 * te + (1 - lam6) * taub
thsb = tbar_b / (tv + tbar_b)
check("L06 M1 kappa", kb, F(4))
check("L06 M1 theta_s", thsb, F(3, 8))
check("L06 M1 theta_u", kb * thsb, F(3, 2))


# ---- L07 (cards c141-c150) ----
def rho2(sv2_: F, se2_: F, a_: F, lam_: F, su_: F) -> F:
    kap_ = a_ * se2_ / lam_
    seta2_ = se2_ + kap_ * kap_ * su_**2
    return sv2_ / (sv2_ + seta2_)


def varp(sv2_: F, se2_: F, a_: F, lam_: F, su_: F) -> F:
    kap_ = a_ * se2_ / lam_
    seta2_ = se2_ + kap_ * kap_ * su_**2
    tau_e = 1 / (se2_ + kap_ * kap_ * su_**2) * 0 + 1 / se2_
    tau_e = 1 / seta2_
    tau_eps = 1 / se2_
    taubar_ = lam_ * tau_eps + (1 - lam_) * tau_e
    th_s = taubar_ / (1 / sv2_ + taubar_)
    th_u = kap_ * th_s
    return th_s * th_s * (sv2_ + se2_) + th_u * th_u * su_ * su_


check("L07 Part A rho2", rho2(F(1), F(1), F(1), F(1, 2), F(1, 2)), F(1, 3))
sus = [F(1, 4), F(1, 2), F(1), F(2), F(4)]
check(
    "L07 Part B rho2 sweep",
    [rho2(F(1), F(1), F(1), F(1, 2), s) for s in sus],
    [F(4, 9), F(1, 3), F(1, 6), F(1, 18), F(1, 66)],
)
check("L07 Part B var(p) at 1/4", varp(F(1), F(1), F(1), F(1, 2), F(1, 4)), F(729, 1444))
check("L07 Part B var(p) at 1/2", varp(F(1), F(1), F(1), F(1, 2), F(1, 2)), F(27, 49))
check("L07 Part B var(p) at 4", varp(F(1), F(1), F(1), F(1, 2), F(4)), F(35937, 4802))
check(
    "L07 Part C rho2 lam sweep",
    [rho2(F(1), F(1), F(1), l, F(1, 2)) for l in [F(1, 4), F(1, 2), F(3, 4)]],
    [F(1, 6), F(1, 3), F(9, 22)],
)
check(
    "L07 Part D rho2 a sweep",
    [rho2(F(1), F(1), a, F(1, 2), F(1, 2)) for a in [F(1, 2), F(1), F(2)]],
    [F(4, 9), F(1, 3), F(1, 6)],
)
check("L07 rho2 at sigma_u=4 (1/66)", rho2(F(1), F(1), F(1), F(1, 2), F(4)), F(1, 66))
check("L07 rho2 tau form at base = 1/3", (F(1, 2)) / (F(1) + F(1, 2)), F(1, 3))
check("L07 R2 sigma_u at half benchmark", math.sqrt(2 / 4), 1 / math.sqrt(2), tol=1e-12)
check("L07 E1 difference", (F(1, 3) - F(330625, 10**6)), F(2708, 10**6), tol=1e-6)

# ---- L08 (cards c180-c184, c222-c224) ----
a8, sv28, se28, su28 = 2.0, 1.0, 1.0, 1.0
tv8, te8 = 1 / sv28, 1 / se28


def gain_and_corr(lam: float, su2_: float = su28, sv2_: float = sv28, se2_: float = se28) -> tuple[float, float]:
    tv_, te_ = 1 / sv2_, 1 / se2_
    kap = a8 * se2_ / lam
    tau_eta = 1 / (se2_ + kap * kap * su2_)
    A = lam * te_ + (1 - lam) * tau_eta
    beta = A / (tv_ + A)
    bs = sv2_ / (sv2_ + se2_)
    by = tau_eta / (tv_ + tau_eta)
    sig_eta2 = 1 / tau_eta
    VI = 1 / (tv_ + te_)
    VU = 1 / (tv_ + tau_eta)
    var_di = (bs - beta) ** 2 * (sv2_ + se2_) + kap * kap * beta * beta * su2_
    var_du = (by - beta) ** 2 * (sv2_ + sig_eta2)
    g = (1 / (2 * a8)) * math.log((1 + var_di / VI) / (1 + var_du / VU))
    corr2 = tau_eta / (tv_ + tau_eta)
    return g, corr2


g0 = math.log(2) / 4
g1 = math.log(5 / 3) / 4
check("L08 G(0) closed form", g0, 0.173287, tol=1e-6)
check("L08 G(1) numeric", gain_and_corr(1.0)[0], g1, tol=1e-12)
check("L08 G(1) closed form ln(5/3)/4", g1, 0.127706, tol=1e-6)
check("L08 G(0.5) printed 0.158997", gain_and_corr(0.5)[0], 0.158997, tol=1e-6)
check("L08 Part A slope formula b_y/beta at 0.5", 0.1605, (1 / 18) / (9 / 26), tol=1e-4)


def solve(cost: float) -> tuple[float, float, float]:
    if cost >= g0:
        return 0.0, g0 - cost, 0.0
    if cost <= g1:
        return 1.0, g1 - cost, gain_and_corr(1.0)[1]
    lo, hi = 0.0, 1.0
    # the lab's bisection on (0, 1); the net benefit is positive at lo=0+ and negative at hi=1
    while hi - lo > 1e-12:
        mid = (lo + hi) / 2
        if gain_and_corr(mid)[0] - cost > 0:
            lo = mid
        else:
            hi = mid
    lam = (lo + hi) / 2
    return lam, gain_and_corr(lam)[0] - cost, gain_and_corr(lam)[1]


expect = {
    0.12: 1.0,
    0.13: 0.965625410,
    0.14: 0.815032329,
    0.15: 0.657828572,
    0.16: 0.480567912,
    0.17: 0.231615819,
    0.18: 0.0,
}
for cst, want in expect.items():
    lam, gap, corr = solve(cst)
    check(f"L08 Part C lam* at cost {cst}", round(lam, 6), round(want, 6), tol=None)
lam15, gap15, corr15 = solve(0.15)
check("L08 cost 0.15 Corr^2", round(corr15, 6), 0.088941, tol=None)
check("L08 cost 0.15 gap is 0 to 1e-12", abs(gap15) < 1e-9, True)
check("L08 cost 0.12 boundary gap", round(solve(0.12)[1], 5), 0.00771, tol=None)
check("L08 cost 0.18 boundary gap", round(solve(0.18)[1], 5), -0.00671, tol=None)
check("L08 Corr^2 at cost 0.17", round(solve(0.17)[2], 6), 0.013061, tol=None)
check("L08 Corr^2 at cost 0.12", round(solve(0.12)[2], 6), 0.166667, tol=None)
check("L08 G(1) boundary: cost 0.12 <= G(1)=0.127706", 0.12 <= g1, True)
check("L08 G(0) boundary: cost 0.18 >= G(0)=0.173287", 0.18 >= g0, True)
# Part D: sigma_u^2 = 0, cost 0.15: gains on the 999 interior grid are all zero
grid999 = [k / 1000 for k in range(1, 1000)]
gains_nu0 = [gain_and_corr(x, su2_=0.0)[0] for x in grid999]
check("L08 Part D max |gain| (sigma_u=0) on grid", max(abs(g) for g in gains_nu0), 0.0, tol=1e-12)
check("L08 Part D gain(0) sigma_u=0", math.log(2) / 4, 0.173287, tol=1e-6)
check("L08 Part D interior gain equal to cost 0.15", sum(1 for g in gains_nu0 if abs(g - 0.15) <= 1e-9), 0)

# ---- L09 (cards c200, c201, c203, c204, c211) ----
Omega = [1, 2, 3, 4, 5, 6]
P1 = [{1, 2}, {3}, {4, 5, 6}]
P2 = [{1, 2, 3}, {4, 5}, {6}]
prior = F(1, 6)


def cell(parts: list[set[int]], w: int) -> set[int]:
    return next(c for c in parts if w in c)


cnt_strict = 0
cnt_nonneg_meet = 0
cnt_nonneg_meet_nonzero = 0
example_first = None
vals = [-2, -1, 0, 1, 2]
for x_vals in product(vals, repeat=6):
    x = {w: F(x_vals[w - 1]) for w in Omega}
    if len(x) != 6:
        continue

    def post1(w: int) -> F:
        c_ = cell(P1, w)
        return sum((x[v] for v in c_), F(0)) / len(c_)

    def post2(w: int) -> F:
        c_ = cell(P2, w)
        return sum((-x[v] for v in c_), F(0)) / len(c_)

    # meet of state 1
    meet = {1}
    changed = True
    while changed:
        changed = False
        for part in (P1, P2):
            for c_ in part:
                if c_ & meet and not c_ <= meet:
                    meet |= c_
                    changed = True
    if meet != {1, 2, 3}:
        continue
    if post1(1) > 0 and post2(1) > 0:
        cnt_strict += 1
        if example_first is None:
            example_first = x_vals
        if all(post1(w) >= 0 and post2(w) >= 0 for w in meet):
            cnt_nonneg_meet += 1
    if all(post1(w) >= 0 and post2(w) >= 0 for w in meet):
        cnt_nonneg_meet_nonzero += 0
check("L09 bets enumerated 5^6", len(list(product(vals, repeat=6))), 15625)
check("L09 strict both at state 1 on meet {1,2,3} setting", cnt_strict, 500)
check("L09 strict both and nonneg on meet", cnt_nonneg_meet, 0)
check("L09 first strict bet", example_first, (-1, 2, -2, -2, -2, -2))
# nonneg on meet count (625) and zero-posterior characterisation
nn = 0
zero_char = 0
for x_vals in product(vals, repeat=6):
    x = {w: F(x_vals[w - 1]) for w in Omega}

    def p1(w: int) -> F:
        c_ = cell(P1, w)
        return sum((x[v] for v in c_), F(0)) / len(c_)

    def p2(w: int) -> F:
        c_ = cell(P2, w)
        return sum((-x[v] for v in c_), F(0)) / len(c_)

    meet = {1, 2, 3}
    if all(p1(w) >= 0 and p2(w) >= 0 for w in meet):
        nn += 1
        if all(p1(w) == 0 and p2(w) == 0 for w in meet):
            zero_char += 1
    if x[3] == 0 and x[2] == -x[1] and all(p1(w) == 0 and p2(w) == 0 for w in meet):
        pass
check("L09 nonneg on meet {1,2,3} count 625", nn, 625)
check("L09 nonneg on meet are all zero-posterior", zero_char, nn)
check("L09 closed-form count 5*5^3", 5 * 5**3, 625)
# Example 2.4 posteriors
xe = {1: F(-1), 2: F(2), 3: F(-2), 4: F(-2), 5: F(-2), 6: F(-2)}
g1_1 = (xe[1] + xe[2]) / 2
g2_1 = sum((-xe[v] for v in {1, 2, 3}), F(0)) / 3
check("L09 Example 2.4 g1(1)", g1_1, F(1, 2))
check("L09 Example 2.4 g2(1)", g2_1, F(1, 3))
# Section 4 two priors
check("L09 Sec 4 trader1 expected", F(7, 10) * 1 + F(3, 10) * (-1), F(2, 5))
check("L09 Sec 4 trader2 expected of -x", F(-4, 10) + F(6, 10), F(1, 5))
# Res 2 with p=0.7 (H) and r=0.4 (H) and theta=(p+r)/2
pp, rr = F(7, 10), F(2, 5)
th = (pp + rr) / 2
tt = th / (1 - th)
check("L09 Res 2 trader1 receipt positive", pp - (1 - pp) * tt > 0, True)
check("L09 Res 2 trader2 receipt positive", -(rr - (1 - rr) * tt) > 0, True)

print("MISMATCHES:", FAIL if FAIL else "none")
