"""Instance generator for the MS1 project autograder.

SIMULATED: generates synthetic trade prices and trade directions under the repeated-trade
microstructure model with known order-processing cost c, adverse-selection parameter theta,
and efficient price shock volatility sigma.
"""

from __future__ import annotations

import random


def make_instance(seed: int) -> dict[str, object]:
    """Generate a deterministic synthetic trade sequence for testing spread decomposition."""
    rng = random.Random(seed)
    n = 400 + (seed * 37) % 1601  # n in [400, 2000]

    # Seed 0 has theta = 0.0 to test the classical Roll identity
    theta = 0.0 if seed == 0 else round(rng.uniform(0.02, 0.45), 4)

    c = round(rng.uniform(0.08, 0.40), 4)
    sigma = round(rng.uniform(0.02, 0.08), 4)
    m = 100.0

    prices: list[float] = []
    signs: list[int] = []

    for _ in range(n):
        q = rng.choice([-1, 1])
        eta = rng.gauss(0.0, sigma)
        m += theta * q + eta
        prices.append(round(m + c * q, 6))
        signs.append(q)

    # Ensure signs vary (cannot be all equal)
    if all(s == signs[0] for s in signs):
        signs[0] = -signs[0]

    return {
        "prices": prices,
        "signs": signs,
        "n": n,
        "theta": theta,
        "c": c,
        "sigma": sigma,
    }
