"""Lab CR1-project-2 (Rung 2, Completion): Credit valuation, naive distance to default, and spread decomposition.

SIMULATED: complete solution for the Rung 2 completion problem.
Calculates Merton debt and equity values, Duffie-Singleton reduced-form spread,
Bharath-Shumway naive distance to default, and credit spread decomposition.
Standard library only; no network.
"""

from __future__ import annotations

import math


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def main() -> None:
    # Stylized inputs
    v = 100.0
    d = 70.0
    t = 2.0
    r = 0.04
    sigma_v = 0.25

    # Step 1: Merton (1974) option pricing components
    vol_sqrt = sigma_v * math.sqrt(t)
    d1 = (math.log(v / d) + (r + 0.5 * sigma_v * sigma_v) * t) / vol_sqrt
    d2 = d1 - vol_sqrt
    equity = v * norm_cdf(d1) - d * math.exp(-r * t) * norm_cdf(d2)
    debt = v - equity
    merton_spread = (-math.log(debt / d) / t - r) * 10000.0

    # Step 2: Duffie-Singleton (1999) RMV spread
    hazard_rate = 0.0150
    recovery_rate = 0.40
    rmv_spread = hazard_rate * (1.0 - recovery_rate) * 10000.0

    # Step 3: Bharath-Shumway (2008) naive distance to default
    obs_e = equity
    obs_sigma_e = 0.32
    v_naive = obs_e + d
    sigma_d = 0.05 + 0.25 * obs_sigma_e
    sigma_v_naive = (obs_e / v_naive) * obs_sigma_e + (d / v_naive) * sigma_d
    dd_naive = (math.log(v_naive / d) + (r - 0.5 * sigma_v_naive**2) * t) / (sigma_v_naive * math.sqrt(t))

    # Step 4: Credit spread decomposition (Huang & Huang 2012)
    market_spread_bps = 140.0
    pd = 0.0060
    s_el = -math.log(1.0 - pd * (1.0 - recovery_rate)) / t * 10000.0
    s_crp = s_el * 0.80
    s_credit = s_el + s_crp
    s_residual = max(0.0, market_spread_bps - s_credit)

    print(f"Merton equity: ${equity:.2f}, debt: ${debt:.2f}, spread: {merton_spread:.1f} bp")
    print(f"Duffie-Singleton RMV credit spread: {rmv_spread:.1f} bp")
    print(f"Bharath-Shumway naive DD: {dd_naive:.2f}")
    print(f"Spread decomposition: EL={s_el:.1f} bp, CRP={s_crp:.1f} bp, Residual={s_residual:.1f} bp")


main()
