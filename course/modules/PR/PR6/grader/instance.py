"""Deterministic instance generator for PR6: Dynamic & Long-Horizon Allocation.

Generates seed-dependent economic environments, wage profiles, return predictability
parameters, and lifecycle investor preferences for autograding.
"""

from __future__ import annotations

from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic, valid lifecycle parameter instance for the given seed."""
    # Deterministic parameter variations derived from seed
    initial_age = 24 + (seed % 5)  # 24 to 28
    retire_age = 64 + ((seed * 3 + 1) % 4)  # 64 to 67
    initial_wealth = 20000.0 + float((seed * 17 + 5) % 11) * 2000.0  # 20k to 40k
    initial_wage = 48000.0 + float((seed * 13 + 7) % 9) * 3000.0  # 48k to 72k
    wage_growth = 0.020 + float((seed * 7 + 2) % 6) * 0.003  # 0.020 to 0.035
    savings_rate = 0.12 + float((seed * 11 + 3) % 5) * 0.02  # 0.12 to 0.20
    r_free = 0.018 + float((seed * 5 + 1) % 5) * 0.003  # 0.018 to 0.030
    equity_premium = 0.045 + float((seed * 9 + 4) % 6) * 0.004  # 0.045 to 0.065
    equity_vol = 0.16 + float((seed * 3 + 2) % 5) * 0.015  # 0.16 to 0.22
    phi = 0.80 + float((seed * 7 + 5) % 5) * 0.025  # 0.80 to 0.90
    sigma_eta = 0.09 + float((seed * 11 + 1) % 4) * 0.012  # 0.09 to 0.126
    rho = -0.80 + float((seed * 13 + 3) % 6) * 0.035  # -0.80 to -0.625
    beta_pred = 0.050 + float((seed * 17 + 2) % 5) * 0.006  # 0.050 to 0.074
    gamma = 3.0 + float((seed * 7 + 4) % 5) * 0.7  # 3.0 to 5.8
    wage_beta = 0.05 * float((seed * 3) % 4)  # 0.0, 0.05, 0.10, 0.15

    return {
        "initial_age": initial_age,
        "retire_age": retire_age,
        "initial_wealth": initial_wealth,
        "initial_wage": initial_wage,
        "wage_growth": wage_growth,
        "savings_rate": savings_rate,
        "r_free": r_free,
        "equity_premium": equity_premium,
        "equity_vol": equity_vol,
        "phi": phi,
        "sigma_eta": sigma_eta,
        "rho": rho,
        "beta_pred": beta_pred,
        "gamma": gamma,
        "wage_beta": wage_beta,
        "seed": seed,
    }
