"""Reference solution for the SC6 project: HJB solver with policy iteration (hjb_solver.py).

Implements:
1. Analytical Merton fraction and exact closed-form benchmark (unconstrained and constrained).
2. Continuous-time finite-difference discretization with upwind drift stencil to preserve M-matrix monotonicity.
3. Policy iteration (Howard's algorithm) solving the constrained Merton HJB equation.
"""

from __future__ import annotations

from typing import Any


def merton_fraction(r: float, mu: float, sigma: float, gamma: float) -> float:
    """Compute the theoretical unconstrained Merton portfolio fraction pi* = (mu - r) / (gamma * sigma^2)."""
    if sigma <= 0.0:
        raise ValueError("sigma must be strictly positive")
    if gamma <= 0.0 or abs(gamma - 1.0) < 1e-12:
        raise ValueError("gamma must be positive and not equal to 1")
    return (mu - r) / (gamma * (sigma**2))


def exact_merton_solution(
    w: list[float],
    r: float,
    mu: float,
    sigma: float,
    gamma: float,
    rho: float,
    pi_bound: float | None = None,
) -> dict[str, Any]:
    """Compute the exact analytical Merton solution on wealth grid w under an optional borrowing bound pi_bound."""
    if r < 0.0 or sigma <= 0.0 or rho <= 0.0 or gamma <= 0.0 or abs(gamma - 1.0) < 1e-12:
        raise ValueError("Invalid parameters for Merton solution")
    for val in w:
        if val <= 0.0:
            raise ValueError("Wealth values must be strictly positive")

    pi_star = merton_fraction(r, mu, sigma, gamma)
    pi_eff = pi_star if (pi_bound is None or pi_bound >= pi_star) else pi_bound

    k = r + pi_eff * (mu - r) - 0.5 * gamma * (pi_eff**2) * (sigma**2)
    nu = (rho - (1.0 - gamma) * k) / gamma
    if nu <= 0.0:
        raise ValueError(f"Transversality condition failed: nu = {nu} <= 0")

    v = [(nu ** (-gamma)) / (1.0 - gamma) * (x ** (1.0 - gamma)) for x in w]
    c = [nu * x for x in w]
    return {
        "pi": pi_eff,
        "nu": nu,
        "v": v,
        "c": c,
    }


def solve_tridiagonal(sub: list[float], diag: list[float], sup: list[float], rhs: list[float]) -> list[float]:
    """Solve tridiagonal linear system A x = rhs using the Thomas algorithm (O(n))."""
    n = len(diag)
    c_prime = [0.0] * n
    d_prime = [0.0] * n

    c_prime[0] = sup[0] / diag[0]
    d_prime[0] = rhs[0] / diag[0]

    for i in range(1, n):
        denom = diag[i] - sub[i] * c_prime[i - 1]
        if i < n - 1:
            c_prime[i] = sup[i] / denom
        d_prime[i] = (rhs[i] - sub[i] * d_prime[i - 1]) / denom

    x = [0.0] * n
    x[-1] = d_prime[-1]
    for i in range(n - 2, -1, -1):
        x[i] = d_prime[i] - c_prime[i] * x[i + 1]
    return x


def solve_merton_hjb(instance: dict[str, Any], max_iter: int = 100, tol: float = 1e-7) -> dict[str, Any]:
    """Solve the constrained Merton HJB equation via policy iteration on a finite-difference grid."""
    r = float(instance["r"])
    mu = float(instance["mu"])
    sigma = float(instance["sigma"])
    gamma = float(instance["gamma"])
    rho = float(instance["rho"])
    pi_max = float(instance["pi_max"])

    if sigma <= 0.0 or rho <= 0.0 or gamma <= 0.0 or abs(gamma - 1.0) < 1e-12:
        raise ValueError("Invalid parameters in instance")
    if pi_max <= 0.0:
        raise ValueError("Borrowing constraint upper bound pi_max must be positive")

    w = [float(x) for x in instance["wealth_grid"]]
    n = len(w)
    if n < 3:
        raise ValueError("Wealth grid must have at least 3 points")
    for i in range(n):
        if w[i] <= 0.0:
            raise ValueError("Wealth must be strictly positive")
        if i > 0 and w[i] <= w[i - 1]:
            raise ValueError("Wealth grid must be strictly increasing")

    dw = (w[-1] - w[0]) / (n - 1)

    exact = exact_merton_solution(w, r, mu, sigma, gamma, rho, pi_max)
    v_exact = exact["v"]

    # Initial policy
    pi = [min(pi_max, float(exact["pi"]))] * n
    c = [float(exact["nu"]) * x for x in w]
    v = list(v_exact)

    converged = False
    diff_v = float("inf")
    it = 0

    for _ in range(max_iter):
        it += 1
        sub = [0.0] * n
        diag = [0.0] * n
        sup = [0.0] * n
        rhs = [0.0] * n

        # Dirichlet boundary conditions
        diag[0] = 1.0
        rhs[0] = v_exact[0]
        diag[-1] = 1.0
        rhs[-1] = v_exact[-1]

        for i in range(1, n - 1):
            drift = (r + pi[i] * (mu - r)) * w[i] - c[i]
            diff = 0.5 * (pi[i] ** 2) * (sigma**2) * (w[i] ** 2)

            # Upwind finite difference scheme
            if drift >= 0.0:
                alpha_i = diff / (dw**2)
                beta_i = rho + 2.0 * diff / (dw**2) + drift / dw
                gamma_i = diff / (dw**2) + drift / dw
            else:
                alpha_i = diff / (dw**2) - drift / dw
                beta_i = rho + 2.0 * diff / (dw**2) - drift / dw
                gamma_i = diff / (dw**2)

            sub[i] = -alpha_i
            diag[i] = beta_i
            sup[i] = -gamma_i
            rhs[i] = (c[i] ** (1.0 - gamma)) / (1.0 - gamma)

        v_new = solve_tridiagonal(sub, diag, sup, rhs)

        # Policy improvement
        vp = [0.0] * n
        vpp = [0.0] * n
        for i in range(1, n - 1):
            vp[i] = (v_new[i + 1] - v_new[i - 1]) / (2.0 * dw)
            vpp[i] = (v_new[i + 1] - 2.0 * v_new[i] + v_new[i - 1]) / (dw**2)
        vp[0] = (v_new[1] - v_new[0]) / dw
        vpp[0] = vpp[1]
        vp[-1] = (v_new[-1] - v_new[-2]) / dw
        vpp[-1] = vpp[-2]

        c_new = [max(vp[i], 1e-12) ** (-1.0 / gamma) for i in range(n)]
        pi_new = [0.0] * n
        for i in range(n):
            curv = min(vpp[i], -1e-12)
            pi_unc = -(mu - r) / (sigma**2) * (vp[i] / (w[i] * curv))
            pi_new[i] = max(0.0, min(pi_max, pi_unc))

        diff_v = max(abs(v_new[i] - v[i]) for i in range(n))
        v = v_new
        c = c_new
        pi = pi_new

        if diff_v < tol:
            converged = True
            break

    return {
        "w": w,
        "v": v,
        "c": c,
        "pi": pi,
        "iterations": it,
        "converged": converged,
        "max_residual": diff_v,
    }
