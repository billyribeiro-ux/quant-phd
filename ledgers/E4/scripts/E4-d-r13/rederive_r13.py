"""Independent re-derivation of the E4 project model (round 13, verifier for slice d).

Nothing here reads the page or the reference solution. The model is set up as a Gaussian vector Z = (v, eps, u)
with independent components of variances (1/tau_v, 1/tau_e, sigma^2). Every quantity is computed from covariance
matrices and linear algebra:

* the linear price p = b_s s + b_u u is found as the root of the market-clearing residual, where each investor's
  demand is the regression (conditional mean) of v on its information minus p, divided by a times the conditional
  variance (Lemma 1 of the page, applied as a formula on covariances);
* the expected utilities are exact Gaussian quadratic-form integrals E[exp(-a Z'SZ)] = det(I + 2 a Sigma S)^(-1/2);
* the informativeness is Corr(v, p)^2 from the covariance matrix.

Usage: .venv/bin/python -I ledgers/E4/scripts/E4-d-r13/rederive_r13.py
"""

from __future__ import annotations

import math

import numpy as np
from scipy.optimize import brentq, least_squares

A = 2.0
TAU_V = 1.0
TAU_E = 1.0


def sigma_matrix(sd: float) -> np.ndarray:
    return np.diag([1.0 / TAU_V, 1.0 / TAU_E, sd * sd])


