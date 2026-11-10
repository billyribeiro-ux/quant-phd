"""Instance generator for CF9 Corporate Hedging Program project.

Deterministic from seed. Exposes make_instance(seed: int) -> dict[str, Any].
Standard library only.
"""

from __future__ import annotations

import random
from typing import Any

CURRENCIES = ["EUR", "JPY", "GBP"]


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic, valid corporate hedging instance for the given seed.

    Returns currency cash flow projections, spot rates, covariance structures,
    and capital budgeting parameters for Meridian Global Industries.
    """
    rng = random.Random(seed)

    # 1. Foreign currency committed receivables and payables (in millions of FC)
    # EUR: ~20-35M rec, 8-15M pay
    eur_rec = round(rng.uniform(22.0, 35.0), 2)
    eur_pay = round(rng.uniform(8.0, 14.0), 2)

    # JPY: ~2500-4500M rec, 800-1800M pay
    jpy_rec = round(rng.uniform(2500.0, 4200.0), 1)
    jpy_pay = round(rng.uniform(800.0, 1600.0), 1)

    # GBP: ~12-22M rec, 4-9M pay
    gbp_rec = round(rng.uniform(14.0, 24.0), 2)
    gbp_pay = round(rng.uniform(4.0, 9.0), 2)

    # 2. Spot exchange rates in USD per unit of foreign currency
    s_eur = round(rng.uniform(1.05, 1.15), 4)
    s_jpy = round(rng.uniform(0.0065, 0.0075), 6)
    s_gbp = round(rng.uniform(1.24, 1.34), 4)

    # 3. Volatilities and correlation matrix
    vol_eur = round(rng.uniform(0.09, 0.12), 4)
    vol_jpy = round(rng.uniform(0.10, 0.14), 4)
    vol_gbp = round(rng.uniform(0.08, 0.11), 4)
    vols = [vol_eur, vol_jpy, vol_gbp]

    # Valid positive definite correlation matrix
    rho_ej = round(rng.uniform(0.25, 0.45), 4)
    rho_eg = round(rng.uniform(0.55, 0.75), 4)
    rho_jg = round(rng.uniform(0.20, 0.40), 4)

    corr_matrix = [
        [1.0, rho_ej, rho_eg],
        [rho_ej, 1.0, rho_jg],
        [rho_eg, rho_jg, 1.0],
    ]

    # Covariance matrix: Sigma_ij = rho_ij * vol_i * vol_j
    cov_matrix: list[list[float]] = []
    for i in range(3):
        row: list[float] = []
        for j in range(3):
            cov_ij = corr_matrix[i][j] * vols[i] * vols[j]
            row.append(round(cov_ij, 8))
        cov_matrix.append(row)

    # 4. Hurdle cash flow (minimum required for debt service + capex) in USD millions
    hurdle = round(rng.uniform(42.0, 55.0), 2)
    domestic_costs_usd = round(rng.uniform(15.0, 25.0), 2)

    # 5. Hedge accounting dollar-offset scenario
    delta_exposure = round(rng.uniform(-12.0, -8.0), 2)
    ratio = round(rng.uniform(0.75, 1.30), 4)
    delta_derivative = round(abs(delta_exposure) * ratio, 2)

    # 6. Cross-border capital budgeting project parameters
    initial_outlay_eur = round(rng.uniform(40.0, 60.0), 2)
    cf_eur_1 = round(rng.uniform(12.0, 18.0), 2)
    cf_eur_2 = round(rng.uniform(16.0, 24.0), 2)
    cf_eur_3 = round(rng.uniform(20.0, 28.0), 2)
    cf_eur_4 = round(rng.uniform(18.0, 25.0), 2)
    project_cfs_eur = [cf_eur_1, cf_eur_2, cf_eur_3, cf_eur_4]

    r_usd = round(rng.uniform(0.045, 0.055), 4)
    r_eur = round(rng.uniform(0.025, 0.035), 4)
    wacc_usd = round(rng.uniform(0.095, 0.115), 4)

    return {
        "seed": seed,
        "currencies": list(CURRENCIES),
        "receivables": [eur_rec, jpy_rec, gbp_rec],
        "payables": [eur_pay, jpy_pay, gbp_pay],
        "spot_rates": [s_eur, s_jpy, s_gbp],
        "fx_volatilities": [vol_eur, vol_jpy, vol_gbp],
        "correlation_matrix": corr_matrix,
        "covariance_matrix": cov_matrix,
        "hurdle_cash_flow": hurdle,
        "domestic_costs_usd": domestic_costs_usd,
        "delta_exposure": delta_exposure,
        "delta_derivative": delta_derivative,
        "initial_outlay_eur": initial_outlay_eur,
        "project_cfs_eur": project_cfs_eur,
        "r_usd": r_usd,
        "r_eur": r_eur,
        "wacc_usd": wacc_usd,
    }
