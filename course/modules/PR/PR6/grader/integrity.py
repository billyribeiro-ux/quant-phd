"""Input and output integrity validation for PR6: Dynamic & Long-Horizon Allocation.

Provides invariant verification, domain bounds checks, and structural output validation
for lifecycle portfolio optimization and glide path simulation.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def validate_lifecycle_params(params: dict[str, Any]) -> dict[str, Any]:
    """Validate lifecycle model input parameters against theoretical domain constraints."""
    required = {
        "initial_age",
        "retire_age",
        "initial_wealth",
        "initial_wage",
        "wage_growth",
        "savings_rate",
        "r_free",
        "equity_premium",
        "equity_vol",
        "phi",
        "sigma_eta",
        "rho",
        "beta_pred",
        "gamma",
        "wage_beta",
    }
    missing = required - set(params.keys())
    if missing:
        raise ValueError(f"Missing required lifecycle parameters: {sorted(missing)}")

    initial_age = int(params["initial_age"])
    retire_age = int(params["retire_age"])
    if initial_age >= retire_age:
        raise ValueError(f"initial_age ({initial_age}) must be strictly less than retire_age ({retire_age})")
    if initial_age < 18 or retire_age > 80:
        raise ValueError(f"Ages out of realistic bounds: [{initial_age}, {retire_age}]")

    if float(params["gamma"]) <= 0.0:
        raise ValueError(f"CRRA risk aversion gamma must be strictly positive, got {params['gamma']}")

    if float(params["equity_vol"]) <= 0.0 or float(params["sigma_eta"]) <= 0.0:
        raise ValueError("Volatilities must be strictly positive")

    rho = float(params["rho"])
    if not -1.0 <= rho <= 1.0:
        raise ValueError(f"Correlation rho must lie in [-1, 1], got {rho}")

    phi = float(params["phi"])
    if not 0.0 <= phi < 1.0:
        raise ValueError(f"AR(1) persistence phi must lie in [0, 1) for stationarity, got {phi}")

    if float(params["initial_wealth"]) < 0.0 or float(params["initial_wage"]) <= 0.0:
        raise ValueError("Initial wealth must be non-negative and wage must be strictly positive")

    if not 0.0 <= float(params["savings_rate"]) <= 1.0:
        raise ValueError("Savings rate must lie in [0, 1]")

    return params


def validate_simulation_outputs(out: dict[str, Any]) -> bool:
    """Validate structural invariants of lifecycle simulation outputs."""
    required_keys = {
        "mean_terminal_wealth",
        "median_terminal_wealth",
        "std_terminal_wealth",
        "p5_terminal_wealth",
        "certainty_equivalent",
        "max_late_drawdown_p95",
        "equity_weights",
    }
    if not required_keys.issubset(out.keys()):
        missing = required_keys - set(out.keys())
        raise ValueError(f"Output dictionary missing required keys: {sorted(missing)}")

    # Invariants
    if float(out["p5_terminal_wealth"]) > float(out["mean_terminal_wealth"]):
        raise ValueError("5th percentile wealth cannot exceed mean terminal wealth")
    if float(out["certainty_equivalent"]) <= 0.0:
        raise ValueError("Certainty equivalent wealth must be strictly positive")
    if not (0.0 <= float(out["max_late_drawdown_p95"]) <= 1.0):
        raise ValueError("Drawdown must lie in [0, 1]")

    weights = np.asarray(out["equity_weights"])
    if weights.ndim != 1 or len(weights) < 2:
        raise ValueError("equity_weights must be a 1D array across lifecycle ages")
    if np.any(np.isnan(weights)) or np.any(np.isinf(weights)):
        raise ValueError("equity_weights contains NaN or Inf")

    return True