def rows(bs: float, bu: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    v = np.array([1.0, 0.0, 0.0])
    s = np.array([1.0, 1.0, 0.0])
    u = np.array([0.0, 0.0, 1.0])
    p = bs * s + bu * u
    return v, s, p


def demands(lam: float, bs: float, bu: float, sd: float) -> tuple[np.ndarray, np.ndarray]:
    """Linear forms (rows over Z) of the informed and uninformed demands, from regressions on covariances."""
    sig = sigma_matrix(sd)
    v, s, p = rows(bs, bu)
    cov = lambda x, y: x @ sig @ y  # noqa: E731
    # informed: information (s, p)
    info = np.vstack([s, p])
    gram = np.array([[cov(info[i], info[j]) for j in range(2)] for i in range(2)])
    cvi = np.array([cov(v, info[i]) for i in range(2)])
    beta = np.linalg.solve(gram, cvi)
    var_v_given_info = cov(v, v) - beta @ cvi
    x_i = (beta[0] * s + beta[1] * p - p) / (A * var_v_given_info)
    # uninformed: information (p)
    cvp = cov(v, p)
    beta_u = cvp / cov(p, p)
    var_v_given_p = cov(v, v) - cvp * cvp / cov(p, p)
    x_u = (beta_u * p - p) / (A * var_v_given_p)
    return x_i, x_u


def clearing_residual(params: np.ndarray, lam: float, sd: float) -> np.ndarray:
    bs, bu = params
    x_i, x_u = demands(lam, bs, bu, sd)
    u = np.array([0.0, 0.0, 1.0])
    return lam * x_i + (1.0 - lam) * x_u - u


def equilibrium(lam: float, sd: float) -> tuple[float, float, float]:
    """(b_s, b_u, residual norm) from least squares on the clearing residual, started at the page's closed form."""
    ty = lam * lam * TAU_E * TAU_E / (lam * lam * TAU_E + A * A * sd * sd)
    denom = lam * (TAU_V + TAU_E) + (1 - lam) * (TAU_V + ty)
    bs0 = (lam * TAU_E + (1 - lam) * ty) / denom
    bu0 = -A * bs0 / (lam * TAU_E)
    res = least_squares(
        lambda x: clearing_residual(x, lam, sd), x0=np.array([bs0, bu0]), xtol=1e-15, ftol=1e-15, gtol=1e-15
    )
    return float(res.x[0]), float(res.x[1]), float(np.linalg.norm(clearing_residual(res.x, lam, sd)))


def eu_quadratic(l: np.ndarray, m: np.ndarray, sd: float) -> float:
    """E[exp(-a (l.Z)(m.Z))] for Z ~ N(0, Sigma), by the Gaussian quadratic-form identity det(I + 2 a Sigma S)^(-1/2)."""
    sig = sigma_matrix(sd)
    s_mat = 0.5 * (np.outer(l, m) + np.outer(m, l))
    mat = np.eye(3) + 2.0 * A * sig @ s_mat
    eig = np.linalg.eigvals(mat)
    # the identity needs the matrix to be positive definite for the integral to converge
    if np.min(np.real(eig)) <= 0.0:
        raise ValueError("integral does not converge")
    return float(np.linalg.det(mat) ** -0.5)


def gap_independent(lam: float, sd: float, cost: float) -> tuple[float, float, float, float]:
    """(G, E[U_I], E[U_U], informativeness) at informed fraction lam > 0, computed from linear forms only."""
    bs, bu, res = equilibrium(lam, sd)
    if res > 1e-9:
        raise RuntimeError(f"clearing residual {res}")
    v, s, p = rows(bs, bu)
    x_i, x_u = demands(lam, bs, bu, sd)
    vmp = v - p
    eu_i = -math.exp(A * cost) * eu_quadratic(x_i, vmp, sd)
    eu_u = -eu_quadratic(x_u, vmp, sd)
    sig = sigma_matrix(sd)
    cov_vp = v @ sig @ p
    corr2 = cov_vp * cov_vp / ((v @ sig @ v) * (p @ sig @ p))
    return eu_i - eu_u, eu_i, eu_u, float(corr2)


def page_gap(lam: float, sd: float, cost: float) -> float:
    ty = lam * lam * TAU_E * TAU_E / (lam * lam * TAU_E + A * A * sd * sd)
    denom = lam * (TAU_V + TAU_E) + (1 - lam) * (TAU_V + ty)
    bs = (lam * TAU_E + (1 - lam) * ty) / denom
    bu = -A * bs / (lam * TAU_E)
    r = ty / (TAU_V + ty) - bs
    f_u = (1 + r * r * (TAU_V + ty) * (1 / TAU_V + 1 / ty)) ** -0.5
    prec = TAU_V + TAU_E
    slope = TAU_E / prec - bs
    var_gap = slope * slope * (1 / TAU_V + 1 / TAU_E) + bu * bu * sd * sd
    f_i = (1 + prec * var_gap) ** -0.5
    return f_u - math.exp(A * cost) * f_i


def page_gap_at_zero(sd: float, cost: float) -> float:
    return (1 + A * A * sd * sd / TAU_V) ** -0.5 - math.exp(A * cost) * (
        1 + TAU_E / TAU_V + (TAU_V + TAU_E) * A * A * sd * sd / (TAU_V * TAU_V)
    ) ** -0.5


def page_informativeness(lam: float, sd: float) -> float:
    ty = lam * lam * TAU_E * TAU_E / (lam * lam * TAU_E + A * A * sd * sd)
    return ty / (TAU_V + ty)


def main() -> None:
    print("== 1. independent gap vs page formula, and informativeness, on a lambda grid")
    worst_gap = 0.0
    worst_corr = 0.0
    for sd, cost in [(0.6, 0.13), (0.7, 0.14), (0.5, 0.12), (0.75, 0.15), (0.625, 0.135), (1.0, 0.1), (0.3, 0.05)]:
        for lam in [0.05, 0.2, 0.4, 0.57937525, 0.7, 0.9, 1.0]:
            g_ind, eu_i, eu_u, corr2 = gap_independent(lam, sd, cost)
            g_page = page_gap(lam, sd, cost)
            worst_gap = max(worst_gap, abs(g_ind - g_page))
            worst_corr = max(worst_corr, abs(corr2 - page_informativeness(lam, sd)))
    print(f"max |G_indep - G_page| over grid = {worst_gap:.3e}")
    print(f"max |Corr^2_indep - tau_y/(tau_v+tau_y)| over grid = {worst_corr:.3e}")

    print("== 2. the limit G(0+) at small lambda vs the page's closed form")
    for sd, cost in [(0.6, 0.13), (0.7, 0.14), (0.5, 0.15)]:
        g_small, _, _, _ = gap_independent(1e-7, sd, cost)
        print(f"sd={sd} c={cost}: G(1e-7)={g_small:+.10f}  page G(0+)={page_gap_at_zero(sd, cost):+.10f}")

    print("== 3. Lab 1 and Lab 2 printed numbers, recomputed")
    for sd, cost in [(0.60, 0.13), (0.70, 0.14)]:
        g0 = page_gap_at_zero(sd, cost)
        g1 = page_gap(1.0, sd, cost)
        lo, hi = 1e-300, 1.0
        root = brentq(lambda lam: page_gap(lam, sd, cost), 1e-9, 1.0, xtol=1e-16, rtol=1e-15)
        print(f"sd={sd} c={cost}: G(0+)={g0:+.6f} G(1)={g1:+.6f} root={root:.8f} inform={page_informativeness(root, sd):.8f}")
        ty = page_informativeness(root, sd) / (1 - page_informativeness(root, sd))
        bs, bu, _ = equilibrium(root, sd)
        print(f"   b_u/b_s independent={bu / bs:.8f}  -a/(lam tau_e)={-A / (root * TAU_E):.8f}  tau_y={ty:.8f}")
        print(f"   tau_bar={(TAU_V + TAU_E) * math.exp(-2 * A * cost) - TAU_V:.8f}  closed form 1-e^(2ac)tau_v/(tau_v+tau_e)="
              f"{1 - math.exp(2 * A * cost) * TAU_V / (TAU_V + TAU_E):.8f}")
        _ = (lo, hi)

    print("== 4. Lab 3 grid: unrounded ratios, constancy of informativeness, closed-form agreement")
    closed = lambda sd, c: 0.0 if (2 * math.exp(-4 * c) - 1) <= 0 else (  # noqa: E731
        1.0 if (2 * math.exp(-4 * c) - 1) >= 1 / (1 + 4 * sd * sd) else
        2 * sd * math.sqrt((2 * math.exp(-4 * c) - 1) / (1 - (2 * math.exp(-4 * c) - 1))))
    frac: dict[tuple[float, float], float] = {}
    for sd in (0.5, 0.625, 0.75):
        for cost in (0.120, 0.135, 0.150):
            tbar = 2 * math.exp(-4 * cost) - 1
            interior = 0.0 < tbar < 1 / (1 + 4 * sd * sd)
            lam = closed(sd, cost)
            frac[(sd, cost)] = lam
            pi = 1 - math.exp(4 * cost) / 2
            print(f"sd={sd} c={cost}: lam*={lam:.10f} interior={interior} inform={pi:.10f}")
    print(f"ratio lam(0.625)/lam(0.5) at c=0.120 (unrounded) = {frac[(0.625, 0.120)] / frac[(0.5, 0.120)]:.12f}")
    print(f"ratio lam(0.750)/lam(0.5) at c=0.120 (unrounded) = {frac[(0.75, 0.120)] / frac[(0.5, 0.120)]:.12f}")
    print(f"displayed ratio 0.6978/0.5582 = {0.6978 / 0.5582:.6f}; 0.8373/0.5582 = {0.8373 / 0.5582:.6f}")

    print("== 4b. Lab 3 bisection-vs-closed-form and gap sign, page's own grid, from the page's gap formula")
    for sd in (0.5, 0.625, 0.75):
        for cost in (0.120, 0.135, 0.150):
            lam = frac[(sd, cost)]
            if 0 < lam < 1:
                print(f"sd={sd} c={cost}: gap at closed-form root (page formula) = {page_gap(lam, sd, cost):+.3e}"
                      f"  independent = {gap_independent(lam, sd, cost)[0]:+.3e}")

    print("== 5. Box: sign pattern on the 22 by 22 grid of the autograder's box")
    inside = 0
    for i in range(22):
        for j in range(22):
            sd = 0.500 + 0.250 * i / 21.0
            cost = 0.120 + 0.030 * j / 21.0
            if page_gap_at_zero(sd, cost) > 0.0 and page_gap(1.0, sd, cost) < 0.0:
                inside += 1
    print(f"box points with interior fraction (page formulas): {inside} of 484")

    print("== 6. Bound numbers on the page: tau_bar at box corners, tau_y(1) lower bound")
    print(f"tau_bar(0.150) = {2 * math.exp(-0.6) - 1:.10f}")
    print(f"tau_bar(0.120) = {2 * math.exp(-0.48) - 1:.10f}")
    print(f"1/(1+4*0.75^2) = {1 / (1 + 4 * 0.75 * 0.75):.10f}")
    print(f"2^-240 = {2.0 ** -240:.4e}; 2^-240 / 1e-12 = {2.0 ** -240 / 1e-12:.4e}; 2^-200 = {2.0 ** -200:.4e}")
    print(f"2^-200 / 1e-12 = {2.0 ** -200 / 1e-12:.4e}; 1e-10 * 2e-51 = {1e-10 * 2e-51:.4e}")


if __name__ == "__main__":
    main()
