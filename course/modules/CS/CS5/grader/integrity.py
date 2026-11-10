"""Input validation and numerical integrity utilities for CS5 Monte Carlo pricer.

Validates parameter bounds, integer ranges, and float finiteness under the CS5 contract.
"""

from __future__ import annotations

import math

UINT64_MAX: int = (1 << 64) - 1


def validate_pricing_inputs(
    s0: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    n_paths: int,
    seed: int,
) -> None:
    """Validate numerical inputs for option pricing under the CS5 contract.

    Raises ValueError for non-finite floats, non-positive parameters, path counts
    less than 2, or out-of-range integer seeds.
    """
    for name, val in (
        ("s0", s0),
        ("strike", strike),
        ("rate", rate),
        ("vol", vol),
        ("maturity", maturity),
    ):
        if not isinstance(val, (int, float)) or not math.isfinite(val):
            raise ValueError(f"parameter {name} must be a finite real number; got {val}")

    if s0 <= 0.0:
        raise ValueError(f"spot price s0 must be strictly positive; got {s0}")
    if strike <= 0.0:
        raise ValueError(f"strike price must be strictly positive; got {strike}")
    if vol <= 0.0:
        raise ValueError(f"volatility vol must be strictly positive; got {vol}")
    if maturity <= 0.0:
        raise ValueError(f"maturity must be strictly positive; got {maturity}")

    if not isinstance(n_paths, int) or n_paths < 2:
        raise ValueError(f"number of paths n_paths must be an integer >= 2; got {n_paths}")

    if not isinstance(seed, int) or not (0 <= seed <= UINT64_MAX):
        raise ValueError(f"seed must be a 64-bit unsigned integer in [0, 2^64 - 1]; got {seed}")


def validate_stream_inputs(seed: int, count: int) -> None:
    """Validate inputs for the random number stream generator.

    Raises ValueError if count < 0 or seed is not a valid 64-bit unsigned integer.
    """
    if not isinstance(seed, int) or not (0 <= seed <= UINT64_MAX):
        raise ValueError(f"seed must be a 64-bit unsigned integer in [0, 2^64 - 1]; got {seed}")
    if not isinstance(count, int) or count < 0:
        raise ValueError(f"stream count must be a non-negative integer; got {count}")
