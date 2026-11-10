"""CS1 project lab 2: Completion problem solution for return calculations.

Tests core return computation logic and input validation on SIMULATED price quotes.
"""

from __future__ import annotations

import math
from collections.abc import Sequence


def validate_prices(prices: Sequence[float]) -> None:
    if len(prices) < 2:
        raise ValueError("prices sequence must have length >= 2")
    for p in prices:
        val = float(p)
        if not math.isfinite(val) or val <= 0.0:
            raise ValueError("each price must be finite and positive")


def compute_pair_returns(p_prev: float, p_curr: float) -> tuple[float, float]:
    r_t = p_curr / p_prev - 1.0
    ell_t = math.log(p_curr / p_prev)
    return r_t, ell_t


def main() -> None:
    # SIMULATED quote path
    quotes: tuple[float, ...] = (50.0, 52.0, 51.0, 53.55)
    validate_prices(quotes)

    simple_rets: list[float] = []
    log_rets: list[float] = []
    for i in range(1, len(quotes)):
        r, ell = compute_pair_returns(quotes[i - 1], quotes[i])
        simple_rets.append(r)
        log_rets.append(ell)

    print(f"validated quote count: {len(quotes)}")
    print(f"computed pairs count: {len(simple_rets)}")
    print(f"first simple return: {simple_rets[0]:.6f}")
    print(f"first log return: {log_rets[0]:.6f}")
    invariant_check = abs(log_rets[0] - math.log(1.0 + simple_rets[0])) < 1e-12
    print(f"first return invariant holds: {invariant_check}")
    total_compounded = math.prod(1.0 + x for x in simple_rets)
    expected_ratio = quotes[-1] / quotes[0]
    print(f"compounding ratio matches: {abs(total_compounded - expected_ratio) < 1e-12}")


main()
