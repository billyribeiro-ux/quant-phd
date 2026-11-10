"""Lab MS2-L01-1: Queue-position simulator.

Simulates FIFO limit order queue priority at the best bid, computing fill
probability and execution time as a function of initial queue position k.
"""

from __future__ import annotations

import random


def simulate_queue(
    initial_queue_size: int,
    target_pos: int,
    market_sell_rate: float,
    cancel_rate_per_order: float,
    limit_arrival_rate: float,
    max_time: float,
    rng: random.Random,
) -> tuple[bool, float]:
    """Simulate a single FIFO queue realization until target order fills or expires.

    Returns:
        (filled, time_elapsed)
    """
    pos = target_pos
    queue_len = initial_queue_size
    current_time = 0.0

    while current_time < max_time and pos > 0:
        total_cancel_rate = cancel_rate_per_order * queue_len
        total_rate = market_sell_rate + total_cancel_rate + limit_arrival_rate
        if total_rate <= 0.0:
            break

        dt = rng.expovariate(total_rate)
        current_time += dt
        if current_time >= max_time:
            break

        u = rng.random() * total_rate
        if u < market_sell_rate:
            # Market sell executes against the head of the queue
            pos -= 1
            queue_len = max(0, queue_len - 1)
        elif u < market_sell_rate + total_cancel_rate:
            # A cancellation occurs uniformly in the queue
            cancel_idx = rng.randint(1, max(1, queue_len))
            if cancel_idx < pos:
                pos -= 1
            queue_len = max(0, queue_len - 1)
        else:
            # A new limit order joins the back of the queue
            queue_len += 1

    return pos == 0, current_time


def main() -> None:
    rng = random.Random(42)
    n_sims = 2500
    queue_depth = 20
    market_sell_rate = 2.0  # orders per second
    cancel_rate_per_order = 0.05  # per order per second
    limit_arrival_rate = 1.8  # orders per second
    time_horizon = 4.0  # seconds

    positions = [1, 5, 10, 15, 20]

    print("Queue-Position Simulation Results (N=2500 per position, depth=20, T=4.0s):")
    print("Pos (k) | Fill Prob | Mean Fill Time (s) | Relative Fill")
    print("---------------------------------------------------------")

    p1_prob = 0.0
    for k in positions:
        fills = 0
        fill_times: list[float] = []
        for _ in range(n_sims):
            filled, t = simulate_queue(
                queue_depth,
                k,
                market_sell_rate,
                cancel_rate_per_order,
                limit_arrival_rate,
                time_horizon,
                rng,
            )
            if filled:
                fills += 1
                fill_times.append(t)

        prob = fills / n_sims
        if k == 1:
            p1_prob = prob
        rel_fill = prob / p1_prob if p1_prob > 0 else 0.0
        mean_time = sum(fill_times) / len(fill_times) if fill_times else float("nan")

        print(f"{k:7d} | {prob:9.4f} | {mean_time:18.4f} | {rel_fill:13.4f}")


main()
