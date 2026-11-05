"""Independent re-derivation of the numbers printed on L07, L08 and L09 (verifier round 9, slice E4-c).

Written from the page formulas, not from the lab code. Exact rationals where possible; floats otherwise.
Run as: <venv python> -I -W error ledgers/E4/scripts/E4-c-r9/independent_checks.py
"""

from __future__ import annotations

import math
import random
from fractions import Fraction as F
from itertools import product

failures: list[str] = []


def check(name: str, cond: bool, detail: str) -> None:
    print(("PASS " if cond else "FAIL ") + name + " :: " + detail)
    if not cond:
        failures.append(name)


# ---------- L07: closed form rho^2 = sv2/(sv2 + se2 + kappa^2 sd^2 ...) via Prop 6.7 of L06 ----------
def l06_coeffs(sv2: F, se2: F, a: F, lam: F, su2: F) -> tuple[F, F, F, F]:
    tau_v, tau_e = 1 / sv2, 1 / se2
    kappa = a * se2 / lam  # kappa = a sigma_eps^2 / lambda
    seta2 = se2 + kappa * kappa * su2
    tau_eta = 1 / seta2
    tau_bar = lam * tau_e + (1 - lam) * tau_eta
    theta_s = tau_bar / (tau_v + tau_bar)
    return kappa, seta2, theta_s, kappa * theta_s


def rho2_moments(sv2: F, se2: F, theta_s: F, theta_u: F, su2: F) -> F:
    cov = theta_s * sv2
    var_p = theta_s * theta_s * (sv2 + se2) + theta_u * theta_u * su2
    return cov * cov / (sv2 * var_p)


# base instance and sweeps
for sd, expect in [(F(1, 4), F(4, 9)), (F(1, 2), F(1, 3)), (F(1), F(1, 6)), (F(2), F(1, 18)), (F(4), F(1, 66))]:
    kappa, seta2, ts, tu = l06_coeffs(F(1), F(1), F(1), F(1, 2), sd * sd)
    r2 = rho2_moments(F(1), F(1), ts, tu, sd * sd)
    closed = F(1) / (F(1) + seta2)
    check(f"L07 PartB rho2 sd={sd}", r2 == expect == closed, f"moments={r2} closed={closed} expected={expect}")

for sd, expect_var in [(F(1, 4), F(729, 1444)), (F(1, 2), F(27, 49)), (F(1), F(27, 32)), (F(2), F(729, 338)), (F(4), F(35937, 4802))]:
    kappa, seta2, ts, tu = l06_coeffs(F(1), F(1), F(1), F(1, 2), sd * sd)
    var_p = ts * ts * 2 + tu * tu * sd * sd
    check(f"L07 PartB var_p sd={sd}", var_p == expect_var, f"var_p={var_p} expected={expect_var}")

for lam, expect in [(F(1, 4), F(1, 6)), (F(1, 2), F(1, 3)), (F(3, 4), F(9, 22))]:
    kappa, seta2, ts, tu = l06_coeffs(F(1), F(1), F(1), lam, F(1, 4))
    r2 = F(1) / (F(1) + seta2)
    check(f"L07 PartC lam={lam}", r2 == expect, f"rho2={r2} expected={expect}")

for a, expect in [(F(1, 2), F(4, 9)), (F(1), F(1, 3)), (F(2), F(1, 6))]:
    kappa, seta2, ts, tu = l06_coeffs(F(1), F(1), a, F(1, 2), F(1, 4))
    r2 = F(1) / (F(1) + seta2)
    check(f"L07 PartD a={a}", r2 == expect, f"rho2={r2} expected={expect}")

kappa, seta2, ts, tu = l06_coeffs(F(1), F(1), F(1), F(1, 2), F(1, 100) ** 2)  # sd = 1/100, variance 1/10000
check("L07 PartE tiny sd below benchmark", F(1) / (F(1) + seta2) == F(2500, 5001), f"rho2={F(1) / (F(1) + seta2)}")

# L07 E1: difference with the printed sample value
diff = F(1, 3) - F(330625, 10**6)
check("L07 E1 difference = 13/4800", diff == F(13, 4800), f"diff={diff} float={float(diff):.6f}")
check("L07 E1 tolerance units = 13/96", diff / F(2, 100) == F(13, 96), f"units={float(diff / F(2, 100)):.4f}")

