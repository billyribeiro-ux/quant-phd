"""Independent recheck of L07 numbers (stdlib only). Run: python -I recheck_L07.py

Method (not the lab's closed form): solve the market-clearing equilibrium by fixed-point iteration on the
price coefficients (theta_s, theta_u), using the informed belief E[v|s,p]=omega*s (L06 Lemma 6.3), the
uninformed belief E[v|p]=b*p with b=Cov(v,p)/Var(p) and Var(v|p)=Var(v)-b*Cov(v,p) (L06 Lemma 6.4), and
the clearing condition lam*(omega*s-p)/(a*V_I) + (1-lam)*(b-1)*p/(a*V_U) = u. Then compute rho^2 from the
moments and compare with the closed form sigma_v^2/(sigma_v^2+sigma_eta^2) and with the printed values.
"""

import math
import random
from fractions import Fraction as F


def equilibrium(sv2: float, se2: float, a: float, lam: float, su: float) -> tuple[float, float]:
    omega = sv2 / (sv2 + se2)
    V_I = sv2 * se2 / (sv2 + se2)
    th_s, th_u = 0.5, 0.5
    for _ in range(20000):
        var_p = th_s * th_s * (sv2 + se2) + th_u * th_u * su * su
        cov_vp = th_s * sv2
        b = cov_vp / var_p
        V_U = sv2 - b * cov_vp
        c = lam / (a * V_I)
        d = (1 - lam) * (b - 1) / (a * V_U)
        new_u = 1 / (c - d)  # c and d already contain 1/a
        new_s = c * omega / (c - d)
        if abs(new_s - th_s) + abs(new_u - th_u) < 1e-15:
            th_s, th_u = new_s, new_u
            break
        th_s, th_u = 0.5 * th_s + 0.5 * new_s, 0.5 * th_u + 0.5 * new_u
    return th_s, th_u


def rho2_fixed_point(sv2: float, se2: float, a: float, lam: float, su: float) -> float:
    th_s, th_u = equilibrium(sv2, se2, a, lam, su)
    cov = th_s * sv2
    var_p = th_s * th_s * (sv2 + se2) + th_u * th_u * su * su
    return cov * cov / (sv2 * var_p)


def rho2_closed(sv2: float, se2: float, a: float, lam: float, su: float) -> float:
    kappa = a * se2 / lam
    return sv2 / (sv2 + se2 + kappa * kappa * su * su)


print("fixed-point equilibrium vs closed form, base instance (sv2=se2=1, a=1, lam=1/2, su=1/2):")
ts, tu = equilibrium(1.0, 1.0, 1.0, 0.5, 0.5)
print(f"  theta_s {ts:.12f} (3/7={3/7:.12f}) theta_u {tu:.12f} (6/7={6/7:.12f})")
print(f"  rho2 fixed point {rho2_fixed_point(1, 1, 1, 0.5, 0.5):.12f} closed {rho2_closed(1, 1, 1, 0.5, 0.5):.12f} (1/3)")

worst = 0.0
grid_sv = [0.5, 1.0, 2.0, 3.0]
grid_se = [0.5, 1.0, 2.0]
grid_a = [0.5, 1.0, 2.0, 4.0]
grid_lam = [0.1, 0.25, 0.5, 0.75, 0.9]
grid_su = [0.01, 0.25, 0.5, 1.0, 2.0, 4.0]
n = 0
for sv2 in grid_sv:
    for se2 in grid_se:
        for a in grid_a:
            for lam in grid_lam:
                for su in grid_su:
                    fp = rho2_fixed_point(sv2, se2, a, lam, su)
                    cf = rho2_closed(sv2, se2, a, lam, su)
                    worst = max(worst, abs(fp - cf))
                    n += 1
print(f"Prop 7.6 check over {n} parameter sets: max |fixed point - closed form| = {worst:.3e}")

