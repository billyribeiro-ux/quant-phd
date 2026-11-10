"""Lab AP2-L08-1: The empirically flat security market line and beta attenuation.

SIMULATED cross-sections (seeds 1 to 5).
Demonstrates the econometric mechanism by which sampling noise and errors-in-variables
in estimated betas bias the second-pass cross-sectional regression slope toward zero,
producing a flat-looking security market line even when the true risk premium is positive.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    n_assets = 15
    t_obs = 60
    true_gamma_0 = 0.002  # monthly zero-beta rate ~ 20 bps
    true_gamma_1 = 0.006  # monthly market risk premium ~ 60 bps (7.2% annualized)

    print("--- SIMULATED Cross-Sectional Regressions: Flat SML Demonstration ---")
    print("Seed | True Slope | Estimated Slope | Estimated Intercept | t-stat (Slope)")
    print("------------------------------------------------------------------------")

    for seed in range(1, 6):
        rng = random.Random(seed)
        # Generate true betas in [0.6, 1.4]
        true_betas = [0.6 + 0.8 * (i / (n_assets - 1)) for i in range(n_assets)]

        # Generate market excess returns
        mkt = [rng.gauss(true_gamma_1, 0.045) for _ in range(t_obs)]
        mean_m = sum(mkt) / float(t_obs)
        s_mm = sum((m - mean_m) ** 2 for m in mkt)

        # Generate asset returns and estimate first-pass betas
        beta_hats: list[float] = []
        mean_returns: list[float] = []

        for i in range(n_assets):
            b_true = true_betas[i]
            # True expected excess return
            e_r = true_gamma_0 + true_gamma_1 * b_true
            series = [e_r + b_true * (mkt[t] - true_gamma_1) + rng.gauss(0.0, 0.035) for t in range(t_obs)]
            mean_y = sum(series) / float(t_obs)
            s_ym = sum((series[t] - mean_y) * (mkt[t] - mean_m) for t in range(t_obs))
            b_hat = s_ym / s_mm
            beta_hats.append(b_hat)
            mean_returns.append(mean_y)

        # Second-pass cross-sectional regression: mean_returns = gamma_0 + gamma_1 * beta_hats
        mean_bh = sum(beta_hats) / float(n_assets)
        mean_mr = sum(mean_returns) / float(n_assets)
        s_bb = sum((b - mean_bh) ** 2 for b in beta_hats)
        s_by = sum((beta_hats[i] - mean_bh) * (mean_returns[i] - mean_mr) for i in range(n_assets))

        gamma_1_hat = s_by / s_bb
        gamma_0_hat = mean_mr - gamma_1_hat * mean_bh

        residuals = [mean_returns[i] - (gamma_0_hat + gamma_1_hat * beta_hats[i]) for i in range(n_assets)]
        s2 = sum(e * e for e in residuals) / float(n_assets - 2)
        se_g1 = math.sqrt(s2 / s_bb)
        t_stat = gamma_1_hat / se_g1

        print(
            f"{seed:4d} |   {true_gamma_1:8.4f} |        {gamma_1_hat:8.4f} |"
            f"            {gamma_0_hat:8.4f} |       {t_stat:6.2f}"
        )


main()
