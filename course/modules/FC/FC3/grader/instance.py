"""Instance generator for the FC3 project: Fund-skill test.

SIMULATED fund returns and market factor data for evaluating fund skill
against the luck benchmark and bootstrap skill detection.
"""

from __future__ import annotations

import math
import random


def make_instance(seed: int) -> dict[str, object]:
    """Generate a simulated universe of fund returns and a market factor.

    SIMULATED: All factor returns and fund returns are generated using
    seeded pseudo-random draws. No real financial data is used.

    Parameters
    ----------
    seed : int
        Seed for the random number generator.

    Returns
    -------
    dict[str, object]
        A dictionary containing:
        - "returns": list[list[float]], N funds each with T monthly returns.
        - "factor": list[float], T monthly returns of the benchmark factor.
        - "planted_skill": list[int], sorted fund indices with true positive alpha.
        - "planted_alpha": list[float], monthly decimal alpha for all N funds.
    """
    rng = random.Random(seed)
    n_funds = 40
    n_months = 60

    # Market factor parameters (monthly decimal): mean 0.70%, stdev 4.5%
    mu_f = 0.007
    sigma_f = 0.045
    factor = [rng.gauss(mu_f, sigma_f) for _ in range(n_months)]

    mean_f = sum(factor) / n_months
    s_ff = sum((ft - mean_f) ** 2 for ft in factor)

    # Residual standard deviation: 2.0% monthly
    sigma_eps = 0.020
    # Expected standard error of alpha given factor variance
    expected_se = sigma_eps * math.sqrt(1.0 / n_months + (mean_f**2) / s_ff)

    # Randomly select 3 to 5 skilled funds
    num_skilled = rng.randint(3, 5)
    planted_skill = sorted(rng.sample(range(n_funds), num_skilled))

    # Assign planted alpha: >= 6.5 * expected_se (guarantees planted t >= 4 by construction)
    planted_alpha = [0.0] * n_funds
    for idx in planted_skill:
        planted_alpha[idx] = expected_se * (6.5 + 1.2 * rng.random())

    # Generate fund returns
    returns: list[list[float]] = []
    for i in range(n_funds):
        beta = 0.8 + 0.4 * rng.random()
        alpha = planted_alpha[i]
        r_i = [alpha + beta * factor[t] + rng.gauss(0.0, sigma_eps) for t in range(n_months)]
        returns.append(r_i)

    return {
        "returns": returns,
        "factor": factor,
        "planted_skill": planted_skill,
        "planted_alpha": planted_alpha,
    }
