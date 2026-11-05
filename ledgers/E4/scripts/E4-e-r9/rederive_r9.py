"""Round 9, slice e (verifier): independent re-derivation of the numbers on the E4 cards.

Written from the lesson formulas, not from the lesson or lab code. Exact values use fractions.Fraction; float checks
use math and print the computed value next to the card value. Prints CHECK lines and a SUMMARY line.
Run as: .venv/bin/python -I ledgers/E4/scripts/E4-e-r9/rederive_r9.py
"""

import itertools
import math
from fractions import Fraction as F

rows: list[bool] = []


def check(name: str, got: object, want: object, tol: float | None = None) -> None:
    if tol is None:
        ok = got == want
    else:
        ok = abs(float(got) - float(want)) <= tol  # type: ignore[arg-type]
    rows.append(ok)
    print(f"CHECK {name} computed={got} card={want} {'OK' if ok else 'MISMATCH'}")


# ---------- L01 (cards c011, c012, c013, c007) ----------
q = [F(1, 2), F(1, 3), F(1, 4), F(1, 5)]
x = [F(100), F(40), F(0), F(250)]
y = [F(0), F(60), F(120), F(30)]
check("c011 V(x) for x=(100,40,0,250)", sum(a * b for a, b in zip(q, x)), F(340, 3))
comb = [2 * a - F(1, 2) * b for a, b in zip(x, y)]
check("c012 combination payoff", comb, [F(200), F(50), F(-60), F(485)])
Vy = sum(a * b for a, b in zip(q, y))
check("c012 V(2x - y/2) = 2V(x) - V(y)/2", sum(a * b for a, b in zip(q, comb)), 2 * F(340, 3) - F(1, 2) * Vy)
check("c012 value 596/3", sum(a * b for a, b in zip(q, comb)), F(596, 3))
pi = [F(1, 8), F(3, 8), F(3, 8), F(1, 8)]
check("c013 E x", sum(a * b for a, b in zip(pi, x)), F(235, 4))

# ---------- L02 (cards c030, c031-c034, c036, c237, c238) ----------
pi2 = [F(1, 2), F(1, 4), F(1, 4)]
e1 = [F(3), F(4), F(1)]
e2 = [F(1), F(4), F(3)]
ebar = [a + b for a, b in zip(e1, e2)]
check("c237 aggregate endowment", ebar, [F(4), F(8), F(4)])
qs = [p / e for p, e in zip(pi2, ebar)]
check("c031 prices", qs, [F(1, 8), F(1, 32), F(1, 16)])
check("c238 q*.ebar = 1", sum(a * b for a, b in zip(qs, ebar)), F(1))
th1 = sum(p * a / e for p, a, e in zip(pi2, e1, ebar))
th2 = sum(p * a / e for p, a, e in zip(pi2, e2, ebar))
check("c030 wealth w1 = theta_1", th1, F(9, 16))
check("c030 wealth w2 = theta_2", th2, F(7, 16))
check("c032 agent 1 bundle", [th1 * e for e in ebar], [F(9, 4), F(9, 2), F(9, 4)])
check("c032 agent 2 bundle", [th2 * e for e in ebar], [F(7, 4), F(7, 2), F(7, 4)])
x1 = [th1 * e for e in ebar]
check("c034 pi_s/(x_s q_s) agent 1", [p / (a * qq) for p, a, qq in zip(pi2, x1, qs)], [F(16, 9)] * 3)
x2 = [th2 * e for e in ebar]
check("c034 pi_s/(x_s q_s) agent 2", [p / (a * qq) for p, a, qq in zip(pi2, x2, qs)], [F(16, 7)] * 3)
check("c036 price state 2 vs 3", (qs[1], qs[2]), (F(1, 32), F(1, 16)))
v = [1, -1, 0]
check("c037 v.q (Walras) at Example 2.11 prices", sum(a * b for a, b in zip(v, qs)), F(3, 32))

