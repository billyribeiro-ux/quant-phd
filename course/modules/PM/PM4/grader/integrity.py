"""Integrity and input validation helpers for the PM4 MBS pricer engine.

Validates input types, dimensions, bounded domains, and mathematical consistency.
Raises ValueError on invalid numerical domains or lengths, and TypeError on bad types.
"""

from __future__ import annotations

import math


def validate_pool_spec(pool: dict[str, float | int]) -> None:
    """Validate mortgage collateral pool parameters."""
    required_keys = ["notional", "wac", "pass_through_rate", "wam", "delay_days"]
    for k in required_keys:
        if k not in pool:
            raise ValueError(f"Missing required pool parameter: {k}")

    notional = float(pool["notional"])
    wac = float(pool["wac"])
    pt_rate = float(pool["pass_through_rate"])
    wam = int(pool["wam"])
    delay = int(pool["delay_days"])

    if notional <= 0.0 or not math.isfinite(notional):
        raise ValueError(f"Pool notional must be strictly positive and finite, got {notional}")
    if not (0.01 <= wac <= 0.20):
        raise ValueError(f"WAC must be between 1% and 20%, got {wac}")
    if not (0.005 <= pt_rate <= wac):
        raise ValueError(f"Pass-through rate must be positive and not exceed WAC, got {pt_rate}")
    if not (12 <= wam <= 480):
        raise ValueError(f"Remaining maturity WAM must be between 12 and 480 months, got {wam}")
    if not (0 <= delay <= 90):
        raise ValueError(f"Delay days must be between 0 and 90, got {delay}")


def validate_rate_model(rates: dict[str, float]) -> None:
    """Validate 1-factor short-rate model parameters."""
    required = ["r0", "kappa", "theta", "sigma"]
    for k in required:
        if k not in rates:
            raise ValueError(f"Missing required rate parameter: {k}")

    r0 = float(rates["r0"])
    kappa = float(rates["kappa"])
    theta = float(rates["theta"])
    sigma = float(rates["sigma"])

    if not (-0.02 <= r0 <= 0.20):
        raise ValueError(f"Initial short rate r0 out of realistic range: {r0}")
    if kappa <= 0.0 or not math.isfinite(kappa):
        raise ValueError(f"Mean reversion speed kappa must be strictly positive, got {kappa}")
    if not (-0.02 <= theta <= 0.20):
        raise ValueError(f"Long-term mean rate theta out of realistic range: {theta}")
    if sigma <= 0.0 or not math.isfinite(sigma):
        raise ValueError(f"Volatility sigma must be strictly positive, got {sigma}")


def validate_prepayment_spec(prep: dict[str, float]) -> None:
    """Validate prepayment and burnout parameters."""
    required = ["base_cpr", "max_cpr", "beta", "mu", "margin", "gamma_burnout"]
    for k in required:
        if k not in prep:
            raise ValueError(f"Missing required prepayment parameter: {k}")

    base_cpr = float(prep["base_cpr"])
    max_cpr = float(prep["max_cpr"])
    beta = float(prep["beta"])
    mu = float(prep["mu"])
    margin = float(prep["margin"])
    gamma = float(prep["gamma_burnout"])

    if not (0.0 <= base_cpr <= 0.20):
        raise ValueError(f"base_cpr must be in [0, 0.20], got {base_cpr}")
    if not (base_cpr <= max_cpr <= 0.90):
        raise ValueError(f"max_cpr must exceed base_cpr and not exceed 0.90, got {max_cpr}")
    if beta <= 0.0:
        raise ValueError(f"beta must be strictly positive, got {beta}")
    if not (-0.05 <= mu <= 0.05):
        raise ValueError(f"mu refinancing midpoint out of range: {mu}")
    if not (0.0 <= margin <= 0.05):
        raise ValueError(f"mortgage refinancing margin out of range: {margin}")
    if gamma < 0.0:
        raise ValueError(f"gamma_burnout must be non-negative, got {gamma}")