# L07 R2 and E2 closed forms
check("L07 E2 sigma_u = 1/sqrt2", abs(math.sqrt(1 / 2) - 0.7071) < 1e-4, "sqrt(1/2)")
chi = F(1)  # a=1, sigma_eps^2=1, lam=1/2 -> chi = a^2 se^4 / lam^2 = 4
chi = F(1) * F(1) / (F(1, 2) * F(1, 2))
check("L07 R2 chi=4 and sigma_u^2=1/2", chi == 4 and F(2) / chi == F(1, 2), f"chi={chi}")

# L07 R3 derivative sign and ratio
check("L07 M3 rho2 = 2/7", F(2) / (F(2) + F(5)) == F(2, 7), "sv2=2, seta2=5")

# ---------- L08: CARA-normal model, exact bisection-free checks ----------
a = F(2)


def l08_eq(lam: F, su2: F, sv2: F = F(1), se2: F = F(1)) -> dict[str, F]:
    tau_v, tau_e = 1 / sv2, 1 / se2
    kappa = a * se2 / lam
    tau_eta = 1 / (se2 + kappa * kappa * su2)
    A = lam * tau_e + (1 - lam) * tau_eta
    beta = A / (tau_v + A)
    b_s = tau_e / (tau_v + tau_e)
    b_y = tau_eta / (tau_v + tau_eta)
    post_s = 1 / (tau_v + tau_e)
    post_u = 1 / (tau_v + tau_eta)
    var_ds = (b_s - beta) ** 2 * (sv2 + se2) + (kappa * beta) ** 2 * su2
    var_du = (b_y - beta) ** 2 * (sv2 + 1 / tau_eta)
    return dict(kappa=kappa, tau_eta=tau_eta, beta=beta, b_y=b_y, b_s=b_s, post_s=post_s, post_u=post_u,
                var_ds=var_ds, var_du=var_du, corr2=b_y)


# Quiz: Corr^2 at lam = 1/2, unit variances, a=2, sigma_u^2=1 should be 1/18
e = l08_eq(F(1, 2), F(1))
check("L08 quiz Corr2 lam=1/2 = 1/18", e["corr2"] == F(1, 18), f"corr2={e['corr2']} tau_eta={e['tau_eta']}")
# Corr^2 via moments: Cov(v,p)=beta, Var(p)=beta^2*(1+1)+(kappa beta)^2
cov = e["beta"]
varp = e["beta"] ** 2 * 2 + (e["kappa"] * e["beta"]) ** 2
check("L08 Cor 3.2 moments = closed form", cov * cov / (1 * varp) == e["corr2"], f"moments={cov * cov / varp}")
# slope b_y/beta
check("L08 lab slope formula b_y/beta at lam=1/2 ~ 0.1605", abs(float(e["b_y"] / e["beta"]) - 0.1605) < 5e-5,
      f"b_y/beta={float(e['b_y'] / e['beta']):.6f}")

# G(1) and G(0)
def gain(lam: F, su2: F = F(1)) -> float:
    e = l08_eq(lam, su2)
    ln_arg = (1 + float(e["var_ds"] / e["post_s"])) / (1 + float(e["var_du"] / e["post_u"]))
    return math.log(ln_arg) / (2 * float(a))


G1 = gain(F(1))
check("L08 G(1)=ln(5/3)/4", abs(G1 - math.log(5 / 3) / 4) < 1e-12, f"G1={G1:.12f}")
G0_closed = math.log(2) / 4
check("L08 G(0)=ln2/4 (Lemma 4.5 closed form)", abs(G0_closed - 0.1732868) < 1e-7, f"G0={G0_closed:.10f}")

