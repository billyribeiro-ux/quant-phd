"""Starter template for Atlas A12 Quantitative Risk Engine (`atlas.risk`).

Students implement the functions below to satisfy the contract.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def historical_var(losses: np.ndarray[Any, Any], alpha: float = 0.99) -> float:
    """Compute empirical Historical Simulation Value-at-Risk at confidence level alpha."""
    raise NotImplementedError("historical_var is not implemented yet")


def historical_es(losses: np.ndarray[Any, Any], alpha: float = 0.99) -> float:
    """Compute empirical Historical Simulation Expected Shortfall at confidence level alpha."""
    raise NotImplementedError("historical_es is not implemented yet")


def parametric_normal_var_es(
    losses: np.ndarray[Any, Any],
    alpha: float = 0.99,
) -> tuple[float, float]:
    """Compute parametric Gaussian Value-at-Risk and Expected Shortfall."""
    raise NotImplementedError("parametric_normal_var_es is not implemented yet")


def parametric_student_t_var_es(
    losses: np.ndarray[Any, Any],
    alpha: float = 0.99,
    df: int = 5,
) -> tuple[float, float]:
    """Compute parametric Student-t Value-at-Risk and Expected Shortfall."""
    raise NotImplementedError("parametric_student_t_var_es is not implemented yet")


def evt_gpd_var_es(
    losses: np.ndarray[Any, Any],
    threshold: float,
    alpha: float = 0.99,
) -> tuple[float, float, float, float]:
    """Compute Extreme Value Theory Peaks-Over-Threshold (POT) VaR and ES using GPD."""
    raise NotImplementedError("evt_gpd_var_es is not implemented yet")


def kupiec_pof_test(
    exceptions: int,
    total_obs: int,
    alpha: float = 0.99,
) -> tuple[float, float, bool]:
    """Execute Kupiec Proportion of Failures (POF) Likelihood Ratio test."""
    raise NotImplementedError("kupiec_pof_test is not implemented yet")


def christoffersen_test(
    hits: np.ndarray[Any, Any],
    alpha: float = 0.99,
) -> tuple[float, float, float, float, float, float]:
    """Execute Christoffersen (1998) unconditional, independence, and conditional coverage tests."""
    raise NotImplementedError("christoffersen_test is not implemented yet")


def stress_scenario_pnl(
    weights: np.ndarray[Any, Any],
    portfolio_value: float,
    asset_shocks: np.ndarray[Any, Any],
) -> float:
    """Compute portfolio dollar P&L under a prescribed multi-asset stress scenario."""
    raise NotImplementedError("stress_scenario_pnl is not implemented yet")


def gaussian_copula_tail_metrics(
    corr_matrix: np.ndarray[Any, Any],
    threshold: float = 0.95,
    n_sims: int = 100000,
    seed: int = 42,
) -> tuple[float, float]:
    """Simulate from a bivariate Gaussian copula and compute tail co-movement metrics."""
    raise NotImplementedError("gaussian_copula_tail_metrics is not implemented yet")
