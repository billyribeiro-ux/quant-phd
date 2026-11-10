"""Instance generator for SR3 autograded project: Atlas A19 Systemic-Risk Monitor.

SIMULATED: generates synthetic heavy-tailed market returns, multi-firm equity returns,
macroeconomic state variables, balance-sheet debt and equity values, and interbank
bilateral liability networks for deterministic seed-specific validation.
"""

from __future__ import annotations

import math
import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic systemic risk monitoring instance for Atlas A19.

    Parameters
    ----------
    seed : int
        Pseudorandom seed for reproducibility.

    Returns
    -------
    dict[str, Any]
        Dictionary of returns, balance sheet items, interbank networks, and parameters.
    """
    rng = random.Random(seed)
    t_obs = 500  # 500 daily trading periods (~2 years)
    n_institutions = 4  # 4 interconnected financial institutions

    # Generate macroeconomic state variables M_t:
    # M_t[:, 0] = volatility shock (mean 0, AR(1) persistence 0.7)
    # M_t[:, 1] = term spread / liquidity shock (mean 0, AR(1) persistence 0.5)
    macro_states: list[list[float]] = []
    v0, s0 = 0.0, 0.0
    for _ in range(t_obs):
        v0 = 0.7 * v0 + rng.gauss(0.0, 0.01)
        s0 = 0.5 * s0 + rng.gauss(0.0, 0.005)
        macro_states.append([round(v0, 6), round(s0, 6)])

    # Generate systemic market return R_s:
    # Leptokurtic market returns driven by macro states and Student-t(4) innovations
    r_system: list[float] = []
    market_drift = 0.0003 + (seed % 3) * 0.0001
    for t in range(t_obs):
        # Chi-square with 4 degrees of freedom
        v = sum(rng.gauss(0.0, 1.0) ** 2 for _ in range(4))
        scale = math.sqrt(v / 4.0)
        t_noise = rng.gauss(0.0, 0.012) / (scale if scale > 1e-4 else 1.0)
        r_s = market_drift - 0.4 * macro_states[t][0] - 0.2 * macro_states[t][1] + t_noise
        r_system.append(round(r_s, 6))

    # Generate institutional returns R_i,t:
    # Institutional betas range between 0.8 and 1.6
    betas = [0.85 + (seed % 4) * 0.1, 1.15 + (seed % 3) * 0.1, 1.45 + (seed % 2) * 0.1, 1.0 + (seed % 5) * 0.05]
    r_institutions: list[list[float]] = [[] for _ in range(n_institutions)]
    for i in range(n_institutions):
        b = betas[i]
        idio_vol = 0.008 + i * 0.002
        for t in range(t_obs):
            idio = rng.gauss(0.0, idio_vol)
            r_it = b * r_system[t] + 0.1 * macro_states[t][0] + idio
            r_institutions[i].append(round(r_it, 6))

    # Balance sheet items (in billions USD):
    # Equities W_i and Book Debts D_i
    equities = [
        round(120.0 + (seed % 20) * 3.5, 2),
        round(85.0 + (seed % 15) * 2.8, 2),
        round(210.0 + (seed % 25) * 4.2, 2),
        round(55.0 + (seed % 10) * 1.9, 2),
    ]
    debts = [
        round(850.0 + (seed % 30) * 12.0, 2),
        round(620.0 + (seed % 25) * 10.5, 2),
        round(1600.0 + (seed % 40) * 18.0, 2),
        round(440.0 + (seed % 20) * 8.0, 2),
    ]

    # Interbank nominal liability network L (4x4):
    # Off-diagonal bilateral nominal debt obligations
    nominal_liabilities: list[list[float]] = [[0.0] * n_institutions for _ in range(n_institutions)]
    for i in range(n_institutions):
        for j in range(n_institutions):
            if i != j:
                base_l = 10.0 + ((seed + i * 3 + j * 7) % 25)
                nominal_liabilities[i][j] = round(base_l, 2)

    # Outside external assets z and senior obligations b:
    external_assets: list[float] = []
    senior_liabilities: list[float] = []
    for i in range(n_institutions):
        total_interbank_out = sum(nominal_liabilities[i])
        z_val = round(total_interbank_out * (0.8 + ((seed + i) % 5) * 0.1), 2)
        b_val = round(total_interbank_out * (0.15 + ((seed + i * 2) % 4) * 0.05), 2)
        external_assets.append(z_val)
        senior_liabilities.append(b_val)

    # Stressed asset shock for contagion cascade:
    # Catastrophic external shock with institution 0 asset wipeout
    stressed_assets = [round(z * 0.15, 2) for z in external_assets]
    stressed_assets[0] = 0.0

    return {
        "seed": seed,
        "t_obs": t_obs,
        "n_institutions": n_institutions,
        "r_system": r_system,
        "r_institutions": r_institutions,
        "macro_states": macro_states,
        "equities": equities,
        "debts": debts,
        "nominal_liabilities": nominal_liabilities,
        "external_assets": external_assets,
        "senior_liabilities": senior_liabilities,
        "stressed_assets": stressed_assets,
        "alpha": 0.05,
        "prudential_ratio": 0.08,
        "crisis_drop": 0.40,
        "alert_thresholds": {
            "delta_covar": -0.015,
            "mes": 0.035,
            "srisk_pct": 0.35,
            "network_defaults": 1,
        },
    }
