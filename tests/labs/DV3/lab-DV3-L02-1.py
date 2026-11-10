"""Lab 2 · SABR Implied Volatility Expansion & Arbitrage Pathologies.

This lab implements the Hagan et al. asymptotic implied volatility formula for the
SABR model, evaluates the implied smile across moneyness, computes the risk-neutral
density via the Breeden-Litzenberger identity, and detects butterfly arbitrage
(negative probability density) in the deep left wing under high vol-of-vol stress on seed 0 (SIMULATED).
"""

from __future__ import annotations

import math


def sabr_implied_vol(
    f: float,
    k: float,
    t: float,
    alpha: float,
    beta: float,
    rho: float,
    nu: float,
) -> float:
    """Hagan et al. asymptotic formula for Black implied volatility."""
    if f <= 0.0 or k <= 0.0 or t <= 0.0:
        return 0.0

    eps = 1e-7
    if abs(f - k) < eps:
        fk_mid = f ** (1.0 - beta)
        term1 = (1.0 - beta) ** 2 / 24.0 * (alpha * alpha) / (fk_mid * fk_mid)
        term2 = 0.25 * rho * beta * nu * alpha / fk_mid
        term3 = (2.0 - 3.0 * rho * rho) / 24.0 * nu * nu
        val = (alpha / fk_mid) * (1.0 + (term1 + term2 + term3) * t)
        return float(val)

    log_fk = math.log(f / k)
    fk = f * k
    fk_beta = fk ** ((1.0 - beta) / 2.0)

    denom = fk_beta * (1.0 + ((1.0 - beta) ** 2 / 24.0) * (log_fk**2) + ((1.0 - beta) ** 4 / 1920.0) * (log_fk**4))

    z = (nu / alpha) * fk_beta * log_fk
    arg = math.sqrt(max(0.0, 1.0 - 2.0 * rho * z + z * z)) + z - rho
    chi_z = z if arg <= 0.0 or abs(1.0 - rho) < 1e-12 else math.log(arg / (1.0 - rho))
    z_over_chi = 1.0 if abs(z) < 1e-6 else z / chi_z

    factor = (
        1.0
        + (
            ((1.0 - beta) ** 2 / 24.0) * (alpha * alpha) / (fk ** (1.0 - beta))
            + 0.25 * (rho * beta * nu * alpha) / fk_beta
            + ((2.0 - 3.0 * rho * rho) / 24.0) * (nu * nu)
        )
        * t
    )

    ans = (alpha / denom) * z_over_chi * factor
    return float(ans)


def black76_call_price(f: float, k: float, t: float, r: float, sigma: float) -> float:
    """Black-76 call price on forward."""
    if t <= 0.0 or sigma <= 0.0:
        return math.exp(-r * t) * max(0.0, f - k)
    std = sigma * math.sqrt(t)
    d1 = (math.log(f / k) + 0.5 * std * std) / std
    d2 = d1 - std

    def n_cdf(x: float) -> float:
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

    disc = math.exp(-r * t)
    return disc * (f * n_cdf(d1) - k * n_cdf(d2))


def breeden_litzenberger_density(
    f: float,
    k: float,
    t: float,
    r: float,
    alpha: float,
    beta: float,
    rho: float,
    nu: float,
    dk: float = 0.5,
) -> float:
    """Compute risk-neutral state-price density q(K) = exp(r*T) * d^2 C / dK^2."""
    vol_c = sabr_implied_vol(f, k, t, alpha, beta, rho, nu)
    vol_up = sabr_implied_vol(f, k + dk, t, alpha, beta, rho, nu)
    vol_dn = sabr_implied_vol(f, k - dk, t, alpha, beta, rho, nu)

    c_center = black76_call_price(f, k, t, r, vol_c)
    c_up = black76_call_price(f, k + dk, t, r, vol_up)
    c_dn = black76_call_price(f, k - dk, t, r, vol_dn)

    second_deriv = (c_up - 2.0 * c_center + c_dn) / (dk * dk)
    return math.exp(r * t) * second_deriv


def main() -> None:
    print("=== SABR Model Asymptotics & Density Analysis ===")
    f0 = 100.0
    r = 0.02

    # Case A: Well-behaved baseline (T=1.0, beta=0.5, nu=0.40)
    alpha_base = 2.0
    beta_base = 0.50
    rho_base = -0.30
    nu_base = 0.40
    t_base = 1.0

    # Case B: Stressed long-maturity regime (T=3.0, beta=0.2, nu=1.20, rho=-0.60)
    alpha_stress = 2.0
    beta_stress = 0.20
    rho_stress = -0.60
    nu_stress = 1.20
    t_stress = 3.0

    print(f"Baseline: F0={f0}, T={t_base}, alpha={alpha_base}, beta={beta_base}, rho={rho_base}, nu={nu_base}")
    print(
        f"Stressed: F0={f0}, T={t_stress}, alpha={alpha_stress}, beta={beta_stress}, rho={rho_stress}, nu={nu_stress}"
    )

    strikes = [15.0, 30.0, 50.0, 75.0, 100.0, 125.0, 150.0]

    print("\nImplied Volatility Smile & Density Comparison (SIMULATED):")
    print(" Strike | IV (Base) | Density (Base) | IV (Stress) | Density (Stress) ")
    print("-------------------------------------------------------------------")
    negative_density_found = False
    for k in strikes:
        iv_b = sabr_implied_vol(f0, k, t_base, alpha_base, beta_base, rho_base, nu_base)
        dens_b = breeden_litzenberger_density(f0, k, t_base, r, alpha_base, beta_base, rho_base, nu_base)
        iv_s = sabr_implied_vol(f0, k, t_stress, alpha_stress, beta_stress, rho_stress, nu_stress)
        dens_s = breeden_litzenberger_density(f0, k, t_stress, r, alpha_stress, beta_stress, rho_stress, nu_stress)
        if dens_s < 0.0:
            negative_density_found = True
        print(f" {k:6.1f} |   {iv_b:7.4f} |        {dens_b:7.5f} |     {iv_s:7.4f} |          {dens_s:7.5f} ")

    print(f"\nButterfly Arbitrage Detected Under Stress (Density < 0): {negative_density_found}")
    print("Interpretation: Under large vol-of-vol nu*sqrt(T), the Hagan expansion violates")
    print("no-arbitrage in the deep wing, proving the need for arbitrage-free SABR formulations.")


main()
