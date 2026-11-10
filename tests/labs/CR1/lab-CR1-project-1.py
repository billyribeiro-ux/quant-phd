"""Lab CR1-project-1 (Rung 1, Worked Example): Fully solved credit valuation and analytics workflow.

SIMULATED: complete end-to-end demonstration of the Atlas A14 credit engine:
Merton pricing, Black-Cox first passage, reduced-form intensity pricing,
distance-to-default estimation, and credit spread decomposition.
Standard library only; no network.
"""

from __future__ import annotations

import math


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def main() -> None:
    # Stylized firm parameters
    v = 100.0
    d = 70.0
    t = 2.0
    r = 0.04
    sigma_v = 0.25

    print("Step 1 · Merton (1974) Structural Model Pricing:")
    vol_sqrt = sigma_v * math.sqrt(t)
    d1 = (math.log(v / d) + (r + 0.5 * sigma_v * sigma_v) * t) / vol_sqrt
    d2 = d1 - vol_sqrt
    equity = v * norm_cdf(d1) - d * math.exp(-r * t) * norm_cdf(d2)
    debt = v - equity
    merton_yield = -math.log(debt / d) / t
    merton_spread_bps = (merton_yield - r) * 10000.0
    print(f"  Asset Value V = ${v:.2f}, Debt Face D = ${d:.2f}")
    print(f"  Equity E = ${equity:.2f}, Risky Debt B = ${debt:.2f}")
    print(f"  Yield = {merton_yield * 100:.2f}%, Credit Spread = {merton_spread_bps:.1f} bp")
    assert abs(equity + debt - v) < 1e-11

    print("\nStep 2 · Black-Cox (1976) First-Passage Model Pricing:")
    barrier = 60.0
    rec = 0.40
    b = math.log(barrier / v)
    mu = r - 0.5 * sigma_v**2
    lam = r + 0.5 * sigma_v**2
    d_minus = (b - mu * t) / vol_sqrt
    d_plus = (b + mu * t) / vol_sqrt
    pd_bc = norm_cdf(d_minus) + math.exp(2.0 * mu * b / (sigma_v**2)) * norm_cdf(d_plus)
    g1 = math.exp(2.0 * r * b / (sigma_v**2)) * norm_cdf((b + lam * t) / vol_sqrt)
    g2 = math.exp(-b) * norm_cdf((b - lam * t) / vol_sqrt)
    bc_debt = d * math.exp(-r * t) * (1.0 - pd_bc) + rec * d * (g1 + g2)
    bc_spread_bps = (-math.log(bc_debt / d) / t - r) * 10000.0
    print(f"  Safety Covenant Barrier K = ${barrier:.2f}, Recovery R = {rec:.0%}")
    print(f"  First-Passage Default Prob = {pd_bc:.4f}, Debt = ${bc_debt:.2f}, Spread = {bc_spread_bps:.1f} bp")

    print("\nStep 3 · Reduced-Form Duffie-Singleton (1999) Intensity Pricing:")
    hazard_rate = 0.0150
    p_rmv = math.exp(-(r + hazard_rate * (1.0 - rec)) * t)
    s_rmv_bps = hazard_rate * (1.0 - rec) * 10000.0
    print(f"  Default Intensity lambda = {hazard_rate * 10000:.0f} bp")
    print(f"  RMV Bond Price = {p_rmv:.4f}, RMV Spread = {s_rmv_bps:.1f} bp")

    print("\nStep 4 · Distance-to-Default and Bharath-Shumway Naive Proxy:")
    obs_e = equity
    obs_sigma_e = 0.32
    v_naive = obs_e + d
    sigma_d = 0.05 + 0.25 * obs_sigma_e
    sigma_v_naive = (obs_e / v_naive) * obs_sigma_e + (d / v_naive) * sigma_d
    dd_naive = (math.log(v_naive / d) + (r - 0.5 * sigma_v_naive**2) * t) / (sigma_v_naive * math.sqrt(t))
    print(f"  Observed Equity = ${obs_e:.2f}, Equity Vol = {obs_sigma_e * 100:.1f}%")
    print(f"  Naive Asset Value V = ${v_naive:.2f}, Naive Vol = {sigma_v_naive * 100:.2f}%")
    print(f"  Bharath-Shumway Naive DD = {dd_naive:.2f}, Implied PD = {norm_cdf(-dd_naive):.4f}")

    print("\nStep 5 · Huang & Huang (2012) Spread Decomposition:")
    market_spread_bps = 140.0
    pd_10y = 0.0060
    s_el_bps = -math.log(1.0 - pd_10y * (1.0 - rec)) / t * 10000.0
    s_crp_bps = s_el_bps * 0.80
    s_credit_bps = s_el_bps + s_crp_bps
    s_residual_bps = max(0.0, market_spread_bps - s_credit_bps)
    print(f"  Market Spread = {market_spread_bps:.1f} bp")
    print(f"  Expected Loss = {s_el_bps:.1f} bp, Risk Premium = {s_crp_bps:.1f} bp")
    print(
        f"  Non-Credit Residual = {s_residual_bps:.1f} bp ({(s_residual_bps / market_spread_bps) * 100:.1f}% of total)"
    )


main()
