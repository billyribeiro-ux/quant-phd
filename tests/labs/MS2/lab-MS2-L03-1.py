"""Lab MS2-L03-1: Reg NMS order protection and ISO routing simulator.

Simulates order routing across fragmented lit exchanges under Reg NMS Rule 611,
evaluating sequential routing vs Intermarket Sweep Orders (ISO) across SIP latency delays.
"""

from __future__ import annotations

import random


def simulate_routing(
    n_orders: int,
    sip_latency_ms: float,
    quote_fade_prob_per_ms: float,
    rng: random.Random,
) -> tuple[float, float, float]:
    """Compare sequential Reg NMS routing against simultaneous ISO routing.

    Returns:
        (iso_fill_rate, seq_fill_rate, seq_slippage_bps)
    """
    iso_fills = 0
    seq_fills = 0
    seq_slippage_sum = 0.0

    for _ in range(n_orders):
        # Order arrives wanting 2 lots at the NBBO
        # Exchange A has 1 lot at 100.00; Exchange B has 1 lot at 100.00
        # Both exchanges define the NBBO = 100.00.

        # ISO strategy: sends 1 lot to Ex A and 1 lot to Ex B simultaneously
        # Transit time to both is direct (approx 0 ms relative to SIP)
        # Likelihood of fill is high because quotes haven't faded
        iso_filled = 2
        iso_fills += iso_filled

        # Sequential Reg NMS routing:
        # 1. First lot hits Exchange A at t=0 and executes at 100.00.
        # 2. Exchange A routes second lot to Exchange B through SIP broker routing.
        # Transit delay = sip_latency_ms.
        # During transit, probability that Exchange B's quote fades or is picked off:
        fade_prob = min(1.0, sip_latency_ms * quote_fade_prob_per_ms)
        if rng.random() < fade_prob:
            # Quote on B faded! Second lot must execute at inferior price (e.g. 100.02)
            # 1 lot at 100.00, 1 lot at 100.02 -> avg price 100.01 (+1 bp slippage)
            seq_fills += 2
            seq_slippage_sum += 1.0  # 1 bp slippage on total order
        else:
            # Quote still intact on B
            seq_fills += 2
            seq_slippage_sum += 0.0

    iso_rate = iso_fills / (2 * n_orders)
    seq_rate = seq_fills / (2 * n_orders)
    mean_slippage = seq_slippage_sum / n_orders

    return iso_rate, seq_rate, mean_slippage


def main() -> None:
    rng = random.Random(42)
    n_orders = 2000
    quote_fade_per_ms = 0.08  # 8% chance per millisecond of quote change

    latencies = [0.5, 1.0, 2.0, 5.0, 10.0]  # ms

    print("Reg NMS Order Protection: Sequential vs ISO Routing (N=2000 orders):")
    print("SIP Delay (ms) | ISO Fill Rate | Seq Fill Rate | Seq Slippage (bps) | Fade Prob")
    print("-------------------------------------------------------------------------------")

    for lat in latencies:
        iso_rate, seq_rate, slippage = simulate_routing(
            n_orders,
            lat,
            quote_fade_per_ms,
            rng,
        )
        fade_prob = min(1.0, lat * quote_fade_per_ms)
        print(f"     {lat:4.1f}      | {iso_rate:13.4f} | {seq_rate:13.4f} | {slippage:18.4f} | {fade_prob:9.4f}")


main()
