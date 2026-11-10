"""Starter file for AP2 project (CAPM on trial).

Students must implement all seven functions to satisfy the specification.
"""

from __future__ import annotations

from fractions import Fraction


def minimum_variance_weights(cov: list[list[Fraction]]) -> list[Fraction]:
    """Compute the global minimum-variance portfolio weights w_GMV."""
    raise NotImplementedError("Implement minimum_variance_weights")


def tangency_weights(mu: list[Fraction], cov: list[list[Fraction]], r_f: Fraction) -> list[Fraction]:
    """Compute the tangency portfolio weights w_T."""
    raise NotImplementedError("Implement tangency_weights")


def frontier_weights(mu: list[Fraction], cov: list[list[Fraction]], target: Fraction) -> list[Fraction]:
    """Compute the minimum-variance portfolio weights achieving target expected return."""
    raise NotImplementedError("Implement frontier_weights")


def is_tangency(mu: list[Fraction], cov: list[list[Fraction]], r_f: Fraction, weights: list[Fraction]) -> bool:
    """Check whether weights represent the tangency portfolio in exact Fraction arithmetic."""
    raise NotImplementedError("Implement is_tangency")


def capm_beta(asset: list[Fraction], market: list[Fraction]) -> Fraction:
    """Compute sample market beta: Cov(asset, market) / Var(market)."""
    raise NotImplementedError("Implement capm_beta")


def jensen_regression(asset: list[float], market: list[float]) -> dict[str, float]:
    """Run time-series Jensen regression of asset excess returns on market excess returns."""
    raise NotImplementedError("Implement jensen_regression")


def security_market_line(betas: list[Fraction], mean_excess: list[Fraction]) -> tuple[Fraction, Fraction]:
    """Fit cross-sectional security market line: mean_excess = gamma_0 + gamma_1 * beta."""
    raise NotImplementedError("Implement security_market_line")
