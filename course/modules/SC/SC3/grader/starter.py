"""Starter template for SC3: Numeraire Toolkit.

Implement the five functions below according to the specification in project.html.
All functions must validate inputs and raise ValueError on invalid arguments.
"""

from __future__ import annotations

from typing import Any


def margrabe_price(
    s1: float,
    s2: float,
    sig1: float,
    sig2: float,
    rho: float,
    q1: float,
    q2: float,
    t: float,
) -> float:
    """Compute the closed-form Margrabe exchange option price max(S_1(T) - S_2(T), 0)."""
    raise NotImplementedError("margrabe_price is not implemented")


def margrabe_mc(
    s1: float,
    s2: float,
    sig1: float,
    sig2: float,
    rho: float,
    q1: float,
    q2: float,
    t: float,
    r: float,
    n_paths: int,
    seed: int,
) -> tuple[float, float]:
    """Estimate the Margrabe exchange option price and standard error via bivariate Monte Carlo."""
    raise NotImplementedError("margrabe_mc is not implemented")


def quanto_call_price(
    s_f: float,
    k: float,
    r_d: float,
    r_f: float,
    sig_s: float,
    sig_x: float,
    rho: float,
    t: float,
) -> float:
    """Compute the closed-form quanto European call price with payoff max(S^f_T - K, 0) in domestic currency."""
    raise NotImplementedError("quanto_call_price is not implemented")


def quanto_call_mc(
    s_f: float,
    x0: float,
    k: float,
    r_d: float,
    r_f: float,
    sig_s: float,
    sig_x: float,
    rho: float,
    t: float,
    n_paths: int,
    seed: int,
) -> tuple[float, float]:
    """Estimate the quanto call price and standard error via Monte Carlo under domestic measure Q^d."""
    raise NotImplementedError("quanto_call_mc is not implemented")


def verify_invariance(instance: dict[str, Any]) -> dict[str, Any]:
    """Verify numeraire invariance, homogeneity, exchange parity, and simulation concordance."""
    raise NotImplementedError("verify_invariance is not implemented")
