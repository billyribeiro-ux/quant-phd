"""Lab MS2-L05-1: Budish-Cramton-Shim latency arbitrage simulator.

Simulates cross-asset public news arrivals, quote sniping, and latency arbitrage rents
in a continuous limit order book as the number of competing snipers N varies.
"""

from __future__ import annotations

import random


def simulate_latency_race(
    n_jumps: int,
    n_snipers: int,
    half_spread: float,
    jump_size: float,
    mm_latency: float,
    sniper_mean_latency: float,
    rng: random.Random,
) -> tuple[float, float, float]:
    """Simulate public jump innovations and races between market maker and N snipers.

    Returns:
        (total_sniper_rent, mm_loss, avg_rent_per_sniper)
    """
    total_rent = 0.0

    for _ in range(n_jumps):
        # Public innovation occurs: jump_size > half_spread
        # MM attempts to cancel:
        mm_cancel_time = rng.expovariate(1.0 / mm_latency)

        # N snipers race to pick off the quote:
        sniper_times = [rng.expovariate(1.0 / sniper_mean_latency) for _ in range(n_snipers)]
        fastest_sniper_time = min(sniper_times)

        # If fastest sniper arrives before MM cancel request:
        if fastest_sniper_time < mm_cancel_time:
            rent = jump_size - half_spread
            total_rent += rent

    mm_loss = total_rent
    per_sniper_rent = total_rent / n_snipers if n_snipers > 0 else 0.0

    return total_rent, mm_loss, per_sniper_rent


def main() -> None:
    rng = random.Random(42)
    n_jumps = 1000
    half_spread = 0.05
    jump_size = 0.20  # $0.20 jump, net rent = 0.20 - 0.05 = $0.15 per sniped lot
    mm_latency = 2.0  # mean 2.0 ms
    sniper_mean_lat = 0.8  # mean 0.8 ms (snipers are systematically faster)

    sniper_counts = [1, 2, 5, 10, 20]

    print("Budish-Cramton-Shim (2015) Latency Race Simulation (N=1000 jumps):")
    print("Snipers (K) | Total Rent ($) | MM Loss ($) | Rent per Sniper ($) | Sniped Pct")
    print("-----------------------------------------------------------------------------")

    for k in sniper_counts:
        total_rent, mm_loss, per_sniper = simulate_latency_race(
            n_jumps,
            k,
            half_spread,
            jump_size,
            mm_latency,
            sniper_mean_lat,
            rng,
        )
        sniped_pct = (total_rent / (n_jumps * (jump_size - half_spread))) * 100.0

        print(f"    {k:2d}      | ${total_rent:12.2f} | ${mm_loss:9.2f} | ${per_sniper:17.2f} | {sniped_pct:9.2f}%")


main()