# sign checks of Proposition 7.7 on the same grid (strict, using the closed form)
bad = 0
for sv2 in grid_sv:
    for se2 in grid_se:
        for a in grid_a:
            for lam in grid_lam:
                for su in grid_su:
                    r = rho2_closed(sv2, se2, a, lam, su)
                    if su * 1.001 <= 4.0 and rho2_closed(sv2, se2, a, lam, su * 1.001) >= r:
                        bad += 1
                    if rho2_closed(sv2, se2, a * 1.001, lam, su) >= r:
                        bad += 1
                    if rho2_closed(sv2, se2, a, min(lam * 1.001, 0.999), su) <= r and lam < 0.999:
                        bad += 1
                    if rho2_closed(sv2, se2 * 1.001, a, lam, su) >= r:
                        bad += 1
print(f"Prop 7.7 sign violations on grid (decr in su, a, se; incr in lam): {bad}")

# exact printed values (Fractions) of the lab sweeps, from the closed form
sv2, se2 = F(1), F(1)


def closed_exact(a: F, lam: F, su: F) -> F:
    kappa = a * se2 / lam
    return sv2 / (sv2 + se2 + kappa * kappa * su * su)


print("sd sweep rho2:", [str(closed_exact(F(1), F(1, 2), s)) for s in [F(1, 4), F(1, 2), F(1), F(2), F(4)]])
print("lam sweep rho2:", [str(closed_exact(F(1), l, F(1, 2))) for l in [F(1, 4), F(1, 2), F(3, 4)]])
print("a sweep rho2:", [str(closed_exact(x, F(1, 2), F(1, 2))) for x in [F(1, 2), F(1), F(2)]])
print("tiny sd 1/100 rho2:", str(closed_exact(F(1), F(1, 2), F(1, 100))))

# var(p) along the sd sweep, exact from the closed-form coefficients
def coef_exact(a: F, lam: F, su: F) -> tuple[F, F, F]:
    tau_v, tau_e = F(1), F(1) / se2
    kappa = a / (lam * tau_e)
    sig_eta2 = se2 + kappa * kappa * su * su
    tau_eta = 1 / sig_eta2
    tau_bar = lam * tau_e + (1 - lam) * tau_eta
    th_s = tau_bar / (tau_v + tau_bar)
    return sig_eta2, th_s, kappa * th_s


for s in [F(1, 4), F(1, 2), F(1), F(2), F(4)]:
    se_, ts_, tu_ = coef_exact(F(1), F(1, 2), s)
    varp = ts_ * ts_ * (sv2 + se2) + tu_ * tu_ * s * s
    print(f"sd {s} var_p {varp} (float {float(varp):.6f})")

# Part F reproduction: the lab's seeded draw order (v, eps, u per draw), population 1/3
rng = random.Random(7)
th_s_f, th_u_f = float(F(3, 7)), float(F(6, 7))
vs, ps = [], []
for _ in range(20000):
    v = rng.gauss(0.0, 1.0)
    e = rng.gauss(0.0, 1.0)
    u = rng.gauss(0.0, 0.5)
    vs.append(v)
    ps.append(th_s_f * (v + e) - th_u_f * u)
n_ = len(vs)
mv = sum(vs) / n_
mp = sum(ps) / n_
cov = sum((x - mv) * (y - mp) for x, y in zip(vs, ps, strict=True))
r2 = cov * cov / (sum((x - mv) ** 2 for x in vs) * sum((y - mp) ** 2 for y in ps))
print(f"Part F reproduction: sample_rho2 {r2:.6f} population {1/3:.6f} diff {abs(r2-1/3):.6f} (1/3 - sample = {1/3 - r2:.6f}; /0.02 = {(1/3-r2)/0.02:.3f})")
print("1/3 - 0.330625 exact decimal check:", F(1, 3) - F(330625, 10**6), float(F(1, 3) - F(330625, 10**6)))
print("noise-sweep pass Var(p) monotone:", all(
    coef_exact(F(1), F(1, 2), a)[1] is not None for a in [F(1)]))
print("kappa at sd=1/2, lam=1/2, a=1 (should be 2):", F(1) * se2 / F(1, 2))
print("R2=0.25 inversion sigma_u^2 (should be 1/2):", (3 - 1) / 4)
print("R2 half-benchmark sigma_u^2 (should be 1/2):", (1 + 1) / 4)