# ---------- L03 (cards c046, c048, c049, c214) ----------
mrs = lambda pis, xs, s, t: (pis[s] / xs[s]) / (pis[t] / xs[t])  # noqa: E731  (u' = 1/x for ln)
check("c046 MRS 1-2 agent 1", mrs(pi2, x1, 0, 1), F(4))
check("c046 MRS 1-3 agent 1", mrs(pi2, x1, 0, 2), F(2))
check("c046 MRS 2-3 agent 1", mrs(pi2, x1, 1, 2), F(1, 2))
check("c046 MRS 1-2 agent 2", mrs(pi2, x2, 0, 1), F(4))
check("c046 price ratios", (qs[0] / qs[1], qs[0] / qs[2], qs[1] / qs[2]), (F(4), F(2), F(1, 2)))


def ln_util(pis, bundle):
    return sum(float(p) * math.log(float(b)) for p, b in zip(pis, bundle))


def count_improvements(alloc_a, alloc_b, endow_a, endow_b):
    """Pareto improvements of (alloc_a, alloc_b) among the grid allocations (shares in {0,1/4,1/2,3/4,1})."""
    base_a, base_b = ln_util(pi2, endow_a), ln_util(pi2, endow_b)
    cur_a, cur_b = ln_util(pi2, alloc_a), ln_util(pi2, alloc_b)
    del base_a, base_b
    n = 0
    shares = [F(k, 4) for k in range(5)]
    for sh in itertools.product(shares, repeat=3):
        ya = [s * e for s, e in zip(sh, ebar)]
        yb = [e - a for e, a in zip(ebar, ya)]
        if any(b <= 0 for b in ya + yb):
            continue
        ua, ub = ln_util(pi2, ya), ln_util(pi2, yb)
        if ua >= cur_a - 1e-12 and ub >= cur_b - 1e-12 and (ua > cur_a + 1e-12 or ub > cur_b + 1e-12):
            n += 1
    return n


check("c048 grid Pareto improvements at equilibrium", count_improvements(x1, x2, e1, e2), 0)
check("c214 grid Pareto improvements at endowment", count_improvements(e1, e2, e1, e2), 2)
# c049: trade from endowment; derivatives at eps = 0
d1 = pi2[0] * (-1 / 3) + pi2[1] * (4 / 4)
d2 = pi2[0] * (1 / 1) + pi2[1] * (-4 / 4)
check("c049 dU1/deps", F(d1).limit_denominator(1000), F(1, 12))
check("c049 dU2/deps", F(d2).limit_denominator(1000), F(1, 4))

# ---------- L04 (cards c062-c065, c226, c240) ----------


def rank(rows_):
    m = [list(map(F, r)) for r in rows_]
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


check("c062 rank two securities", rank([(1, 1, 1), (0, 1, 2)]), 2)
check("c064 rank four securities", rank([(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 2, 3)]), 3)
check("c065 aug rank (1,2,3)", rank([(1, 1, 1), (0, 1, 2), (1, 2, 3)]), 2)
check("c065 aug rank (0,0,1)", rank([(1, 1, 1), (0, 1, 2), (0, 0, 1)]), 3)
check("c065 aug rank (5,0,0)", rank([(1, 1, 1), (0, 1, 2), (5, 0, 0)]), 3)
check("c071 rank (1,1,1),(1,1,1),(0,1,2)", rank([(1, 1, 1), (1, 1, 1), (0, 1, 2)]), 2)

# ---------- L05 (cards c090-c097, c243) ----------


def l05_path(alpha, beta, sv, dl, n):
    c0, c1 = F(0), F(0)
    out = [(c0, c1)]
    for _ in range(n):
        c0, c1 = (alpha - sv * c0) / beta, -(sv * c1 + dl) / beta
        out.append((c0, c1))
    return out


