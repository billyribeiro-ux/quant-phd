"""CS1 project lab 1: Worked example of Atlas A1 returns computation and invariant checks.

Demonstrates simple and log return calculation, input validation, and tolerance-checked invariants.
SIMULATED synthetic equity price trajectory.
"""

from __future__ import annotations

import math
from collections.abc import Sequence


def simple_return(prices: Sequence[float]) -> list[float]:
    """Compute simple returns: r_t = P_t / P_{t-1} - 1."""
    if len(prices) < 2:
        raise ValueError("At least 2 prices are required")
    out: list[float] = []
    p_prev = float(prices[0])
    if not math.isfinite(p_prev) or p_prev <= 0.0:
        raise ValueError(f"Price must be finite and positive, got {p_prev}")
    for p in prices[1:]:
        p_curr = float(p)
        if not math.isfinite(p_curr) or p_curr <= 0.0:
            raise ValueError(f"Price must be finite and positive, got {p_curr}")
        out.append(p_curr / p_prev - 1.0)
        p_prev = p_curr
    return out


def log_return(prices: Sequence[float]) -> list[float]:
    """Compute log returns: ell_t = ln(P_t / P_{t-1})."""
    if len(prices) < 2:
        raise ValueError("At least 2 prices are required")
    out: list[float] = []
    p_prev = float(prices[0])
    if not math.isfinite(p_prev) or p_prev <= 0.0:
        raise ValueError(f"Price must be finite and positive, got {p_prev}")
    for p in prices[1:]:
        p_curr = float(p)
        if not math.isfinite(p_curr) or p_curr <= 0.0:
            raise ValueError(f"Price must be finite and positive, got {p_curr}")
        out.append(math.log(p_curr / p_prev))
        p_prev = p_curr
    return out


def main() -> None:
    # SIMULATED prices for 5 trading days
    simulated_prices = [100.0, 102.5, 101.0, 104.0, 106.6]
    r = simple_return(simulated_prices)
    ell = log_return(simulated_prices)

    print(f"input price count: {len(simulated_prices)}")
    print(f"return count: {len(r)}")
    print(f"first simple return: {r[0]:.6f}")
    print(f"first log return: {ell[0]:.6f}")

    # Check invariant: ell[t] == ln(1 + r[t])
    invariant_diffs = [abs(ell[t] - math.log(1.0 + r[t])) for t in range(len(r))]
    max_diff = max(invariant_diffs)
    print(f"invariant holds within 1e-12: {max_diff < 1e-12}")

    # Check compounding
    cum_simple = 1.0
    for ret in r:
        cum_simple *= 1.0 + ret
    cum_simple -= 1.0
    expected_simple = simulated_prices[-1] / simulated_prices[0] - 1.0
    print(f"cumulative simple return matches price ratio: {abs(cum_simple - expected_simple) < 1e-12}")

    # Check log sum
    sum_log = sum(ell)
    expected_log = math.log(simulated_prices[-1] / simulated_prices[0])
    print(f"cumulative log return matches log price ratio: {abs(sum_log - expected_log) < 1e-12}")


main()
