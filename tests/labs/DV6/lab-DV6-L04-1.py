"""Lab 4 · Dealer Gamma Positioning, Vanna/Volga & Expiration Pinning Mechanics.

Aggregates dealer gamma exposure (GEX) across option strikes and structured product
barriers, and simulates the Ni, Pearson & Poteshman (2005) expiration strike pinning
dynamic driven by delta rebalancing feedback on seed 42 (SIMULATED).
"""

from __future__ import annotations

import math

import numpy as np


def norm_pdf(x: float) -> float:
    """Probability density function of standard normal distribution."""
    return (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * x * x)


def bs_gamma(s: float, k: float, t: float, r: float, q: float, sigma: float) -> float:
    """Option gamma d^2V / dS^2 under Black-Scholes."""
    if t <= 0.0 or sigma <= 0.0 or s <= 0.0:
        return 0.0
    d1 = (math.log(s / k) + (r - q + 0.5 * sigma * sigma) * t) / (sigma * math.sqrt(t))
    return float(math.exp(-q * t) * norm_pdf(d1) / (s * sigma * math.sqrt(t)))


def calculate_dealer_gex(
    spot: float,
    strikes: list[float],
    dealer_net_contracts: list[float],
    t: float,
    r: float,
    q: float,
    sigma: float,
) -> float:
    """Calculate aggregate dealer gamma exposure (GEX in USD per 1% spot move)."""
    total_gex = 0.0
    for k, contracts in zip(strikes, dealer_net_contracts, strict=True):
        gamma_k = bs_gamma(spot, k, t, r, q, sigma)
        # 1 contract = 100 shares. GEX_USD_1pct = Gamma * Spot * (0.01 * Spot) * 100 * Contracts
        gex_k = gamma_k * (spot**2) * 0.01 * 100.0 * contracts
        total_gex += gex_k
    return total_gex


def simulate_expiration_pinning(
    s0: float,
    pin_strike: float,
    dealer_gamma_shares: float,
    market_depth: float,
    sigma: float,
    t_hours: float = 6.5,
    n_steps: int = 390,  # 1-minute steps over trading day
    n_sims: int = 5000,
    seed: int = 42,
) -> dict[str, float]:
    """Simulate stock price paths into expiration with and without dealer hedging feedback.

    Following Ni, Pearson & Poteshman (2005):
    Under long dealer gamma, dealer delta is Delta(S).
    If price moves dS, dealer rebalances -Gamma * dS shares.
    Market impact of dealer flow is: dS_hedging = -(Dealer_Gamma / Market_Depth) * dS_exogenous.
    Effective price return: dS_net = dS_exogenous / (1 + Dealer_Gamma / Market_Depth).
    """
    rng = np.random.default_rng(seed)
    dt = (t_hours / (252.0 * 6.5)) / float(n_steps)
    sqrt_dt = math.sqrt(dt)

    z = rng.standard_normal((n_sims, n_steps))

    # Without dealer hedging feedback (unpinned exogenous GBM)
    s_unpinned = np.empty((n_sims, n_steps + 1))
    s_unpinned[:, 0] = s0

    # With dealer hedging feedback (pinned)
    s_pinned = np.empty((n_sims, n_steps + 1))
    s_pinned[:, 0] = s0

    for step in range(n_steps):
        # Exogenous innovation
        dw = z[:, step] * sqrt_dt
        exo_shock = sigma * dw

        # Unpinned step
        s_u = s_unpinned[:, step]
        s_unpinned[:, step + 1] = s_u * (1.0 + exo_shock)

        # Pinned step: feedback strength depends on gamma near strike
        s_p = s_pinned[:, step]
        # Local dealer gamma concentrated near strike (bell curve profile around pin_strike)
        gamma_local = dealer_gamma_shares * np.exp(-0.5 * ((s_p - pin_strike) / 1.0) ** 2)
        feedback_dampening = 1.0 / (1.0 + gamma_local / market_depth)
        net_shock = exo_shock * feedback_dampening
        s_pinned[:, step + 1] = s_p * (1.0 + net_shock)

    terminal_unpinned = s_unpinned[:, -1]
    terminal_pinned = s_pinned[:, -1]

    # Fraction of paths closing within 0.25 USD of pin strike
    cluster_unpinned = float(np.mean(np.abs(terminal_unpinned - pin_strike) <= 0.25))
    cluster_pinned = float(np.mean(np.abs(terminal_pinned - pin_strike) <= 0.25))
    vol_unpinned = float(np.std(terminal_unpinned - s0))
    vol_pinned = float(np.std(terminal_pinned - s0))

    return {
        "cluster_unpinned": cluster_unpinned,
        "cluster_pinned": cluster_pinned,
        "terminal_vol_unpinned": vol_unpinned,
        "terminal_vol_pinned": vol_pinned,
    }


def main() -> None:
    spot = 100.0
    pin_strike = 100.0
    strikes = [90.0, 95.0, 100.0, 105.0, 110.0]
    # Positive indicates dealer long gamma (investors bought puts / sold covered calls)
    net_contracts = [5000.0, 12000.0, 25000.0, 15000.0, 4000.0]
    t = 1.0 / 252.0  # 1 day to expiration
    rate = 0.04
    div_yield = 0.01
    vol = 0.20

    # 1. Dealer Gamma Exposure (GEX) profile
    gex_at_spot = calculate_dealer_gex(spot, strikes, net_contracts, t, rate, div_yield, vol)
    gex_down = calculate_dealer_gex(spot * 0.98, strikes, net_contracts, t, rate, div_yield, vol)
    gex_up = calculate_dealer_gex(spot * 1.02, strikes, net_contracts, t, rate, div_yield, vol)

    # 2. Expiration pinning simulation
    dealer_gamma_shares = 150000.0
    market_depth = 100000.0
    sim_res = simulate_expiration_pinning(
        spot, pin_strike, dealer_gamma_shares, market_depth, vol, n_sims=10000, seed=42
    )

    print("=== Lab 4: Dealer Gamma Exposure (GEX) & Expiration Pinning ===")
    print(f"Dealer Net GEX at Spot ($100):     ${gex_at_spot:,.2f} per 1% move")
    print(f"Dealer Net GEX at Spot ($98):      ${gex_down:,.2f} per 1% move")
    print(f"Dealer Net GEX at Spot ($102):     ${gex_up:,.2f} per 1% move")
    print("\nExpiration Day Pinning Results (Ni, Pearson & Poteshman 2005):")
    print(f"  Unpinned Strike Clustering:      {sim_res['cluster_unpinned'] * 100.0:.2f}%")
    print(f"  Dealer-Pinned Strike Clustering: {sim_res['cluster_pinned'] * 100.0:.2f}%")
    surge_pct = (sim_res["cluster_pinned"] - sim_res["cluster_unpinned"]) * 100.0
    print(f"  Clustering Probability Surge:    +{surge_pct:.2f}%")
    print(f"  Unpinned Realized Volatility:    {sim_res['terminal_vol_unpinned']:.4f}")
    print(f"  Dealer Pinned Realized Vol:      {sim_res['terminal_vol_pinned']:.4f}")


main()
