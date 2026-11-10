"""Lab MS1-L06-1: Kyle's lambda estimation and price impact.

SIMULATED: generates realizations from the Kyle linear equilibrium with noise.
Estimates Kyle's lambda via least squares regression of price changes on total order flow,
and compares the empirical estimate and standard error to the theoretical population value.
"""

from __future__ import annotations

import math
import random


def simulate_kyle_trades(
    n_obs: int, p0: float, sigma0: float, sigma_u: float, obs_noise: float = 0.10, seed: int = 42
) -> tuple[list[float], list[float], float]:
    """Generate equilibrium order flows and transaction price changes."""
    rng = random.Random(seed)
    sd_v = math.sqrt(sigma0)
    lam_pop = sd_v / (2.0 * sigma_u)
    beta_pop = sigma_u / sd_v

    omegas: list[float] = []
    price_changes: list[float] = []

    for _ in range(n_obs):
        v = rng.gauss(p0, sd_v)
        u = rng.gauss(0.0, sigma_u)
        x = beta_pop * (v - p0)
        omega = x + u
        e = rng.gauss(0.0, obs_noise)
        p = p0 + lam_pop * omega + e

        omegas.append(omega)
        price_changes.append(p - p0)

    return omegas, price_changes, lam_pop


def estimate_kyles_lambda(omegas: list[float], price_changes: list[float]) -> tuple[float, float, float]:
    """Regress price changes on order flow without intercept to estimate Kyle's lambda."""
    n = len(omegas)
    s_ww = sum(w * w for w in omegas)
    s_wd = sum(w * d for w, d in zip(omegas, price_changes, strict=False))
    lam_hat = s_wd / s_ww

    residuals = [d - lam_hat * w for w, d in zip(omegas, price_changes, strict=False)]
    s2 = sum(r * r for r in residuals) / (n - 1)
    se_lam = math.sqrt(s2 / s_ww)

    return lam_hat, se_lam, s2


def main() -> None:
    n_obs = 2500
    p0 = 100.0
    sigma0 = 4.0
    sigma_u = 2.0

    omegas, price_changes, lam_pop = simulate_kyle_trades(n_obs, p0, sigma0, sigma_u, obs_noise=0.10, seed=42)
    lam_hat, se_lam, _ = estimate_kyles_lambda(omegas, price_changes)
    t_stat = (lam_hat - lam_pop) / se_lam

    print(f"Sample size: {n_obs} realizations")
    print(f"Prior parameters: p_0 = {p0:.1f}, Sigma_0 = {sigma0:.1f}, sigma_u = {sigma_u:.1f}")
    print(f"Theoretical Kyle's lambda: {lam_pop:.4f}")
    print(f"Estimated Kyle's lambda:   {lam_hat:.4f}")
    print(f"Regression standard error: {se_lam:.6f}")
    print(f"Estimation error:          {abs(lam_hat - lam_pop):.6f}")
    print(f"t-statistic against null lambda = {lam_pop:.4f}: {t_stat:.4f}")


main()
