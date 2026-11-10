"""Lab AP6-L02-1: Primary Dealer Intermediary Capital Ratio SDF Estimation.

SIMULATED: Estimates the He, Kelly & Manela (2017) intermediary asset pricing model.
Constructs aggregate dealer equity capital ratio eta_t, extracts AR(1) innovations u_t,
computes multi-asset factor betas beta_i^eta, and evaluates cross-sectional risk price lambda_eta.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    rng = np.random.default_rng(42)
    n_quarters = 160  # 40 years of quarterly data
    n_assets = 8  # 8 test asset classes: US equities, Corp bonds, MBS, FX, Options, CDS, Commodities, Treasuries

    # Simulate primary dealer equity capital ratio eta_t = Equity / (Equity + Debt)
    # Calibrated to HKM (2017) historical dealer equity capital ratio: mean ~8%, AR(1) persistence ~0.90
    phi_eta = 0.90
    mu_eta = 0.08 * (1.0 - phi_eta)
    sigma_eta = 0.012

    eta = np.zeros(n_quarters)
    eta[0] = 0.08
    for t in range(1, n_quarters):
        eta[t] = mu_eta + phi_eta * eta[t - 1] + sigma_eta * rng.standard_normal()

    # AR(1) shocks: u_t = eta_t - (mu + phi * eta_{t-1})
    x_ar = np.column_stack([np.ones(n_quarters - 1), eta[:-1]])
    ar_coefs = np.linalg.lstsq(x_ar, eta[1:], rcond=None)[0]
    estimated_phi = float(ar_coefs[1])
    dealer_shocks = eta[1:] - x_ar @ ar_coefs
    var_u = float(np.var(dealer_shocks, ddof=1))

    # True cross-sectional risk price for dealer capital: lambda_eta = 0.08 (8% annualized per unit beta)
    lambda_eta_true = 0.08 / 4.0  # quarterly: 2% per quarter
    true_betas = np.array([2.5, 1.8, 1.4, 0.9, 3.2, 1.1, 0.7, 0.3])

    # Simulate test asset excess returns R_{i,t}^e = beta_i * lambda + beta_i * u_t + e_{i,t}
    returns_excess = np.zeros((n_quarters - 1, n_assets))
    for j in range(n_assets):
        idio_vol = 0.03 + 0.005 * j
        returns_excess[:, j] = (
            true_betas[j] * lambda_eta_true
            + true_betas[j] * dealer_shocks
            + idio_vol * rng.standard_normal(n_quarters - 1)
        )

    # 1. Estimate time-series betas: beta_j = Cov(R_j^e, u) / Var(u)
    betas_hat = np.zeros(n_assets)
    for j in range(n_assets):
        cov_ju = float(np.cov(returns_excess[:, j], dealer_shocks)[0, 1])
        betas_hat[j] = cov_ju / var_u

    # 2. Cross-sectional regression: E[R_j^e] = lambda_eta * beta_j
    mean_excess_returns = np.mean(returns_excess, axis=0)
    risk_price_hat = float((betas_hat @ mean_excess_returns) / (betas_hat @ betas_hat))
    pricing_errors = mean_excess_returns - risk_price_hat * betas_hat
    cross_r2 = float(
        1.0 - np.sum(pricing_errors**2) / np.sum((mean_excess_returns - np.mean(mean_excess_returns)) ** 2)
    )

    # Annualize risk price and compute SDF factor loading b_eta
    annual_risk_price = risk_price_hat * 4.0
    b_eta = risk_price_hat / var_u

    print("He, Kelly & Manela (2017) Intermediary Asset Pricing Engine")
    print(f"Sample length T:                 {n_quarters} quarters")
    print(f"Estimated capital AR(1) phi:      {estimated_phi:.4f}")
    print(f"Dealer capital shock vol sigma_u: {np.sqrt(var_u):.4f}")
    print(f"Estimated dealer risk price:     {annual_risk_price * 100:.2f}% per year")
    print(f"Cross-sectional R^2:             {cross_r2 * 100:.2f}%")
    print(f"SDF capital factor loading b:    {b_eta:.2f}")
    print(f"Beta range across asset classes: [{np.min(betas_hat):.2f}, {np.max(betas_hat):.2f}]")
    print(f"Max pricing error (quarterly):   {np.max(np.abs(pricing_errors)):.4f}")


main()
