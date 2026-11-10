"""QR1 Lesson 5 Inline Lab 1: Tick data timestamp semantics and arrival-order hazards.

Demonstrates resolution of prevailing last trades from out-of-order tick streams
using exchange timestamps and deterministic sequence numbers, and quantifies
the error rate of naive arrival-order lookups.
Data: SIMULATED microstructure trade stream.
"""

from __future__ import annotations

import random
from typing import NamedTuple


class Tick(NamedTuple):
    timestamp: str  # Exchange timestamp YYYY-MM-DDTHH:MM:SS.fffZ
    seq: int  # Matching engine sequence number
    price: float
    volume: int
    arrival_order: int  # Intake order at feed handler


def last_trade_canonical(ticks: list[Tick], cutoff: str) -> float | None:
    """Find prevailing last trade by maximum (timestamp, seq) with timestamp <= cutoff."""
    eligible = [t for t in ticks if t.timestamp <= cutoff]
    if not eligible:
        return None
    best = max(eligible, key=lambda t: (t.timestamp, t.seq))
    return best.price


def last_trade_naive_arrival(ticks: list[Tick], cutoff: str) -> float | None:
    """Flawed heuristic: selects last eligible tick in physical arrival order."""
    eligible = [t for t in ticks if t.timestamp <= cutoff]
    if not eligible:
        return None
    # Sorts by arrival order (or takes last received)
    best = max(eligible, key=lambda t: t.arrival_order)
    return best.price


def main() -> None:
    rng = random.Random(1337)

    # Chronological trade sequence at exchange matching engine
    timestamps = [
        "2026-03-01T09:30:00.100Z",
        "2026-03-01T09:30:00.150Z",
        "2026-03-01T09:30:00.200Z",
        "2026-03-01T09:30:00.200Z",  # Simultaneous trade at 200 ms, seq 4
        "2026-03-01T09:30:00.350Z",
        "2026-03-01T09:30:00.400Z",
        "2026-03-01T09:30:00.500Z",
        "2026-03-01T09:30:00.650Z",
        "2026-03-01T09:30:00.700Z",
        "2026-03-01T09:30:00.850Z",
    ]

    prices = [100.10, 100.15, 100.20, 100.25, 100.20, 100.30, 100.35, 100.40, 100.30, 100.50]
    volumes = [100, 200, 50, 150, 300, 100, 250, 400, 100, 500]

    # Create canonical ticks
    true_ticks = [Tick(timestamps[i], i + 1, prices[i], volumes[i], 0) for i in range(len(timestamps))]

    # SIMULATED network jitter causing out-of-order delivery
    # Permute arrival order
    shuffled_indices = list(range(len(true_ticks)))
    rng.shuffle(shuffled_indices)

    received_ticks: list[Tick] = []
    for arrival_idx, orig_idx in enumerate(shuffled_indices):
        t = true_ticks[orig_idx]
        received_ticks.append(Tick(t.timestamp, t.seq, t.price, t.volume, arrival_idx))

    print(f"Total ticks processed: {len(received_ticks)}")
    print("\nTick Stream (Arrival Order vs Exchange (Time, Seq)):")
    for t in sorted(received_ticks, key=lambda x: x.arrival_order):
        print(f"  Arrival #{t.arrival_order:02d}: ex_ts={t.timestamp} seq={t.seq:02d} px={t.price:.2f} vol={t.volume}")

    # Evaluation decision cut-offs
    cutoffs = [
        "2026-03-01T09:30:00.120Z",
        "2026-03-01T09:30:00.180Z",
        "2026-03-01T09:30:00.200Z",
        "2026-03-01T09:30:00.300Z",
        "2026-03-01T09:30:00.450Z",
        "2026-03-01T09:30:00.600Z",
        "2026-03-01T09:30:00.750Z",
        "2026-03-01T09:30:00.900Z",
    ]

    print("\nPrevailing Last Trade Queries at Decision Cut-offs:")
    mismatches = 0
    for cutoff in cutoffs:
        canonical_px = last_trade_canonical(received_ticks, cutoff)
        naive_px = last_trade_naive_arrival(received_ticks, cutoff)
        is_err = canonical_px != naive_px
        if is_err:
            mismatches += 1
        err_flag = " [ERROR: ARRIVAL SKEW]" if is_err else " [OK]"
        print(f"  Cut-off {cutoff}: Canonical={canonical_px:.2f} Naive={naive_px:.2f}{err_flag}")

    print(f"\nTotal queries evaluated: {len(cutoffs)}")
    print(f"Queries corrupted by arrival-order processing: {mismatches}")


main()