p_d = l05_path(F(10), F(2), F(3), F(3, 4), 3)
check("c093 c0 path Part D", [a for a, _ in p_d], [F(0), F(5), F(-5, 2), F(35, 4)])
cstar = F(10) / (F(2) + F(3))
errs = [a - cstar for a, _ in p_d]
check("c243 error ratios Part D", [errs[k + 1] / errs[k] for k in range(3)], [F(-3, 2)] * 3)
p_c = l05_path(F(10), F(2), F(2), F(3, 4), 6)
check("c092 c0 path with varsigma=beta", [a for a, _ in p_c][:4], [F(0), F(5), F(0), F(5)])
p_b = l05_path(F(10), F(2), F(1, 2), F(3, 4), 3)
check("c091 c0 path base", [a for a, _ in p_b], [F(0), F(5), F(15, 4), F(65, 16)])
check("c090 fixed point base", (F(10) / (F(2) + F(1, 2)), -F(3, 4) / (F(2) + F(1, 2))), (F(4), F(-3, 10)))
check("c219 fixed point varsigma 2", (F(10) / F(4), -F(3, 4) / F(4)), (F(5, 2), F(-3, 16)))
check("c094 damped step weight 4/5", F(4, 5) * 0 + (F(1) - F(4, 5)) * 0 + F(4, 5) * ((F(10) - F(1, 2) * 0) / F(2)), F(4))

# ---------- L06 (cards c118-c125, c220, c244, c247) ----------


def l06(sv, se, a, lam, su2):
    tv, te = 1 / sv, 1 / se
    kap = a * se / lam
    setas2 = se + kap * kap * su2
    tau_eta = 1 / setas2
    tbar = lam * te + (1 - lam) * tau_eta
    ths = tbar / (tv + tbar)
    thu = kap * ths
    return dict(kappa=kap, sig_eta2=setas2, tau_eta=tau_eta, ths=ths, thu=thu)


base = l06(F(1), F(1), F(1), F(1, 2), F(1, 4))
check("c118 theta_s", base["ths"], F(3, 7))
check("c118 theta_u", base["thu"], F(6, 7))
check("c118 sigma_eta^2", base["sig_eta2"], F(2))
check("c244 sigma_eta^2 >= sigma_eps^2 at base", base["sig_eta2"] >= F(1), True)
ths, thu = base["ths"], base["thu"]
var_p = ths**2 * (F(1) + F(1)) + thu**2 * F(1, 4)
cov_vp = ths * F(1)
check("L06 Part B Var(p)", var_p, F(27, 49))
check("c119 slope b = Cov/Var(p)", cov_vp / var_p, F(7, 9))
check("c119 Var(v|p) = 1 - b Cov", F(1) - (cov_vp / var_p) * cov_vp, F(2, 3))
# c220 and c247: demands at s=1, u=0 with p = theta_s
s_, u_ = F(1), F(0)
p_ = ths * s_ - thu * u_
omega = F(1) / (F(1) + F(1))
VI = F(1, 1) / (F(1) + F(1))
xI = (omega * s_ - p_) / (F(1) * VI)
b_ = cov_vp / var_p
VU = F(1) - b_ * cov_vp
xU = (b_ * p_ - p_) / (F(1) * VU)
check("c120 x_I at (1,0)", xI, F(1, 7))
check("c220 x_U at (1,0)", xU, F(-1, 7))
check("c247 clearing 1/2 x_I + 1/2 x_U - u", F(1, 2) * xI + F(1, 2) * xU - u_, F(0))
# c123: alternative slope theta_s = 1/2, theta_u unchanged (6/7)
ths_alt = F(1, 2)
p_alt = ths_alt * s_ - thu * u_
var_alt = ths_alt**2 * 2 + thu**2 * F(1, 4)
cov_alt = ths_alt * F(1)
b_alt = cov_alt / var_alt
VU_alt = F(1) - b_alt * cov_alt
xU_alt = (b_alt * p_alt - p_alt) / VU_alt
xI_alt = (omega * s_ - p_alt) / VI
resid = F(1, 2) * xI_alt + F(1, 2) * xU_alt - u_
check("c123 A4 residual at (1,0) with theta_s=1/2", resid, F(-9, 85))

# ---------- L07 (cards c130-c150) ----------


