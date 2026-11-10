"""CF9 lab L03-1: FX Transaction Exposure - Forwards, Money Market, and Options.

Demonstrates transaction exposure management for a foreign-currency receivable:
1. Covered Interest Parity (CIP) synthetic forward pricing.
2. Exact cash flow equivalence between Forward Cover and Money Market Hedge.
3. Garman-Kohlhagen (1983) currency option pricing and asymmetric payoff profile.
4. Downside protection vs upside participation under extreme exchange rate shocks.
Standard library only; deterministic execution.
"""

from __future__ import annotations

import math
from statistics import NormalDist


def garman_kohlhagen_put(spot: float, strike: float, t: float, r_d: float, r_f: float, sigma: float) -> float:
    """Compute European currency put price using Garman-Kohlhagen (1983) formula."""
    if t <= 0.0 or sigma <= 0.0:
        return max(0.0, strike - spot)

    dist = NormalDist()
    d1 = (math.log(spot / strike) + (r_d - r_f + 0.5 * sigma**2) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)

    put_price = strike * math.exp(-r_d * t) * dist.cdf(-d2) - spot * math.exp(-r_f * t) * dist.cdf(-d1)
    return max(0.0, put_price)


def evaluate_transaction_hedges(
    receivable_eur: float = 10_000_000.0,
    s0: float = 1.1000,
    r_usd: float = 0.05,
    r_eur: float = 0.03,
    vol: float = 0.10,
    t: float = 1.0,
) -> dict[str, float]:
    """Compare unhedged, forward, money-market, and put option hedges for committed receivable."""
    # 1. Forward contract rate via CIP
    forward_rate = s0 * ((1.0 + r_usd) / (1.0 + r_eur))
    forward_proceeds = receivable_eur * forward_rate

    # 2. Money market hedge mechanics
    eur_borrowed = receivable_eur / (1.0 + r_eur)
    usd_converted = eur_borrowed * s0
    mm_proceeds = usd_converted * (1.0 + r_usd)

    # 3. Currency Put Option
    strike = s0  # At-the-money spot strike
    put_premium_per_eur = garman_kohlhagen_put(spot=s0, strike=strike, t=t, r_d=r_usd, r_f=r_eur, sigma=vol)
    total_premium_t0 = receivable_eur * put_premium_per_eur
    # Compounded future cost of premium at date T
    future_premium_cost = total_premium_t0 * (1.0 + r_usd)

    # Stress test exchange rate scenarios at T = 1
    scenarios = {
        "Severe Depreciation (-15%)": s0 * 0.85,
        "Moderate Depreciation (-5%)": s0 * 0.95,
        "Unchanged (0%)": s0,
        "Moderate Appreciation (+5%)": s0 * 1.05,
        "Severe Appreciation (+15%)": s0 * 1.15,
    }

    scenario_results: dict[str, dict[str, float]] = {}
    for name, s_t in scenarios.items():
        unhedged_val = receivable_eur * s_t
        fwd_val = forward_proceeds
        mm_val = mm_proceeds
        # Option payoff: exercise if S_T < K, else sell at spot S_T, minus future premium
        gross_option_val = receivable_eur * max(strike, s_t)
        net_option_val = gross_option_val - future_premium_cost

        scenario_results[name] = {
            "s_t": s_t,
            "unhedged": unhedged_val,
            "forward": fwd_val,
            "money_market": mm_val,
            "put_option": net_option_val,
        }

    return {
        "forward_rate": forward_rate,
        "forward_proceeds": forward_proceeds,
        "mm_proceeds": mm_proceeds,
        "cip_parity_diff": abs(forward_proceeds - mm_proceeds),
        "put_premium_per_eur": put_premium_per_eur,
        "total_premium_usd": total_premium_t0,
        "future_premium_usd": future_premium_cost,
        "scenario_results": scenario_results,  # type: ignore[dict-item]
    }


def main() -> None:
    print("CF9 Lab L03-1: FX Transaction Exposure Management")
    print("=================================================")

    receivable = 10_000_000.0  # EUR 10M
    s0 = 1.1000  # USD per EUR
    r_usd = 0.05
    r_eur = 0.03
    vol = 0.10

    res = evaluate_transaction_hedges(receivable_eur=receivable, s0=s0, r_usd=r_usd, r_eur=r_eur, vol=vol)

    print("1. Synthetic Pricing and CIP Arbitrage Parity:")
    print(f"   Spot exchange rate (S0):         ${s0:.4f}")
    print(f"   1-Year Forward rate (CIP):       ${res['forward_rate']:.4f}")
    print(f"   Forward contract proceeds:       ${res['forward_proceeds']:,.2f}")
    print(f"   Money market hedge proceeds:     ${res['mm_proceeds']:,.2f}")
    cip_exact = res["cip_parity_diff"] < 1e-4
    print(f"   CIP Equivalence Wedge:           ${res['cip_parity_diff']:,.4f} (Exact Parity: {cip_exact})")

    print("\n2. Currency Put Option Specification:")
    print(f"   Strike price (K):                ${s0:.4f} (ATM Spot)")
    print(f"   Put option premium per EUR:      ${res['put_premium_per_eur']:.4f}")
    print(f"   Total upfront premium:           ${res['total_premium_usd']:,.2f}")
    print(f"   Future value of option premium:  ${res['future_premium_usd']:,.2f}")

    print("\n3. Net Realized Cash Flows Across Exchange Rate Scenarios ($USD):")
    header = f"   {'Scenario':<28} {'Spot S_T':<10} {'Unhedged ($)':<15} {'Forward ($)':<15} {'Put Option ($)':<15}"
    print(header)
    print("   " + "-" * 85)

    scen_data: dict[str, dict[str, float]] = res["scenario_results"]  # type: ignore[assignment]
    for name, vals in scen_data.items():
        print(
            f"   {name:<28} ${vals['s_t']:<9.4f} ${vals['unhedged']:<14,.2f} "
            f"${vals['forward']:<14,.2f} ${vals['put_option']:<14,.2f}"
        )


main()