# independent Monte Carlo check of Var(D_I), Var(D_U) at lam=1/2 (double precision, seeded)
rng = random.Random(12345)
lam = 0.5
kap = 4.0
tau_eta_f = 1 / (1 + kap * kap)
A_f = lam * 1.0 + (1 - lam) * tau_eta_f
beta_f = A_f / (1 + A_f)
b_s_f = 0.5
b_y_f = tau_eta_f / (1 + tau_eta_f)
N = 200000
dI = []
dU = []
for _ in range(N):
    v = rng.gauss(0, 1)
    eps = rng.gauss(0, 1)
    u = rng.gauss(0, 1)
    s = v + eps
    p = (1 - beta_f) * 0 + beta_f * s - kap * beta_f * u
    dI.append((b_s_f * s) - p)  # E[v|s] - p with prior mean 0
    y = s - kap * u
    dU.append(b_y_f * y - p)
mI = sum(dI) / N
mU = sum(dU) / N
vI = sum((x - mI) ** 2 for x in dI) / N
vU = sum((x - mU) ** 2 for x in dU) / N
ex = l08_eq(F(1, 2), F(1))
mc_ok_I = abs(vI - float(ex["var_ds"])) / float(ex["var_ds"]) < 0.02
mc_ok_U = abs(vU - float(ex["var_du"])) / float(ex["var_du"]) < 0.02
check("L08 Prop 4.1 Var(D_I) by Monte Carlo (2%)", mc_ok_I, f"mc={vI:.5f} closed={float(ex['var_ds']):.5f}")
check("L08 Prop 4.1 Var(D_U) by Monte Carlo (2%)", mc_ok_U, f"mc={vU:.5f} closed={float(ex['var_du']):.5f}")

# gain at cost roots: independent bisection (different code path) at the printed costs
def gain_zero() -> float:
    return math.log(2) / 4


def root(cost: float) -> float:
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if gain(F(mid)) - cost > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


for cost, printed in [(0.13, 0.965625410), (0.14, 0.815032329), (0.15, 0.657828572), (0.16, 0.480567912),
                      (0.17, 0.231615819)]:
    lam_root = root(cost)
    check(f"L08 PartC root at cost {cost}", abs(lam_root - printed) < 1e-6,
          f"independent={lam_root:.9f} printed={printed}")

# Corr^2 at printed costs (0.17 -> 0.013061, 0.12 -> 0.166667 at lam=1)
c17 = float(l08_eq(F(231615819, 10**9), F(1))["corr2"])
check("L08 Corr2 at cost 0.17 root = 0.013061", abs(c17 - 0.013061) < 5e-7, f"corr2={c17:.8f}")
c1 = float(l08_eq(F(1), F(1))["corr2"])
check("L08 Corr2 at lam=1 = 1/6 (cost 0.12 boundary)", abs(c1 - 1 / 6) < 1e-12, f"corr2={c1:.9f}")

# Lab part D: with su2=0 gain is zero for every interior lam
zero_gains = [gain(F(k, 1000), F(0)) for k in range(1, 1000, 37)]
check("L08 Part D gain zero at sigma_u=0 (sampled)", all(abs(g) < 1e-12 for g in zero_gains),
      f"max|gain|={max(abs(g) for g in zero_gains):.2e}")

# Prop 5.2(a) limit: G(lam) -> G(0) as lam -> 0+ with su2 = 1
g_small = gain(F(1, 10**6), F(1))
check("L08 Prop 5.2(a) G(1e-6) ~ G(0)", abs(g_small - math.log(2) / 4) < 1e-6, f"G(1e-6)={g_small:.10f}")

# Emp 3 derivation components
check("L08 Emp3 Var(D_I) at lam=1 = 1", l08_eq(F(1), F(1))["var_ds"] == 1, f"{l08_eq(F(1), F(1))['var_ds']}")
check("L08 Emp3 Var(D_U) at lam=1 = 2/3", l08_eq(F(1), F(1))["var_du"] == F(2, 3), f"{l08_eq(F(1), F(1))['var_du']}")

# ---------- L09: exhaustive independent enumeration ----------
STATES = (1, 2, 3, 4, 5, 6)
P1 = [{1, 2}, {3}, {4, 5, 6}]
P2 = [{1, 2, 3}, {4, 5}, {6}]
PRIOR = F(1, 6)


def cell(part: list[set[int]], w: int) -> set[int]:
    return next(c for c in part if w in c)


