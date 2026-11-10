"""Starter template for the SC6 project: HJB solver (hjb_solver.py).

Implement each function according to the project specification in project.html.
"""

from __future__ import annotations

from typing import Any


def merton_fraction(r: float, mu: float, sigma: float, gamma: float) -> float:
    """Compute the theoretical unconstrained Merton portfolio fraction pi* = (mu - r) / (gamma * sigma^2)."""
    raise NotImplementedError("Implement merton_fraction(r, mu, sigma, gamma)")


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
    raise NotImplementedError("Implement exact_merton_solution(w, r, mu, sigma, gamma, rho, pi_bound)")


def solve_tridiagonal(sub: list[float], diag: list[float], sup: list[float], rhs: list[float]) -> list[float]:
    """Solve tridiagonal linear system A x = rhs using the Thomas algorithm (O(n))."""
    raise NotImplementedError("Implement solve_tridiagonal(sub, diag, sup, rhs)")


def solve_merton_hjb(instance: dict[str, Any], max_iter: int = 100, tol: float = 1e-7) -> dict[str, Any]:
    """Solve the constrained Merton HJB equation via policy iteration on a finite-difference grid."""
    raise NotImplementedError("Implement solve_merton_hjb(instance, max_iter, tol)")
