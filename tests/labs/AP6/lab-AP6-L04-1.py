"""Lab AP6-L04-1: Koijen-Yogo Demand System 2SLS Elasticity Estimation.

SIMULATED: Replicates the Koijen & Yogo (2019) demand system estimation.
Demonstrates the severe endogeneity bias of naive OLS due to unobserved latent demand,
and shows how exogenous investment universe instruments recover the true structural price elasticity.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    rng = np.random.default_rng(42)
    n_stocks = 200
    true_beta = 1.65  # true structural demand elasticity
    true_gamma = np.array([0.75, -0.40])  # loadings on log market equity and book-to-market

    # Stock characteristics X: log market equity and book-to-market
    x_chars = np.zeros((n_stocks, 2))
    x_chars[:, 0] = rng.normal(loc=2.0, scale=0.9, size=n_stocks)
    x_chars[:, 1] = rng.normal(loc=0.0, scale=0.5, size=n_stocks)

    # Exogenous instrument Z (e.g. index investment universe mandate / supply shocks)
    z_inst = np.zeros((n_stocks, 2))
    z_inst[:, 0] = 0.65 * x_chars[:, 0] + 0.70 * rng.standard_normal(n_stocks)
    z_inst[:, 1] = rng.uniform(-1.0, 1.0, size=n_stocks)

    # Unobserved latent quality / demand shock delta_0
    # Latent demand is positively correlated with equilibrium prices (high quality => high price)
    latent_quality = 0.8 * rng.standard_normal(n_stocks)
    log_prices = 1.0 + 0.45 * z_inst[:, 0] + 0.35 * z_inst[:, 1] + 0.50 * latent_quality

    # True institutional portfolio demand:
    # y_n = ln(w_n / w_0) = alpha - beta * log_p + gamma' X + latent_quality
    alpha_true = 0.50
    y_demand = alpha_true - true_beta * log_prices + x_chars @ true_gamma + latent_quality

    # 1. Naive OLS regression of y on [-log_prices, X]:
    # Correlated omitted variable (latent_quality) severely biases beta toward zero or wrong sign!
    m_ols = np.column_stack([np.ones(n_stocks), -log_prices, x_chars])
    theta_ols = np.linalg.lstsq(m_ols, y_demand, rcond=None)[0]
    beta_ols = float(theta_ols[1])

    # 2. 2SLS IV Estimation:
    # First stage: regress log_p on [instruments, characteristics]
    w_first = np.column_stack([np.ones(n_stocks), z_inst, x_chars])
    gamma_first = np.linalg.lstsq(w_first, log_prices, rcond=None)[0]
    hat_log_p = w_first @ gamma_first

    # First stage F-statistic on instruments
    res_ur = log_prices - hat_log_p
    ssr_ur = float(np.sum(res_ur**2))
    w_restr = np.column_stack([np.ones(n_stocks), x_chars])
    gamma_restr = np.linalg.lstsq(w_restr, log_prices, rcond=None)[0]
    ssr_r = float(np.sum((log_prices - w_restr @ gamma_restr) ** 2))
    q_df = z_inst.shape[1]
    df_resid = n_stocks - w_first.shape[1]
    f_stat = float(((ssr_r - ssr_ur) / q_df) / (ssr_ur / df_resid))

    # Second stage: regress y on [-hat_log_p, X]
    m_iv = np.column_stack([np.ones(n_stocks), -hat_log_p, x_chars])
    theta_iv = np.linalg.lstsq(m_iv, y_demand, rcond=None)[0]
    beta_iv = float(theta_iv[1])
    gamma_iv = theta_iv[2:]

    print("Koijen & Yogo (2019) Demand System Elasticity Estimation")
    print(f"Number of cross-sectional stocks N: {n_stocks}")
    print(f"True structural price elasticity:  {true_beta:.2f}")
    print(f"First-stage IV F-statistic:        {f_stat:.2f} (> 10 stock-Yogo bound)")
    print(f"Naive OLS estimated elasticity:    {beta_ols:.4f} (biased toward 0)")
    print(f"2SLS IV estimated elasticity:      {beta_iv:.4f}")
    print(f"2SLS elasticity recovery error:    {abs(beta_iv - true_beta):.4f}")
    print(f"True characteristic loadings:      [{true_gamma[0]:.2f}, {true_gamma[1]:.2f}]")
    print(f"2SLS characteristic loadings:      [{gamma_iv[0]:.2f}, {gamma_iv[1]:.2f}]")
    print(f"OLS severely understates elasticity: {bool(beta_ols < 0.5 * true_beta)}")


main()