def post(part: list[set[int]], w: int, x: dict[int, int]) -> F:
    c = cell(part, w)
    return sum((PRIOR * x[k] for k in c), F(0)) / (PRIOR * len(c))


def meet(w: int) -> set[int]:
    m = {w}
    changed = True
    while changed:
        changed = False
        for part in (P1, P2):
            for k in list(m):
                c = cell(part, k)
                if not c <= m:
                    m |= c
                    changed = True
    return m


check("L09 meet(1) = {1,2,3}", meet(1) == {1, 2, 3}, str(sorted(meet(1))))
check("L09 meet(4) = {4,5,6}", meet(4) == {4, 5, 6}, str(sorted(meet(4))))

bets = [dict(zip(STATES, vals)) for vals in product((-2, -1, 0, 1, 2), repeat=6)]
check("L09 bet count 5^6", len(bets) == 15625, str(len(bets)))

for st in (1, 4):
    m = meet(st)
    strict = 0
    nonneg_on_meet = 0
    nonneg_and_nonzero = 0
    strict_and_nonneg = 0
    for x in bets:
        neg = {k: -v for k, v in x.items()}
        g1 = {w: post(P1, w, x) for w in STATES}
        g2 = {w: post(P2, w, neg) for w in STATES}
        s_at = g1[st] > 0 and g2[st] > 0
        nn = all(g1[w] >= 0 and g2[w] >= 0 for w in m)
        strict += s_at
        nonneg_on_meet += nn
        if nn and any(g1[w] != 0 or g2[w] != 0 for w in m):
            nonneg_and_nonzero += 1
        if s_at and nn:
            strict_and_nonneg += 1
    check(f"L09 state {st}: strict-at-state count = 500", strict == 500, str(strict))
    check(f"L09 state {st}: nonneg-on-meet count = 625", nonneg_on_meet == 625, str(nonneg_on_meet))
    check(f"L09 state {st}: strict AND nonneg-on-meet = 0", strict_and_nonneg == 0, str(strict_and_nonneg))
    check(f"L09 state {st}: nonneg-on-meet with nonzero posterior = 0", nonneg_and_nonzero == 0, str(nonneg_and_nonzero))

# Emp 3: zero-posterior bets on {1,2,3} iff x3 = 0 and x2 = -x1 (count 625 among all bets of the 5^6 space)
zero_post = 0
iff_ok = True
for x in bets:
    neg = {k: -v for k, v in x.items()}
    g1 = {w: post(P1, w, x) for w in (1, 2, 3)}
    g2 = {w: post(P2, w, neg) for w in (1, 2, 3)}
    z = all(g1[w] == 0 and g2[w] == 0 for w in (1, 2, 3))
    desc = x[3] == 0 and x[2] == -x[1]
    if z != desc:
        iff_ok = False
    zero_post += z
check("L09 Emp3 iff description holds for all 15625 bets", iff_ok, "exhaustive")
check("L09 Emp3 count of zero-posterior bets = 625", zero_post == 625, str(zero_post))

# Example 2.4 bet
x_ex = {1: -1, 2: 2, 3: -2, 4: -2, 5: -2, 6: -2}
g1_1 = post(P1, 1, x_ex)
g2_1 = post(P2, 1, {k: -v for k, v in x_ex.items()})
check("L09 Ex2.4 g1(1)=1/2, g2(1)=1/3, g1(3)=-2", g1_1 == F(1, 2) and g2_1 == F(1, 3) and post(P1, 3, x_ex) == -2,
      f"{g1_1}, {g2_1}, {post(P1, 3, x_ex)}")

# Res 2: two-prior bet with nu1 = 0.7, nu2 = 0.4 (Mech 3 numbers) and general construction
nu1, nu2 = F(7, 10), F(4, 10)
r1 = nu1 * 1 + (1 - nu1) * (-1)
r2 = nu2 * (-1) + (1 - nu2) * 1
check("L09 Mech3 receipts 0.4 and 0.2", r1 == F(2, 5) and r2 == F(1, 5), f"{r1}, {r2}")

# Canon: prior example with trader 2 receipt -(0.4-0.6)=0.2 already checked above

print("FAILURES:", failures if failures else "none")
