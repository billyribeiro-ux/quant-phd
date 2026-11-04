"""Independent recheck of L08 numbers (stdlib only). Run: python -I recheck_L08.py

Route (not the lab's closed forms): solve the market-clearing price coefficients (theta_s, theta_u) by fixed
point on lam*(b_s*s - p)/(a*V_I) + (1-lam)*(b-1)*p/(a*V_U) = u, with b = Cov(v,p)/Var(p), V_U = Var(v) - b*Cov(v,p),
b_s = sv2/(sv2+se2), V_I = sv2*se2/(sv2+se2) (L08 Lemma 2.5 and Corollary 2.4(a)). Then compute the demand gaps
directly as random variables: D_I = b_s*s - p and D_U = (b-1)*p, their variances from (s,u) independence, and
G(lam) = (1/(2a)) ln((1+Var(D_I)/V_I)/(1+Var(D_U)/V_U)) (Definition 4.3). Bisection for lam* with the lab's rules.
"""

import math
import random

SV2 = 1.0
SE2 = 1.0
A = 2.0
SU2 = 1.0


def solve(lam: float, su2: float, a: float = A) -> tuple[float, float, float, float]:
    """Return (theta_s, theta_u, b, Var(p)) for the linear equilibrium price p = theta_s*s - theta_u*u."""
    b_s = SV2 / (SV2 + SE2)
    V_I = SV2 * SE2 / (SV2 + SE2)
    th_s, th_u = 0.5, 0.5
    for _ in range(200000):
        var_p = th_s * th_s * (SV2 + SE2) + th_u * th_u * su2
        cov = th_s * SV2
        b = cov / var_p
        V_U = SV2 - b * cov
        c = lam / (a * V_I)
        d = (1 - lam) * (b - 1) / (a * V_U)
        new_u = 1 / (c - d)
        new_s = c * b_s / (c - d)
        if abs(new_s - th_s) + abs(new_u - th_u) < 1e-15:
            th_s, th_u = new_s, new_u
            break
        th_s, th_u = 0.5 * th_s + 0.5 * new_s, 0.5 * th_u + 0.5 * new_u
    var_p = th_s * th_s * (SV2 + SE2) + th_u * th_u * su2
    return th_s, th_u, cov_over(th_s, var_p), var_p


def cov_over(th_s: float, var_p: float) -> float:
    return th_s * SV2 / var_p


def gain(lam: float, su2: float = SU2, a: float = A) -> float:
    if lam == 0.0:
        # no informed trader: p = -a*SV2*u (prior mean 0); uninformed gap D_U = a*SV2*u
        b_s = SV2 / (SV2 + SE2)
        V_I = SV2 * SE2 / (SV2 + SE2)
        var_di = (b_s * b_s) * (SV2 + SE2) + (a * SV2) ** 2 * su2
        var_du = (a * SV2) ** 2 * su2
        V_U = SV2
        return math.log((1 + var_di / V_I) / (1 + var_du / V_U)) / (2 * a)
    th_s, th_u, b, var_p = solve(lam, su2, a)
    b_s = SV2 / (SV2 + SE2)
    V_I = SV2 * SE2 / (SV2 + SE2)
    cov = th_s * SV2
    b = cov / var_p
    V_U = SV2 - b * cov
    var_di = (b_s - th_s) ** 2 * (SV2 + SE2) + th_u ** 2 * su2
    var_du = (b - 1) ** 2 * var_p
    return math.log((1 + var_di / V_I) / (1 + var_du / V_U)) / (2 * a)


def corr2(lam: float, su2: float = SU2, a: float = A) -> float:
    if lam == 0.0:
        return 0.0
    th_s, th_u, b, var_p = solve(lam, su2, a)
    cov = th_s * SV2
    return cov * cov / (SV2 * var_p)


print("independent route vs printed values (a=2, unit variances, sigma_u^2=1)")
g0 = gain(0.0)
g1 = gain(1.0)
gm = gain(0.5)
print(f"gain(0) = {g0:.6f} (printed 0.173287; ln2/4 = {math.log(2)/4:.6f})")
print(f"gain(0.5) = {gm:.6f} (printed 0.158997)")
print(f"gain(1) = {g1:.6f} (printed 0.127706; ln(5/3)/4 = {math.log(5/3)/4:.6f})")
print(f"gain(1e-6) - gain(0) = {gain(1e-6) - g0:.3e} (printed -6.25e-14)")
print(f"ln2/4 exact {math.log(2)/4!r}")
print(f"G(0) closed form ln(1+sv2/se2)/(2a) = {math.log(1 + SV2/SE2)/(2*A)!r}")
print(f"G(1) closed form ln(5/3)/4 = {math.log(5/3)/4!r}")

