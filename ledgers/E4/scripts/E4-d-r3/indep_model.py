"""Independent re-derivation of the E4 project model, from the definitions, with no page formula and no grader code.

Method (verifier's own): W = (v, s, u) is jointly Gaussian with covariance Sigma. The price is p = b_s s + b_u u, so
p = c_p . W with c_p = (0, b_s, b_u). Each agent's demand is the Gaussian conditional mean less the price, over a times
the conditional variance (CARA optimum), computed by numerical Gaussian conditioning on its information F (informed:
(s, p); uninformed: p). Each demand is a row r . W. The clearing condition lam r_I + (1 - lam) r_U = e_u is solved for
(b_s, b_u) by a multi-start root finder. Each expected utility is an unconditional Gaussian quadratic-form expectation:
E[exp(-a W' M W)] = det(I + 2 a Sigma M)^(-1/2) with M the symmetric part of r_x (e_v - c_p)'.
Informativeness is Corr(v, p)^2 from Sigma and c_p. Nothing here uses Propositions 1 to 5 except as a comparison target.

Usage: .venv/bin/python -I ledgers/E4/scripts/E4-d-r3/indep_model.py <repo-root>
"""

import itertools
import sys
from typing import Callable

import numpy as np
from scipy.optimize import brentq, fsolve

A = 2.0
TAU_V = 1.0
TAU_E = 1.0


def sigma_matrix(sd: float) -> np.ndarray:
    tv, te = TAU_V, TAU_E
    return np.array(
        [
            [1 / tv, 1 / tv, 0.0],
            [1 / tv, 1 / tv + 1 / te, 0.0],
            [0.0, 0.0, sd * sd],
        ]
    )


E_V = np.array([1.0, 0.0, 0.0])
E_U = np.array([0.0, 0.0, 1.0])


def demand_row(info_rows: np.ndarray, sigma: np.ndarray, c_p: np.ndarray, cost_zero: bool = False) -> np.ndarray:
    """Coefficient row r with x = r . W, where x = (E[v|F] - p) / (a Var(v|F)) and F = info_rows W."""
    s_ff = info_rows @ sigma @ info_rows.T
    s_vf = E_V @ sigma @ info_rows.T
    w = np.linalg.solve(s_ff, s_vf)  # E[v|F] = w . F
    m_row = w @ info_rows  # E[v|F] = m_row . W
    var_cond = (E_V @ sigma @ E_V) - s_vf @ w
    return (m_row - c_p) / (A * var_cond)


def quad_expect(r: np.ndarray, sigma: np.ndarray, c_p: np.ndarray) -> float:
    """E[exp(-a x (v - p))] for x = r . W, unconditional, by the Gaussian quadratic-form determinant."""
    d = E_V - c_p
    m = 0.5 * (np.outer(r, d) + np.outer(d, r))
    return float(np.linalg.det(np.eye(3) + 2 * A * sigma @ m) ** -0.5)


