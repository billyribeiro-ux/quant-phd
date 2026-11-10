"""Lab QR2-project-1: Rung 2 Completion Problem Solution Twin.

Implements discrete-event lag enforcement, square-root market impact calculation,
and left-purging boundary logic for cross-validation.
"""

from __future__ import annotations

import math


def compute_square_root_impact(
    quantity: float,
    price: float,
    volume: float,
    volatility: float,
    y_coeff: float = 0.5,
) -> float:
    """Calculates square-root market impact cost in currency units."""
    participation = quantity / volume
    price_impact = y_coeff * volatility * price * math.sqrt(participation)
    return quantity * price_impact


def is_order_eligible_for_fill(submitted_bar: int, current_bar: int, lag_bars: int) -> bool:
    """Enforces strictly positive execution lag."""
    return current_bar >= submitted_bar + lag_bars


def compute_left_purge_start(test_start: int, label_lookahead: int) -> int:
    """Computes starting index for left-purging window to eliminate overlapping label leakage."""
    return max(0, test_start - label_lookahead + 1)


def main() -> None:
    # 1. Verify impact calculation
    qty, px, vol, sigma = 2000.0, 150.0, 1_000_000.0, 0.025
    impact_cost = compute_square_root_impact(qty, px, vol, sigma, y_coeff=0.5)
    print(f"Impact Cost for {qty:.0f} shares @ ${px:.2f}: ${impact_cost:.2f}")

    # 2. Verify lag eligibility
    sub_bar = 10
    lag = 2
    for b in [10, 11, 12, 13]:
        eligible = is_order_eligible_for_fill(sub_bar, b, lag)
        status = "ELIGIBLE" if eligible else "BLOCKED (lag pending)"
        print(f"Bar {b}: order submitted at bar {sub_bar} with lag {lag} -> {status}")

    # 3. Verify left purge start
    test_start = 50
    lookahead = 5
    purge_start = compute_left_purge_start(test_start, lookahead)
    print(f"Test fold starts at {test_start} with {lookahead}-day labels: Purge window begins at {purge_start}")
    print(f"Total purged samples: {test_start - purge_start}")
    print("Completion lab twin executed successfully.")


main()
