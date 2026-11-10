"""Starter template for SC4 PDE pricer project.

Implement each function according to the project specification in project.html.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def thomas_solve(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Solve tridiagonal system Ax = d using the Thomas algorithm."""
    raise NotImplementedError("Implement thomas_solve(a, b, c, d)")


def solve_pde(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    vol: float,
    option_type: str,
    payoff_type: str = "vanilla",
    barrier: float | None = None,
    barrier_type: str | None = None,
    method: str = "crank_nicolson",
    rannacher: bool = True,
    s_max_mult: float = 4.0,
    n_space: int = 200,
    n_time: int = 100,
) -> dict[str, Any]:
    """Solve Black-Scholes PDE using finite-difference scheme.

    Returns dict with keys: 'price', 'delta', 'gamma', 'grid_s', 'grid_v'.
    """
    raise NotImplementedError("Implement solve_pde(...)")


def price_option(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    vol: float,
    option_type: str,
    payoff_type: str = "vanilla",
    barrier: float | None = None,
    barrier_type: str | None = None,
    method: str = "crank_nicolson",
    rannacher: bool = True,
    n_space: int = 200,
    n_time: int = 100,
) -> float:
    """Convenience wrapper returning option price from solve_pde."""
    raise NotImplementedError("Implement price_option(...)")


def estimate_convergence_order(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    vol: float,
    option_type: str = "call",
    method: str = "crank_nicolson",
    rannacher: bool = True,
    grids: list[tuple[int, int]] | None = None,
) -> float:
    """Estimate empirical convergence order alpha via regression on a refined grid sequence."""
    raise NotImplementedError("Implement estimate_convergence_order(...)")
