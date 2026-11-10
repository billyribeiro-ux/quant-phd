"""Lab CR1-L02-1: Black-Cox (1976) first-passage credit model and short-term credit spreads.

Demonstrates first-passage hitting time distributions, safety covenants,
and the resolution of Merton's zero short-spread anomaly via early default barriers.
"""

from __future__ import annotations

import math


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def black_cox_components(
    v: float,
    d: float,
    t: float,
    r: float,
    sigma: float,
    k: float,
    rec: float = 0.4,
) -> dict[str, float]:
    """Calculate Black-Cox first passage debt, equity, and credit spread."""
    b = math.log(k / v)
    vol_sqrt = sigma * math.sqrt(t)
    mu = r - 0.5 * sigma * sigma
    lam = r + 0.5 * sigma * sigma

    # Default probability by time T
    d_minus = (b - mu * t) / vol_sqrt
    d_plus = (b + mu * t) / vol_sqrt
    prob_default = norm_cdf(d_minus) + math.exp(2.0 * mu * b / (sigma * sigma)) * norm_cdf(d_plus)
    prob_default = min(1.0, max(0.0, prob_default))
    survival_prob = 1.0 - prob_default

    # Expected discounted hitting factor
    g1 = math.exp(2.0 * r * b / (sigma * sigma)) * norm_cdf((b + lam * t) / vol_sqrt)
    g2 = math.exp(-b) * norm_cdf((b - lam * t) / vol_sqrt)
    exp_disc_hit = g1 + g2

    debt = d * math.exp(-r * t) * survival_prob + rec * d * exp_disc_hit
    equity = v - debt
    debt_yield = -math.log(debt / d) / t
    spread_bps = (debt_yield - r) * 10000.0

    return {
        "debt": debt,
        "equity": equity,
        "spread_bps": spread_bps,
        "default_prob": prob_default,
        "survival_prob": survival_prob,
    }


def merton_spread_bps(v: float, d: float, t: float, r: float, sigma: float) -> float:
    """Compute Merton credit spread in basis points."""
    vol_sqrt = sigma * math.sqrt(t)
    d1 = (math.log(v / d) + (r + 0.5 * sigma * sigma) * t) / vol_sqrt
    d2 = d1 - vol_sqrt
    equity = v * norm_cdf(d1) - d * math.exp(-r * t) * norm_cdf(d2)
    debt = v - equity
    return float((-math.log(debt / d) / t - r) * 10000.0)


def main() -> None:
    # Moderately levered firm: V = 100, D = 80, K = 70, r = 0.04, sigma = 0.25, R = 0.40
    v = 100.0
    d = 80.0
    k_barrier = 70.0
    r = 0.04
    sigma = 0.25
    rec = 0.40

    maturities = [0.25, 0.5, 1.0, 2.0, 3.0, 5.0]

    print("Black-Cox (1976) vs Merton (1974) Credit Spread Term Structure (V=100, D=80, K=70):")
    print("  T (yr) | Merton (bp) | Black-Cox (bp) | Spread Diff (bp) | First-Passage PD")
    print("---------+-------------+----------------+------------------+-----------------")

    for t in maturities:
        bc = black_cox_components(v, d, t, r, sigma, k_barrier, rec)
        m_spread = merton_spread_bps(v, d, t, r, sigma)
        diff = bc["spread_bps"] - m_spread
        assert abs(bc["debt"] + bc["equity"] - v) < 1e-11
        print(
            f"  {t:5.2f}  |   {m_spread:8.1f}  |    {bc['spread_bps']:9.1f}   |     "
            f"{diff:9.1f}    |     {bc['default_prob']:8.4f}"
        )

    # Resolution of Merton zero short-spread puzzle:
    # When a firm is near the safety covenant barrier (e.g. V=75, K=70),
    # Black-Cox produces massive short-term spreads due to first-passage probability,
    # whereas Merton allows the firm to survive until maturity.
    v_near = 75.0
    t_short = 0.10
    m_short = merton_spread_bps(v_near, d, t_short, r, sigma)
    bc_short = black_cox_components(v_near, d, t_short, r, sigma, k_barrier, rec)["spread_bps"]
    print(
        f"\nNear-barrier firm (V=75, K=70) at T=0.10y: "
        f"Merton spread = {m_short:6.1f} bp vs Black-Cox = {bc_short:6.1f} bp"
    )

    # Black-Cox spread is strictly higher than Merton because covenant triggers early reorganization
    assert bc_short > m_short


main()
