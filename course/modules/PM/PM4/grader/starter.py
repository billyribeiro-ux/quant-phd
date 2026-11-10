"""Starter implementation for the PM4 MBS pricer project.

Learners complete this module by implementing exact short-rate diffusion,
pathwise cash flow generation, OAS root-finding, and effective Greeks.
"""

from __future__ import annotations

import numpy as np


def simulate_interest_rates(
    r0: float,
    kappa: float,
    theta: float,
    sigma: float,
    wam: int,
    n_paths: int,
    seed: int = 42,
) -> np.ndarray:
    """Simulate risk-neutral short rate paths using exact Gaussian Vasicek transitions."""
    raise NotImplementedError("simulate_interest_rates is not implemented")


def generate_mbs_cash_flows(
    notional: float,
    wac: float,
    pass_through_rate: float,
    wam: int,
    base_cpr: float,
    max_cpr: float,
    beta: float,
    mu: float,
    margin: float,
    gamma_burnout: float,
    rates: np.ndarray,
) -> np.ndarray:
    """Generate pathwise monthly cash flows under state-dependent prepayment and burnout."""
    raise NotImplementedError("generate_mbs_cash_flows is not implemented")


def price_mbs(
    cash_flows: np.ndarray,
    rates: np.ndarray,
    spread: float = 0.0,
    delay_days: int = 24,
) -> float:
    """Discount pathwise cash flows along simulated rate paths with settlement delay."""
    raise NotImplementedError("price_mbs is not implemented")


def solve_oas(
    rates: np.ndarray,
    cash_flows: np.ndarray,
    target_price: float,
    delay_days: int = 24,
) -> float:
    """Solve for OAS equating model expectation to target market price via bisection."""
    raise NotImplementedError("solve_oas is not implemented")


def compute_effective_greeks(
    instance: dict[str, float | int],
    oas_bps: float,
) -> dict[str, float]:
    """Compute base price, shifted prices, effective duration, and effective convexity."""
    raise NotImplementedError("compute_effective_greeks is not implemented")


def solve_mbs_pricer(instance: dict[str, float | int]) -> dict[str, float]:
    """Execute complete MBS pricing, OAS calibration, and effective Greek computation."""
    raise NotImplementedError("solve_mbs_pricer is not implemented")