def rho2(sv, se, a, lam, su):
    kap = a * se / lam
    se_eta2 = se + kap * kap * su * su
    return sv / (sv + se_eta2)


check("c141 rho2 base", rho2(F(1), F(1), F(1), F(1, 2), F(1, 2)), F(1, 3))
sweep = [rho2(F(1), F(1), F(1), F(1, 2), F(sd)) for sd in (F(1, 4), F(1, 2), F(1), F(2), F(4))]
check("c142 rho2 sweep", sweep, [F(4, 9), F(1, 3), F(1, 6), F(1, 18), F(1, 66)])
lamsweep = [rho2(F(1), F(1), F(1), F(lam), F(1, 2)) for lam in (F(1, 4), F(1, 2), F(3, 4))]
check("c144 rho2 over lambda", lamsweep, [F(1, 6), F(1, 3), F(9, 22)])
asweep = [rho2(F(1), F(1), F(a), F(1, 2), F(1, 2)) for a in (F(1, 2), F(1), F(2))]
check("c145 rho2 over a", asweep, [F(4, 9), F(1, 3), F(1, 6)])
var_sweep = []
for sd in (F(1, 4), F(4)):
    kap = F(1) * F(1) / F(1, 2)
    kap = kap  # a * sigma_eps^2 / lambda with a=1, lambda=1/2
    ths_ = (F(1, 2) * 1 + F(1, 2) * 1 / (1 + kap * kap * sd * sd)) / (1 + (F(1, 2) + F(1, 2) / (1 + kap * kap * sd * sd)))
    thu_ = kap * ths_
    var_sweep.append(ths_**2 * 2 + thu_**2 * sd * sd)
check("c143 Var(p) at sd=1/4 and sd=4", var_sweep, [F(729, 1444), F(35937, 4802)])
check("c146 1/3 - 0.330625", float(F(1, 3)) - 0.330625, 13 / 4800, 1e-12)
check("c146 (13/4800)/0.02", (13 / 4800) / 0.02, 13 / 96, 1e-12)

# ---------- L08 (cards c180, c182-c184, c185, c222, c223, c245, c246) ----------


def l08(lam, a=2.0, sv=1.0, se=1.0, su2=1.0):
    tv, te = 1 / sv, 1 / se
    kap = a * se / lam
    tau_eta = 1 / (se + kap * kap * su2)
    A = lam * te + (1 - lam) * tau_eta
    beta = A / (tv + A)
    bs = te / (tv + te)
    by = tau_eta / (tv + tau_eta)
    VI = 1 / (tv + te)
    VU = 1 / (tv + tau_eta)
    var_DI = (bs - beta) ** 2 * (sv + se) + kap * kap * beta * beta * su2
    var_DU = (by - beta) ** 2 * (sv + 1 / tau_eta)
    G = (1 / (2 * a)) * math.log((1 + var_DI / VI) / (1 + var_DU / VU))
    corr2 = tau_eta / (tv + tau_eta)
    return dict(G=G, corr2=corr2, beta=beta, by=by, bs=bs, tau_eta=tau_eta, A=A)


def G0_closed(a=2.0, sv=1.0, se=1.0):
    return (1 / (2 * a)) * math.log(1 + sv / se)


