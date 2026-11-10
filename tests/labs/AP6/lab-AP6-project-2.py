"""Lab AP6-project-2 (Rung 2, Completion): Inelastic Markets Engine Core.

SIMULATED: Complete solution for the Rung 2 completion problem calculating
the Koijen-Yogo IV demand elasticity, Gabaix-Koijen flow multiplier, and macro wealth impact.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    # Given institutional ownership shares and estimated sector demand elasticities
    # Sectors: Mutual Funds, Pension Funds, Life Insurers, Foreign, Other/Households
    ownership = np.array([0.25, 0.20, 0.10, 0.15, 0.30])
    elasticities = np.array([0.30, 0.05, 0.08, 0.25, 0.50])

    # Step 1: Compute aggregate market elasticity: zeta_m = sum_i s_i * zeta_i
    zeta_m = float(np.sum(ownership * elasticities))

    # Step 2: Compute Gabaix-Koijen aggregate flow multiplier: M = 1 / zeta_m
    m_multiplier = float(1.0 / zeta_m)

    # Given pre-estimated IV 2SLS matrices for stock universe (N = 100)
    # First-stage fitted price: hat_log_p = W @ gamma_first
    rng = np.random.default_rng(77)
    n_stocks = 100
    w_first = np.column_stack([np.ones(n_stocks), rng.standard_normal((n_stocks, 2))])
    gamma_first = np.array([1.2, 0.65, 0.45])
    hat_log_p = w_first @ gamma_first

    # Second stage regressors: M = [1, -hat_log_p, characteristics]
    chars = rng.standard_normal((n_stocks, 2))
    m_second = np.column_stack([np.ones(n_stocks), -hat_log_p, chars])
    theta_true = np.array([0.5, 1.85, 0.6, -0.3])
    y_demand = m_second @ theta_true + 0.1 * rng.standard_normal(n_stocks)

    # Step 3: Compute second-stage 2SLS parameter estimates
    theta_iv = np.linalg.lstsq(m_second, y_demand, rcond=None)[0]
    beta_iv = float(theta_iv[1])

    # Step 4: Macro wealth impact of $100 Billion institutional flow shock on $40T equity market
    market_cap = 40000.0  # $40,000 Billion ($40 Trillion)
    flow_shock = 100.0  # $100 Billion
    flow_fraction = flow_shock / market_cap
    pct_price_change = m_multiplier * flow_fraction
    dollar_impact = market_cap * pct_price_change

    print("Project Rung 2: Completion Problem Reference Output")
    print(f"Aggregate demand elasticity zeta_m: {zeta_m:.4f}")
    print(f"Aggregate flow multiplier M:        {m_multiplier:.4f}")
    print(f"2SLS estimated elasticity beta:     {beta_iv:.4f}")
    print(f"Market percentage price change:     {pct_price_change * 100:.4f}%")
    print(f"Total market cap wealth gain:       ${dollar_impact:.2f}B")
    print(f"Dollar multiplier per $1 flow:      ${dollar_impact / flow_shock:.2f}")


main()
