"""Lab MS2-project-2: Rung 2 completion problem for latency rent calculation.

SIMULATED: generates jump and snipe events.
On the project page, the latency rent calculation line is blanked:
rent = ___
The twin contains the complete solution.
"""

from __future__ import annotations


def calculate_snipe_rent(
    mid_price: float,
    half_spread: float,
    price_delta: float,
    size: int,
    fastest_sniper: float,
    mm_latency: float,
) -> float:
    """Calculate latency arbitrage rent extracted by fastest sniper."""
    if fastest_sniper >= mm_latency:
        return 0.0

    if price_delta > half_spread:
        # Sniper buys stale ask = mid_price + half_spread
        exec_price = mid_price + half_spread
        new_mid = mid_price + price_delta
        rent = (new_mid - exec_price) * size
        return rent
    elif price_delta < -half_spread:
        # Sniper sells stale bid = mid_price - half_spread
        exec_price = mid_price - half_spread
        new_mid = mid_price + price_delta
        rent = (exec_price - new_mid) * size
        return rent
    return 0.0


def main() -> None:
    mid = 100.0
    half_spread = 0.05
    size = 10
    mm_latency = 2.0
    fastest_sniper = 0.8

    jumps = [0.15, -0.20, 0.03, -0.04, 0.25]

    print("Rung 2 Snipe Rent Calculation (mid=100.00, half_spread=0.05, size=10):")
    print("Jump Delta ($) | Fastest Snipe (ms) | MM Cancel (ms) | Rent Extracted ($)")
    print("------------------------------------------------------------------------")

    total_rent = 0.0
    for delta in jumps:
        rent = calculate_snipe_rent(mid, half_spread, delta, size, fastest_sniper, mm_latency)
        total_rent += rent
        print(
            f"    {delta:6.2f}     |        {fastest_sniper:3.1f}         |"
            f"      {mm_latency:3.1f}       | ${rent:18.2f}"
        )

    print(f"Total Latency Arbitrage Rents: ${total_rent:.2f}")


main()