check("c180 G(0) = ln(2)/4", G0_closed(), math.log(2) / 4, 1e-12)
check("c222 G(1) = ln(5/3)/4", l08(1.0)["G"], math.log(5 / 3) / 4, 1e-12)
check("c182 gain at reported lam* = 0.657828572 equals cost 0.15", l08(0.657828572)["G"], 0.15, 1e-6)
check("c182 Corr^2 at lam* = 0.088941", l08(0.657828572)["corr2"], 0.088941, 1e-6)
check("c182 Corr^2 at cost 0.17 root 0.013061", l08(0.231615819)["corr2"], 0.013061, 1e-6)
check("c182 gain at lam = 0.231615819 equals 0.17", l08(0.231615819)["G"], 0.17, 1e-6)
check("c187 Corr^2 at lam=1 = 1/6", l08(1.0)["corr2"], 1 / 6, 1e-12)
check("c223 sample-free formula b_y/beta at lam=0.5", l08(0.5)["by"] / l08(0.5)["beta"], 0.1605, 5e-5)
check("c223 Corr^2 at lam=0.5 equals corr2 closed form", l08(0.5)["corr2"], l08(0.5)["tau_eta"] / (1 + l08(0.5)["tau_eta"]), 1e-12)
# c245: Corr^2 strictly increasing in lambda (su2 = 1)
vals = [l08(lam)["corr2"] for lam in (0.1, 0.3, 0.5, 0.7, 0.9, 1.0)]
check("c245 Corr^2 increasing on grid", all(b > a for a, b in zip(vals, vals[1:])), True)
# c246: N = G - c; at c = 0.18 the boundary gap uses G(0) (closed form)
check("c183 gap at cost 0.12 is G(1)-0.12", round(l08(1.0)["G"] - 0.12, 5), 0.00771)
check("c183 gap at cost 0.18 is G(0)-0.18", round(G0_closed() - 0.18, 5), -0.00671)

# ---------- L09 (cards c200-c207, c233) ----------
Omega = range(1, 7)
P1 = [{1, 2}, {3}, {4, 5, 6}]
P2 = [{1, 2, 3}, {4, 5}, {6}]


def cell(P, w):
    return next(c for c in P if w in c)


def meet(w):
    reach = {w}
    changed = True
    while changed:
        changed = False
        for P in (P1, P2):
            for c in P:
                if reach & c and not c <= reach:
                    reach |= c
                    changed = True
    return reach


def post(x, P, sign, w):
    c = cell(P, w)
    return F(sign) * sum(F(x[k - 1]) for k in c) / len(c)


bets = list(itertools.product((-2, -1, 0, 1, 2), repeat=6))
check("c204 number of bets", len(bets), 15625)
strict1 = [b for b in bets if post(b, P1, 1, 1) > 0 and post(b, P2, -1, 1) > 0]
check("c201 strictly positive for both at state 1", len(strict1), 500)
m1 = meet(1)
nonneg_meet = [b for b in bets if all(post(b, P1, 1, w) >= 0 and post(b, P2, -1, w) >= 0 for w in m1)]
check("c201 nonnegative on meet {1,2,3}", len(nonneg_meet), 625)
check("c201 strict and nonneg on meet", len([b for b in strict1 if b in set(nonneg_meet)]), 0)
zero_on_meet = [b for b in nonneg_meet if all(post(b, P1, 1, w) == 0 and post(b, P2, -1, w) == 0 for w in m1)]
check("c203 nonneg bets with zero posteriors on meet", len(zero_on_meet), 625)
pred = [b for b in bets if b[2] == 0 and b[1] == -b[0]]
check("c203 closed-form count x(3)=0, x(2)=-x(1)", len(pred), 625)
m4 = meet(4)
strict4 = [b for b in bets if post(b, P1, 1, 4) > 0 and post(b, P2, -1, 4) > 0]
nn4 = [b for b in strict4 if all(post(b, P1, 1, w) >= 0 and post(b, P2, -1, w) >= 0 for w in m4)]
check("c233 strict at state 4", len(strict4), 500)
check("c233 strict and nonneg on meet {4,5,6}", len(nn4), 0)
check("c200 Example 2.4 meet of state 1", sorted(m1), [1, 2, 3])
ex = (-1, 2, -2, -2, -2, -2)
check("c200 g1(1), g2(1), g1(3)", (post(ex, P1, 1, 1), post(ex, P2, -1, 1), post(ex, P1, 1, 3)), (F(1, 2), F(1, 3), F(-2)))
check("c205 two-prior receipts", (F(7, 10) * 1 + F(3, 10) * -1, -(F(4, 10) * 1 + F(6, 10) * -1)), (F(2, 5), F(1, 5)))

print(f"SUMMARY checks {len(rows)} failures {rows.count(False)}")
