"""Starter stub for CS5 Monte Carlo pricing project.

Implement the SplitMix64 generator and European option pricer according to the specification.
"""

from __future__ import annotations


def rng_stream(seed: int, count: int) -> list[int]:
    """Generate the first `count` 64-bit unsigned integers from SplitMix64."""
    raise NotImplementedError("Student implementation of rng_stream required")


def price_call_and_put(
    s0: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    n_paths: int,
    seed: int,
) -> tuple[float, float, float, float]:
    """Price European call and put options with Monte Carlo simulation."""
    raise NotImplementedError("Student implementation of price_call_and_put required")