# grid monotonicity on 999 interior points
grid = [k / 1000 for k in range(1, 1000)]
gs = [gain(x) for x in grid]
cs = [corr2(x) for x in grid]
print("gain strictly decreasing on 999 grid points:", all(gs[i + 1] < gs[i] for i in range(len(gs) - 1)))
print("corr2 strictly increasing on 999 grid points:", all(cs[i + 1] > cs[i] for i in range(len(cs) - 1)))

# bisection with the lab's rules, independent G
def root(cost: float) -> tuple[float, str]:
    if cost >= g0:
        return 0.0, "zero"
    if cost <= g1:
        return 1.0, "one"
    lo, hi = 0.0, 1.0
    while hi - lo > 1e-12:
        mid = 0.5 * (lo + hi)
        if gain(mid) - cost > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi), "bisection"


printed = {
    0.12: (1.0, "one", 0.166667),
    0.13: (0.965625410, "root", 0.158986),
    0.14: (0.815032329, "root", 0.124664),
    0.15: (0.657828572, "root", 0.088941),
    0.16: (0.480567912, "root", 0.051760),
    0.17: (0.231615819, "root", 0.013061),
    0.18: (0.0, "zero", 0.0),
}
for cost, (lam_p, rule_p, c2_p) in printed.items():
    lam, rule = root(cost)
    gap = (g1 - cost) if rule == "one" else ((g0 - cost) if rule == "zero" else gain(lam) - cost)
    c2 = corr2(lam) if lam > 0 else 0.0
    print(f"cost {cost:.2f}: indep lam* = {lam:.9f} ({rule}) printed {lam_p:.9f} |diff| = {abs(lam-lam_p):.2e}; "
          f"gap = {gap:.2e}; corr2 = {c2:.6f} printed {c2_p:.6f} |diff| {abs(c2-c2_p):.1e}")

# Part D: sigma_u^2 = 0 -- gain zero on the grid, and no equilibrium at cost 0.15
gz = [gain(x, su2=0.0) for x in grid]
print(f"sigma_u^2=0: max |gain| on grid = {max(abs(x) for x in gz):.1e}; gain(0) = {gain(0.0, su2=0.0):.6f} (ln2/4)")

# Part A: reproduce the seeded simulation at lam=0.5 (same draw order: v, eps, u)
lam = 0.5
th_s, th_u, _, _ = solve(lam, SU2)
kappa = A * SE2 / lam
beta = (lam * 1.0 + (1 - lam) / (1 + kappa * kappa * SU2)) / (1.0 + (lam * 1.0 + (1 - lam) / (1 + kappa * kappa * SU2)))
rng = random.Random(20261103)
prices, payoffs = [], []
worst = 0.0
p_coef = beta
for _ in range(20000):
    v = rng.gauss(0.0, 1.0)
    e = rng.gauss(0.0, 1.0)
    u = rng.gauss(0.0, 1.0)
    s = v + e
    p = p_coef * s - kappa * p_coef * u
    prices.append(p)
    payoffs.append(v)
n = 20000
mp = sum(prices) / n
mv = sum(payoffs) / n
cov_pv = sum((v - mv) * (p - mp) for v, p in zip(payoffs, prices, strict=True)) / n
var_pp = sum((p - mp) ** 2 for p in prices) / n
slope = cov_pv / var_pp
tau_eta = 1 / (SE2 + kappa * kappa * SU2)
b_y = tau_eta / (1 + tau_eta)
print(f"Part A reproduction: sample slope {slope:.4f}, formula b_y/beta {b_y / beta:.4f}, |diff| {abs(slope - b_y / beta):.4f}")
print(f"Part A: indep equilibrium theta_s {th_s:.9f} theta_u {th_u:.9f}; closed beta {beta:.9f} kappa*beta {kappa*beta:.9f}")
print(f"  check: indep theta_s == beta: {abs(th_s - beta) < 1e-9}; theta_u == kappa*beta: {abs(th_u - kappa*beta) < 1e-9}")
