"""Per-learner instances for the SC6 autograder of the HJB solver (hjb_solver.py). All values are SIMULATED.

``make_instance(seed)`` is deterministic and uses only the standard library. From the seed alone it draws:

* risk-free rate r in [0.015, 0.045];
* expected stock return mu in [r + 0.03, r + 0.08];
* stock volatility sigma in [0.15, 0.30];
* relative risk aversion gamma in [1.5, 3.5];
* subjective discount rate rho in [0.04, 0.08];
* borrowing constraint upper bound pi_max;
* wealth grid bounds w_min in [0.8, 1.2], w_max in [w_min + 2.5, w_min + 4.5], and grid size n_points in {81, 101, 121}.

The instance carries the seed and the label "SIMULATED". Nothing here is a real market, a real price or a real asset.
"""

from __future__ import annotations

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """A deterministic SIMULATED instance for ``seed``. Every instance is valid under the project specification."""
    rng = random.Random(3_000_017 * int(seed) + 87_654)
    r = round(rng.uniform(0.015, 0.045), 4)
    mu = round(r + rng.uniform(0.03, 0.08), 4)
    sigma = round(rng.uniform(0.15, 0.30), 4)
    gamma = round(rng.uniform(1.5, 3.5), 2)
    rho = round(rng.uniform(0.04, 0.08), 4)

    # Theoretical unconstrained Merton fraction
    pi_star = (mu - r) / (gamma * sigma**2)

    # Upper bound multiplier: roughly half above pi_star and half below
    mult = rng.uniform(0.5, 1.5)
    pi_max = round(mult * pi_star, 4)
    if pi_max < 0.20:
        pi_max = 0.20

    w_min = round(rng.uniform(0.8, 1.2), 2)
    w_max = round(w_min + rng.uniform(2.5, 4.5), 2)
    n_points = rng.choice([81, 101, 121])

    dw = (w_max - w_min) / (n_points - 1)
    wealth_grid = [round(w_min + i * dw, 6) for i in range(n_points)]

    return {
        "seed": int(seed),
        "label": "SIMULATED",
        "r": r,
        "mu": mu,
        "sigma": sigma,
        "gamma": gamma,
        "rho": rho,
        "pi_max": pi_max,
        "w_min": w_min,
        "w_max": w_max,
        "n_points": n_points,
        "wealth_grid": wealth_grid,
    }
