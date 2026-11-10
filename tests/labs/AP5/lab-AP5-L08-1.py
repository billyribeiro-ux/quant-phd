"""Lab AP5-L08-1: Cross-Asset Return Predictability and Discount-Rate Synthesis.

SIMULATED: evaluates Cochrane's (2011) discount rate synthesis across equities and
Treasuries, estimating predictive regressions and extracting the common discount-rate factor.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    rng = np.random.default_rng(2011)
    n_obs = 200  # 200 quarters (50 years)

    # Macroeconomic business cycle state s_t: countercyclical risk premium driver
    phi_s = 0.90
    sigma_s = 0.25
    s = np.zeros(n_obs + 1)
    for t in range(n_obs):
        s[t + 1] = phi_s * s[t] + sigma_s * rng.standard_normal()

    # Asset 1: Equity market
    # Dividend-price ratio is loaded heavily on macro state s_t
    dp = -3.20 + 0.35 * s[:-1] + 0.08 * rng.standard_normal(n_obs)
    # Equity excess return: positive loading on s_t + idiosyncratic risk
    rx_eq = 0.018 + 0.08 * s[:-1] + 0.16 * rng.standard_normal(n_obs)

    # Asset 2: Treasury bond market
    # Term spread is also countercyclical (widens in recessions)
    term_spread = 0.015 + 0.012 * s[:-1] + 0.004 * rng.standard_normal(n_obs)
    # 5-year Treasury excess return: positive loading on term spread and s_t
    rx_bond = 0.005 + 0.025 * s[:-1] + 0.05 * rng.standard_normal(n_obs)

    # OLS 1: Equity predictive regression: rx_eq = a_eq + b_eq * dp + e
    dp_m = float(np.mean(dp))
    rx_eq_m = float(np.mean(rx_eq))
    sxx_dp = float(np.sum((dp - dp_m) ** 2))
    sxy_eq = float(np.sum((dp - dp_m) * (rx_eq - rx_eq_m)))
    syy_eq = float(np.sum((rx_eq - rx_eq_m) ** 2))
    b_eq = sxy_eq / sxx_dp
    r2_eq = (sxy_eq**2) / (sxx_dp * syy_eq)
    se_eq = float(np.sqrt(max(1e-12, (syy_eq - b_eq * sxy_eq) / ((n_obs - 2) * sxx_dp))))
    t_eq = b_eq / se_eq

    # OLS 2: Bond predictive regression: rx_bond = a_bond + b_bond * term_spread + e
    ts_m = float(np.mean(term_spread))
    rx_bd_m = float(np.mean(rx_bond))
    sxx_ts = float(np.sum((term_spread - ts_m) ** 2))
    sxy_bd = float(np.sum((term_spread - ts_m) * (rx_bond - rx_bd_m)))
    syy_bd = float(np.sum((rx_bond - rx_bd_m) ** 2))
    b_bond = sxy_bd / sxx_ts
    r2_bond = (sxy_bd**2) / (sxx_ts * syy_bd)
    se_bond = float(np.sqrt(max(1e-12, (syy_bd - b_bond * sxy_bd) / ((n_obs - 2) * sxx_ts))))
    t_bond = b_bond / se_bond

    # Extract fitted expected excess returns (time-varying risk premia)
    exp_rx_eq = rx_eq_m + b_eq * (dp - dp_m)
    exp_rx_bd = rx_bd_m + b_bond * (term_spread - ts_m)
    corr_risk_premia = float(np.corrcoef(exp_rx_eq, exp_rx_bd)[0, 1])

    print("Cochrane (2011) Cross-Asset Discount Rate Synthesis")
    print(f"Sample length T:             {n_obs} quarters ({n_obs / 4:.0f} years)")
    print(f"Equity predictive slope:     {b_eq:.4f}")
    print(f"Equity OLS t-stat (R^2):     {t_eq:.2f} ({r2_eq * 100:.2f}%)")
    print(f"Bond predictive slope:       {b_bond:.4f}")
    print(f"Bond OLS t-stat (R^2):       {t_bond:.2f} ({r2_bond * 100:.2f}%)")
    print(f"Risk premia correlation:     {corr_risk_premia:.4f}")
    print("Cross-asset implication:     Common countercyclical discount-rate factor")


main()
