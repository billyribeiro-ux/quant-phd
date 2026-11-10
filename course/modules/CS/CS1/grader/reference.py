"""Reference implementation of Atlas A1 returns module: simple_return and log_return.

Adheres strictly to atlas/A1.contract.md.
"""

from __future__ import annotations

import math
from collections.abc import Sequence


def simple_return(prices: Sequence[float]) -> list[float]:
    """Compute simple (arithmetic) returns: r_t = P_t / P_{t-1} - 1.

    Args:
        prices: Sequence of positive finite price levels.

    Returns:
        List of simple returns of length len(prices) - 1.

    Raises:
        ValueError: If len(prices) < 2, or any price is non-finite or <= 0.
        TypeError: If elements are not real numbers.
    """
    if len(prices) < 2:
        raise ValueError(f"simple_return requires at least 2 prices, got {len(prices)}")

    out: list[float] = []
    p0 = prices[0]
    if isinstance(p0, bool) or not isinstance(p0, (int, float)):
        raise TypeError(f"Price must be a real number, got {type(p0).__name__}")
    p_prev = float(p0)
    if not math.isfinite(p_prev) or p_prev <= 0.0:
        raise ValueError(f"Price must be finite and strictly positive, got {p_prev}")

    for p in prices[1:]:
        if isinstance(p, bool) or not isinstance(p, (int, float)):
            raise TypeError(f"Price must be a real number, got {type(p).__name__}")
        p_curr = float(p)
        if not math.isfinite(p_curr) or p_curr <= 0.0:
            raise ValueError(f"Price must be finite and strictly positive, got {p_curr}")
        out.append(p_curr / p_prev - 1.0)
        p_prev = p_curr

    return out


def log_return(prices: Sequence[float]) -> list[float]:
    """Compute continuously compounded (log) returns: ell_t = ln(P_t / P_{t-1}).

    Args:
        prices: Sequence of positive finite price levels.

    Returns:
        List of log returns of length len(prices) - 1.

    Raises:
        ValueError: If len(prices) < 2, or any price is non-finite or <= 0.
        TypeError: If elements are not real numbers.
    """
    if len(prices) < 2:
        raise ValueError(f"log_return requires at least 2 prices, got {len(prices)}")

    out: list[float] = []
    p0 = prices[0]
    if isinstance(p0, bool) or not isinstance(p0, (int, float)):
        raise TypeError(f"Price must be a real number, got {type(p0).__name__}")
    p_prev = float(p0)
    if not math.isfinite(p_prev) or p_prev <= 0.0:
        raise ValueError(f"Price must be finite and strictly positive, got {p_prev}")

    for p in prices[1:]:
        if isinstance(p, bool) or not isinstance(p, (int, float)):
            raise TypeError(f"Price must be a real number, got {type(p).__name__}")
        p_curr = float(p)
        if not math.isfinite(p_curr) or p_curr <= 0.0:
            raise ValueError(f"Price must be finite and strictly positive, got {p_curr}")
        out.append(math.log(p_curr / p_prev))
        p_prev = p_curr

    return out
