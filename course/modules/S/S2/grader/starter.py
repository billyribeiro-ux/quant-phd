"""Starter template for S2 Inference Engine project.

Implement each function according to the specification in project.html.
Do not modify the function names or argument signatures.
"""

from __future__ import annotations

from typing import Any


def ols_beta(x: list[list[float]], y: list[float]) -> list[float]:
    """Compute OLS coefficient vector beta_hat = (X'X)^{-1} X'y."""
    raise NotImplementedError


def se_classical(x: list[list[float]], y: list[float]) -> list[float]:
    """Compute classical OLS standard errors with degrees-of-freedom correction n - k."""
    raise NotImplementedError


def se_white(x: list[list[float]], y: list[float]) -> list[float]:
    """Compute White (HC0) heteroskedasticity-robust standard errors."""
    raise NotImplementedError


def se_newey_west(x: list[list[float]], y: list[float], lags: int) -> list[float]:
    """Compute Newey-West HAC standard errors with Bartlett kernel weights."""
    raise NotImplementedError


def se_cluster(x: list[list[float]], y: list[float], cluster: list[Any]) -> list[float]:
    """Compute one-way cluster-robust (CR0) standard errors."""
    raise NotImplementedError


def se_two_way(x: list[list[float]], y: list[float], cluster_a: list[Any], cluster_b: list[Any]) -> list[float]:
    """Compute two-way clustered standard errors: V = V_A + V_B - V_{A cap B}."""
    raise NotImplementedError


def t_critical(df: int) -> float:
    """Return the two-sided 95% critical value (97.5th percentile) for Student-t with df degrees of freedom."""
    raise NotImplementedError


def coverage(draws: list[dict[str, Any]], method: str, column: int) -> float:
    """Calculate the empirical coverage rate of nominal 95% confidence intervals on a collection of draws."""
    raise NotImplementedError
