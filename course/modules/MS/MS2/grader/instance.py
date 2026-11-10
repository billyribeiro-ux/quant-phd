"""Instance generator for MS2 project: Batch-auction counterfactual.

Generates deterministic event streams and market parameters for seeds 0-49.
"""

from __future__ import annotations

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic problem instance for MS2 project."""
    rng = random.Random(seed)

    n_events = 80 + (seed * 17) % 61  # Deterministic event count between 80 and 140
    initial_price = 100.0
    half_spread = round(0.02 + ((seed * 13) % 60) * 0.001, 4)
    mm_latency = round(2.0 + ((seed * 7) % 15) * 0.1, 2)
    sniper_count = 2 + (seed % 3)
    sniper_latencies = sorted(round(0.5 + ((seed * 11 + i * 23) % 13) * 0.1, 2) for i in range(sniper_count))
    batch_interval = float([50.0, 100.0, 200.0][seed % 3])
    batch_intervals = [10.0, 50.0, 100.0, 250.0, 500.0]

    events: list[tuple[float, str, float, int]] = []
    current_time = 0.0
    for _ in range(n_events):
        dt = round(rng.expovariate(0.05), 2) + 0.1
        current_time += dt
        u = rng.random()
        if u < 0.25:
            # Price jump event
            delta = round(rng.choice([-1.0, 1.0]) * rng.uniform(0.10, 0.30), 4)
            events.append((round(current_time, 2), "jump", delta, 1))
        elif u < 0.625:
            # Investor buy
            events.append((round(current_time, 2), "investor_buy", 0.0, 1))
        else:
            # Investor sell
            events.append((round(current_time, 2), "investor_sell", 0.0, 1))

    return {
        "seed": seed,
        "n_events": n_events,
        "initial_price": initial_price,
        "half_spread": half_spread,
        "mm_latency": mm_latency,
        "sniper_latencies": sniper_latencies,
        "batch_interval": batch_interval,
        "batch_intervals": batch_intervals,
        "events": events,
    }