def coefs(bs: float, bu: float, lam: float, sd: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    sigma = sigma_matrix(sd)
    c_p = np.array([0.0, bs, bu])
    info_i = np.array([[0.0, 1.0, 0.0], c_p])
    info_u = np.array([c_p])
    r_i = demand_row(info_i, sigma, c_p) if lam > 0 else np.zeros(3)
    r_u = demand_row(info_u, sigma, c_p)
    return r_i, r_u, c_p, sigma


def clearing_residual(x: np.ndarray, lam: float, sd: float) -> np.ndarray:
    bs, bu = x
    r_i, r_u, _, _ = coefs(bs, bu, lam, sd)
    tot = lam * r_i + (1 - lam) * r_u - E_U
    return np.array([tot[1], tot[2]])


def equilibrium(lam: float, sd: float, start: tuple[float, float] = (0.4, -1.4)) -> tuple[float, float, float]:
    """Solve clearing for (b_s, b_u); return (b_s, b_u, max |residual|)."""
    sol, info, ier, msg = fsolve(clearing_residual, np.array(start), args=(lam, sd), full_output=True, xtol=1e-14)
    res = float(np.max(np.abs(clearing_residual(sol, lam, sd))))
    return float(sol[0]), float(sol[1]), res


def gap_and_info(lam: float, sd: float, cost: float) -> tuple[float, float, float, float]:
    """Return (gap, informativeness, b_s, b_u) at informed fraction lam in (0, 1] (lam = 1 uses hypothetical uninformed)."""
    bs, bu, res = equilibrium(lam, sd)
    assert res < 1e-10, ("clearing residual", lam, sd, res)
    sigma = sigma_matrix(sd)
    r_i, r_u, c_p, _ = coefs(bs, bu, lam, sd)
    f_i = quad_expect(r_i, sigma, c_p)
    f_u = quad_expect(r_u, sigma, c_p)
    gap = f_u - np.exp(A * cost) * f_i
    cov_vp = E_V @ sigma @ c_p
    var_p = c_p @ sigma @ c_p
    info = cov_vp**2 / (E_V @ sigma @ E_V * var_p)
    return float(gap), float(info), bs, bu


def gap_at_small(sd: float, cost: float) -> float:
    """Gap at a tiny informed fraction, as an approximation of the limit at 0 (verifier's numerical check)."""
    g, _, _, _ = gap_and_info(1e-7, sd, cost)
    return g


def closed_root(sd: float, cost: float, step: int = 200) -> float:
    """Bisection on the independent gap, with the page's boundary rule evaluated at 1e-7 for the limit at 0."""
    g0 = gap_at_small(sd, cost)
    g1, _, _, _ = gap_and_info(1.0, sd, cost)
    if g0 <= 0:
        return 0.0
    if g1 >= 0:
        return 1.0
    lo, hi = 1e-7, 1.0
    for _ in range(step):
        mid = 0.5 * (lo + hi)
        g, _, _, _ = gap_and_info(mid, sd, cost)
        if g > 0:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-13:
            break
    return 0.5 * (lo + hi)


def main() -> None:
    print("== section 1: Lab 1 instance (sd 0.60, cost 0.13)")
    sd, cost = 0.60, 0.13
    g0 = gap_at_small(sd, cost)
    g1, _, _, _ = gap_and_info(1.0, sd, cost)
    root = closed_root(sd, cost)
    gr, ir, bsr, bur = gap_and_info(root, sd, cost)
    print(f"gap at 0 (lam=1e-7) {g0:+.6f}  gap at 1 {g1:+.6f}  root {root:.8f}  gap at root {gr:+.3e}")
    print(f"b_s {bsr:.8f} b_u {bur:.8f} b_u/b_s {bur / bsr:.8f} -a/(root tau_e) {-A / (root * TAU_E):.8f}")
    print(f"informativeness {ir:.8f}")
    print("== section 2: Lab 2 instance (sd 0.70, cost 0.14)")
    sd, cost = 0.70, 0.14
    g0 = gap_at_small(sd, cost)
    g1, _, _, _ = gap_and_info(1.0, sd, cost)
    root = closed_root(sd, cost)
    gr, ir, _, _ = gap_and_info(root, sd, cost)
    print(f"gap at 0 {g0:+.6f}  gap at 1 {g1:+.6f}  root {root:.8f}  gap at root {gr:+.3e}  informativeness {ir:.8f}")
    print("== section 3: Lab 3 grid")
    for sd in (0.500, 0.625, 0.750):
        for cost in (0.120, 0.135, 0.150):
            root = closed_root(sd, cost)
            if 0 < root < 1:
                gr, ir, _, _ = gap_and_info(root, sd, cost)
            else:
                gr, ir = 0.0, 0.0
            t = (TAU_V + TAU_E) * np.exp(-2 * A * cost) - TAU_V
            closed = A * sd * np.sqrt(t / (TAU_E * (TAU_E - t))) if 0 < t < TAU_E * TAU_E / (TAU_E + A * A * sd * sd) else (0.0 if t <= 0 else 1.0)
            print(f"sd {sd:.3f} cost {cost:.3f} root {root:.6f} info {ir:.6f} gap_at_root {gr:+.2e} closed {closed:.6f} diff {abs(root - closed):.2e}")
    print("== section 4: multi-start equilibrium search (uniqueness in the A4 family, numeric)")
    for lam, sd in itertools.product((0.2, 0.57937525, 1.0), (0.5, 0.75)):
        found = set()
        for bs0, bu0 in itertools.product((-2.0, -0.5, 0.2, 0.9, 2.0), (-6.0, -2.0, -0.5, 0.5, 3.0)):
            sol, info, ier, msg = fsolve(clearing_residual, np.array([bs0, bu0]), args=(lam, sd), full_output=True, xtol=1e-14)
            if ier == 1 and np.max(np.abs(clearing_residual(sol, lam, sd))) < 1e-10:
                found.add((round(float(sol[0]), 8), round(float(sol[1]), 8)))
        print(f"lam {lam} sd {sd}: distinct solutions from 25 starts: {sorted(found)}")


if __name__ == "__main__":
    main()
