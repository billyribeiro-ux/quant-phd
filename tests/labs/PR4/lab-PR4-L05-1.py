"""Lab 5: Peaks Over Threshold (POT) and Generalized Pareto Distribution (GPD) Estimation.

Demonstrates extreme value theory tail modeling under the Pickands-Balkema-de Haan theorem
and quantifies the severe underestimation of tail risk under the Gaussian assumption.
"""

from __future__ import annotations

import math

import numpy as np


def main() -> None:
    rng = np.random.default_rng(42)

    # 1. Simulate heavy-tailed financial returns (Student-t with df=3)
    n_obs = 2000
    daily_vol = 0.015
    losses = rng.standard_t(df=3, size=n_obs) * daily_vol

    # 2. Peaks Over Threshold (POT) at 90th percentile threshold u
    threshold = float(np.quantile(losses, 0.90, method="linear"))
    excesses = losses[losses > threshold] - threshold
    n_u = len(excesses)

    mean_exc = float(np.mean(excesses))
    var_exc = float(np.var(excesses, ddof=1))

    # Method of Moments GPD parameter estimates (Hosking & Wallis 1987)
    ratio = (mean_exc**2) / var_exc
    xi_gpd = 0.5 * (1.0 - ratio)
    beta_gpd = mean_exc * (1.0 - xi_gpd)

    # 3. High-confidence tail quantiles (alpha = 99.5%)
    alpha = 0.995
    factor = (n_obs / n_u) * (1.0 - alpha)

    var_evt = threshold + (beta_gpd / xi_gpd) * (factor ** (-xi_gpd) - 1.0)
    es_evt = (var_evt + beta_gpd - xi_gpd * threshold) / (1.0 - xi_gpd)

    # 4. Compare with Gaussian benchmark
    mu = float(np.mean(losses))
    sigma = float(np.std(losses, ddof=1))
    z_995 = 2.575829  # standard normal quantile for 0.995
    phi_z = (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * z_995**2)

    var_norm = mu + sigma * z_995
    es_norm = mu + sigma * (phi_z / (1.0 - alpha))

    print(f"Sample Observations: {n_obs} | POT Exceedances (u={threshold:.6f}): {n_u}")
    print(f"GPD Shape Parameter xi (tail heaviness): {xi_gpd:.4f}")
    print(f"GPD Scale Parameter beta: {beta_gpd:.6f}")
    print("-" * 65)
    print(f"EVT POT 99.5% VaR: {var_evt:.6f} | Gaussian 99.5% VaR: {var_norm:.6f}")
    print(f"EVT POT 99.5% ES:  {es_evt:.6f} | Gaussian 99.5% ES:  {es_norm:.6f}")
    underest_es = (es_evt - es_norm) / es_evt * 100.0
    print(f"Gaussian Expected Shortfall Underestimation: {underest_es:.1f}%")


main()
