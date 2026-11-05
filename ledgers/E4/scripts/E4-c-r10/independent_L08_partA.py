"""Round 10, slice E4-c: recompute the L08 Part A seeded sample slope (seed 20261103, 20000 draws, lam = 0.5) from the
closed-form price written independently: theta_s = tau_bar/(tau_v+tau_bar) and kappa*beta = kappa*A/(tau_v+A)."""
import random

a, sv2, se2, su2, lam = 2.0, 1.0, 1.0, 1.0, 0.5
kappa = a * se2 / lam
se_eta2 = se2 + kappa * kappa * su2
A = lam / se2 + (1 - lam) / se_eta2
beta = A / (1.0 + A)
rng = random.Random(20261103)
vs, ps = [], []
for _ in range(20000):
    v = rng.gauss(0.0, 1.0); eps = rng.gauss(0.0, 1.0); u = rng.gauss(0.0, 1.0)
    s = v + eps
    vs.append(v); ps.append(beta * s - kappa * beta * u)
n = len(vs); mv = sum(vs) / n; mp = sum(ps) / n
cov = sum((x - mv) * (y - mp) for x, y in zip(vs, ps)) / n
varp = sum((y - mp) ** 2 for y in ps) / n
b_y = (1 / se_eta2) / (1 + 1 / se_eta2)
print(f"sample slope {cov / varp:.4f}  formula b_y/beta {b_y / beta:.6f}  beta {beta:.6f}  b_y {b_y:.6f}")
