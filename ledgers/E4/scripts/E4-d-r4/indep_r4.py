"""Independent numerical checks for E4 project page (slice d, round 4). Usage: python -I indep_r4.py <repo-root>

1. Equilibrium by clearing: for lam, sd the reference price (b_s, b_u) is checked against market clearing computed from
   Gaussian conditioning with moments taken from the covariance matrix (not from the page's closed forms).
2. Expected-utility gap by 3-D trapezoid quadrature over (v, eps, u) with the actual CARA demands, compared with the
   reference indifference_gap (which uses the page's Gaussian closed forms).
3. Proposition 4 closed form vs reference bisection on the 3x3 grid, Lab 1/Lab 2 roots, the 22x22 box, and tiny sd.
4. Exemplar B displayed ratios (0.6978/0.5582, 0.8373/0.5582).
"""

import importlib.util
import math
import sys
from pathlib import Path

import numpy as np

root = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("ref", root / "course/modules/E/E4/grader/reference.py")
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)
A, TV, TE = 2.0, 1.0, 1.0


def clearing_residual(lam, sd, bs, bu):
    """Residual of lam x_I + (1-lam) x_U - u (in coefficients of s and u) with demands from conditional moments."""
    Vs = 1 / TV + 1 / TE
    cov_vs = 1 / TV
    # observed vector for informed: (s, p); for uninformed: (p)
    Vp = bs * bs * Vs + bu * bu * sd * sd
    cov_sp = bs * Vs
    cov_vp = bs * cov_vs
    # informed: regress v on (s, p)
    C = np.array([[Vs, cov_sp], [cov_sp, Vp]])
    beta_I = np.linalg.solve(C, np.array([cov_vs, cov_vp]))
    Vcond_I = 1 / TV - beta_I @ np.array([cov_vs, cov_vp])
    # uninformed: regress v on p
    beta_U = cov_vp / Vp
    Vcond_U = 1 / TV - beta_U * cov_vp

    def xI(s, p):
        m = beta_I[0] * s + beta_I[1] * p
        return (m - p) / (A * Vcond_I)

    def xU(p):
        m = beta_U * p
        return (m - p) / (A * Vcond_U)

    res = []
    for s, u in [(1.0, 0.0), (0.0, 1.0), (0.7, -0.4)]:
        p = bs * s + bu * u
        res.append(lam * xI(s, p) + (1 - lam) * xU(p) - u)
    return max(abs(r) for r in res)


def quad_gap(lam, sd, cost, h=0.1, L=8.0):
    """E[U_I] - E[U_U] by trapezoid over standard normals (z1,z2,z3): v=z1, eps=z2, u=sd*z3 (variances as in the model)."""
    bs, bu, _ = ref.price_coefficients(lam, sd)
    Vs = 1 / TV + 1 / TE
    cov_vs = 1 / TV
    Vp = bs * bs * Vs + bu * bu * sd * sd
    cov_sp = bs * Vs
    cov_vp = bs * cov_vs
    C = np.array([[Vs, cov_sp], [cov_sp, Vp]])
    beta_I = np.linalg.solve(C, np.array([cov_vs, cov_vp]))
    Vcond_I = 1 / TV - beta_I @ np.array([cov_vs, cov_vp])
    beta_U = cov_vp / Vp
    Vcond_U = 1 / TV - beta_U * cov_vp
    g = np.arange(-L, L + h / 2, h)
    w = np.exp(-0.5 * g * g)
    w = w / w.sum()  # normalized trapezoid weights for the standard normal
    z2, z3 = np.meshgrid(g, g, indexing="ij")
    W23 = np.outer(w, w)
    EI = 0.0
    EU = 0.0
    for z1, w1 in zip(g, w):
        v = z1 / math.sqrt(TV)
        eps = z2 / math.sqrt(TE)
        u = sd * z3
        s = v + eps
        p = bs * s + bu * u
        # informed
        m = beta_I[0] * s + beta_I[1] * p
        x = (m - p) / (A * Vcond_I)
        EI += w1 * np.sum(W23 * np.exp(-A * (x * (v - p) - cost)))
        # uninformed
        mu = beta_U * p
        xu = (mu - p) / (A * Vcond_U)
        EU += w1 * np.sum(W23 * np.exp(-A * (xu * (v - p))))
    return -EU * 0 - (-EI) + (-EU) * 0 + 0.0 - (-(EU)) if False else (-EI) - (-EU)


def fmt(x):
    return f"{x:.12g}"


print("1. clearing residual at reference price (must be ~0):")
for lam, sd in [(0.57937525, 0.6), (0.5, 0.5), (0.9, 0.75), (1e-3, 0.6), (1.0, 2.0)]:
    bs, bu, _ = ref.price_coefficients(lam, sd)
    print("   lam", lam, "sd", sd, "residual", f"{clearing_residual(lam, sd, bs, bu):.2e}")

print("2. gap by quadrature vs reference indifference_gap (interior lam):")
for lam, sd, c in [(0.5, 0.6, 0.13), (0.57052263, 0.7, 0.14), (0.8, 0.5, 0.12)]:
    q = quad_gap(lam, sd, c)
    r = ref.indifference_gap(lam, sd, c)
    print(f"   lam {lam} sd {sd} c {c}: quad {q:+.10f} ref {r:+.10f} diff {abs(q - r):.2e}")

print("3. reference root vs Proposition 4 closed form:")
def closed(sd, c):
    t = (TV + TE) * math.exp(-2 * A * c) - TV
    if t <= 0:
        return 0.0
    if t >= TE * TE / (TE + A * A * sd * sd):
        return 1.0
    return A * sd * math.sqrt(t / (TE * (TE - t)))
worst = 0.0
for sd in (0.500, 0.625, 0.750):
    for c in (0.120, 0.135, 0.150):
        worst = max(worst, abs(ref.solve_model(sd, c)["informed_fraction"] - closed(sd, c)))
print("   worst |bisection - closed| on 3x3 grid:", f"{worst:.2e}")
print("   Lab1 root (0.6, 0.13):", fmt(ref.solve_model(0.6, 0.13)["informed_fraction"]), "closed", fmt(closed(0.6, 0.13)))
print("   Lab2 root (0.7, 0.14):", fmt(ref.solve_model(0.7, 0.14)["informed_fraction"]), "closed", fmt(closed(0.7, 0.14)))
pos = 0
for i in range(22):
    for j in range(22):
        sd = 0.5 + 0.25 * i / 21.0
        c = 0.12 + 0.03 * j / 21.0
        if ref.gap_at_zero(sd, c) > 0 and ref.indifference_gap(1.0, sd, c) < 0:
            pos += 1
print("   box 22x22 interior:", pos, "of", 484)
for sd in (1e-6, 1e-9, 1e-12):
    got = ref.solve_model(sd, 0.13)["informed_fraction"]
    cl = closed(sd, 0.13)
    print(f"   tiny sd {sd}: reference {got:.10e} closed {cl:.10e} rel err {abs(got - cl) / cl:.2e}")
print("4. Exemplar B ratios: 0.6978/0.5582 =", f"{0.6978 / 0.5582:.6f}", " 0.8373/0.5582 =", f"{0.8373 / 0.5582:.6f}")
print("   unrounded ratio 0.625/0.5 closed:", f"{closed(0.625, 0.12) / closed(0.5, 0.12):.12f}")
