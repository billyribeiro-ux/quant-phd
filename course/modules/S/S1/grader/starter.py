"""Starter code for module S1 project: Power analysis for a strategy.

Complete each function according to the specification in project.html.
"""

from __future__ import annotations


def sharpe_hat(returns: list[float]) -> float:
    """Compute the per-period sample Sharpe ratio."""
    raise NotImplementedError("sharpe_hat is not implemented")


def analytic_years(sr_ann: float, periods_per_year: int, alpha: float, power: float) -> float:
    """Compute the analytic number of years required to achieve a target power."""
    raise NotImplementedError("analytic_years is not implemented")


def required_periods(sr_ann: float, periods_per_year: int, alpha: float, power: float) -> int:
    """Compute the minimum integer number of periods needed to achieve the target power."""
    raise NotImplementedError("required_periods is not implemented")


def simulated_power(periods: int, sr_per_period: float, alpha: float, n_sims: int, seed: int) -> float:
    """Estimate the statistical power of the one-sided test by Monte Carlo simulation."""
    raise NotImplementedError("simulated_power is not implemented")
