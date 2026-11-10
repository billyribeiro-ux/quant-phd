"""CS1 project lab 3: Comprehensive Atlas A1 contract verification and CLI formatting simulation.

Verifies returns.py contract adherence and format(val, '.15g') CLI formatting.
SIMULATED prices.
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


def format_cli_output(values: list[float]) -> list[str]:
    """Format return values per Atlas A1 CLI contract: format(val, '.15g')."""
    return [format(val, ".15g") for val in values]


def main() -> None:
    prices = [100.0, 105.0, 99.75]
    simple_rets = simple_return(prices)
    log_rets = log_return(prices)

    cli_simple = format_cli_output(simple_rets)
    cli_log = format_cli_output(log_rets)

    print(f"simple CLI lines: {len(cli_simple)}")
    print(f"simple line 1: {cli_simple[0]}")
    print(f"simple line 2: {cli_simple[1]}")
    print(f"log CLI lines: {len(cli_log)}")
    print(f"log line 1: {cli_log[0]}")
    print(f"log line 2: {cli_log[1]}")
    print(f"simple value 1 close to 0.05: {math.isclose(simple_rets[0], 0.05, rel_tol=1e-12)}")


main()
