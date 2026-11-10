"""Lab AP6-project-1 (Rung 1, Worked Example): Index Inclusion Flow Impact.

SIMULATED: Complete worked example estimating stock-level price impact from index
rebalancing flows and translating cross-sectional estimates into the aggregate macro multiplier.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    rng = np.random.default_rng(101)
    n_events = 50  # 50 index addition events

    # Pre-event price and shares outstanding
    pre_prices = 40.0 + 30.0 * rng.uniform(0.0, 1.0, size=n_events)

    # Exogenous tracking inflow: fraction of shares demanded by passive index funds
    # Typically 3% to 12% of shares outstanding
    flow_fractions = rng.uniform(0.03, 0.12, size=n_events)

    # True stock-level demand elasticity zeta_stock = 0.22 => multiplier mu = 1 / 0.22 approx 4.55
    true_mu = 4.60
    true_intercept = 0.015  # average market drift over event window

    # Realized post-event price: Delta ln(P) = intercept + mu * flow + noise
    log_pre = np.log(pre_prices)
    noise = 0.02 * rng.standard_normal(n_events)
    delta_log_p = true_intercept + true_mu * flow_fractions + noise
    post_prices = np.exp(log_pre + delta_log_p)

    # Step 1: Compute cumulative abnormal returns (CAR)
    car_returns = np.log(post_prices) - np.log(pre_prices)
    mean_car = float(np.mean(car_returns))

    # Step 2: OLS regression of CAR on flow fraction: CAR_k = c + mu * flow_k + e_k
    x_design = np.column_stack([np.ones(n_events), flow_fractions])
    coefs = np.linalg.lstsq(x_design, car_returns, rcond=None)[0]
    c_hat = float(coefs[0])
    mu_hat = float(coefs[1])

    # Step 3: Compute implied stock demand elasticity and R-squared
    implied_zeta = float(1.0 / mu_hat)
    residuals = car_returns - x_design @ coefs
    tss = float(np.sum((car_returns - mean_car) ** 2))
    r2 = float(1.0 - np.sum(residuals**2) / tss)

    # Step 4: Macro translation (Gabaix & Koijen 2021)
    # If the micro elasticity is zeta_micro, aggregate market elasticity is dampened by general equilibrium
    # Macro multiplier M_agg approx 1 / (zeta_micro + alpha_macro)
    m_macro_predicted = float(1.0 / (implied_zeta + 0.05))

    print("Project Rung 1: Flow-Impact Worked Example Reference Output")
    print(f"Number of index addition events: {n_events}")
    print(f"Mean event CAR:                  {mean_car * 100:.2f}%")
    print(f"Estimated price impact slope mu: {mu_hat:.4f}")
    print(f"Estimated intercept c:           {c_hat:.4f}")
    print(f"Implied stock elasticity zeta:   {implied_zeta:.4f}")
    print(f"Event regression R^2:            {r2 * 100:.2f}%")
    print(f"Predicted macro multiplier M:    {m_macro_predicted:.2f}")


main()
