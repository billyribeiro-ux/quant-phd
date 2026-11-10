"""Lab BK2-L02-1: ETF creation-redemption mechanism and arbitrage bounds.

Simulates the primary-secondary market interaction: Authorized Participants
arbitrage price discrepancies between the ETF secondary market price and the
intraday indicative value (IIV) of the underlying basket whenever the spread
exceeds creation/redemption transaction costs.
"""

from __future__ import annotations

import random


def simulate_etf_arbitrage(
    days: int,
    create_cost_bps: float,
    redeem_cost_bps: float,
    seed: int = 42,
) -> dict[str, float]:
    """Simulate secondary ETF market prices and AP creation/redemption arbitrage."""
    rng = random.Random(seed)
    create_cost = create_cost_bps / 10_000.0
    redeem_cost = redeem_cost_bps / 10_000.0

    nav = 100.0
    etf_price = 100.0

    creations = 0
    redemptions = 0
    premium_discounts: list[float] = []

    for _ in range(days):
        # Underlying basket return shock
        basket_ret = rng.gauss(0.0004, 0.012)
        nav *= 1.0 + basket_ret

        # Secondary market retail demand noise shock on ETF share price (proportional)
        demand_noise = rng.gauss(0.0, 0.0035)
        raw_etf_price = etf_price * (1.0 + basket_ret + demand_noise)

        premium = (raw_etf_price - nav) / nav

        # AP Arbitrage conditions
        if premium > create_cost:
            # ETF trades at a premium exceeding creation costs: AP creates shares
            etf_price = nav * (1.0 + create_cost)
            creations += 1
        elif premium < -redeem_cost:
            # ETF trades at a discount exceeding redemption costs: AP redeems shares
            etf_price = nav * (1.0 - redeem_cost)
            redemptions += 1
        else:
            # Inside no-arbitrage band: price floats without primary market creation
            etf_price = raw_etf_price

        realized_spread = (etf_price - nav) / nav
        premium_discounts.append(realized_spread)

    mean_spread_bps = (sum(premium_discounts) / len(premium_discounts)) * 10_000.0
    max_premium_bps = max(premium_discounts) * 10_000.0
    max_discount_bps = min(premium_discounts) * 10_000.0

    return {
        "days": float(days),
        "creations": float(creations),
        "redemptions": float(redemptions),
        "mean_spread_bps": mean_spread_bps,
        "max_premium_bps": max_premium_bps,
        "max_discount_bps": max_discount_bps,
    }


def main() -> None:
    days = 250
    create_bps = 15.0
    redeem_bps = 15.0

    res = simulate_etf_arbitrage(days, create_bps, redeem_bps, seed=42)

    print("ETF Creation/Redemption Arbitrage Simulator")
    print("------------------------------------------")
    print(f"Trading horizon:           {int(res['days'])} days")
    print(f"Creation threshold:        +{create_bps:.1f} bps")
    print(f"Redemption threshold:      -{redeem_bps:.1f} bps")
    print(f"Creation events triggered: {int(res['creations'])}")
    print(f"Redemption events:         {int(res['redemptions'])}")
    print(f"Mean premium/discount:     {res['mean_spread_bps']:.2f} bps")
    print(f"Max observed premium:      {res['max_premium_bps']:.2f} bps")
    print(f"Max observed discount:     {res['max_discount_bps']:.2f} bps")


main()
