"""Instance generator for PR4 autograded project (Atlas A12).

SIMULATED: generates synthetic heavy-tailed asset return and loss histories,
stress shock vectors, and backtest exception sequences for seed-specific
risk measurement validation.
"""

from __future__ import annotations

import math
import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic risk measurement instance for Atlas A12.

    Parameters
    ----------
    seed : int
        Seed for the pseudorandom number generator.

    Returns
    -------
    dict[str, Any]
        Dictionary containing asset names, loss series, portfolio weights,
        portfolio dollar value, stress scenarios, backtest hit sequences,
        and threshold parameters.
    """
    rng = random.Random(seed)
    n_assets = 4 + (seed % 3)  # 4, 5, or 6 assets
    t_obs = 600  # 600 daily observation periods (~2.4 years)

    names = [f"Asset_{chr(65 + i)}" for i in range(n_assets)]

    # Generate heavy-tailed univariate losses via Student-t(nu=4) mixture
    # L = -R where R is return. Positive L denotes portfolio loss.
    losses: list[float] = []
    drift = 0.0003 + (seed % 5) * 0.0001
    vol = 0.014 + (seed % 4) * 0.002

    for _ in range(t_obs):
        z = rng.gauss(0.0, vol)
        # Chi-squared with 4 degrees of freedom
        v = sum(rng.gauss(0.0, 1.0) ** 2 for _ in range(4))
        scale = math.sqrt(v / 4.0)
        t_val = -drift + (z / (scale if scale > 1e-4 else 1.0))
        # Loss L = -Return
        loss = round(-t_val, 6)
        losses.append(loss)

    # Portfolio capital weights summing strictly to 1.0
    raw_w = [1.0 + rng.random() for _ in range(n_assets)]
    tot_w = sum(raw_w)
    weights = [round(w / tot_w, 6) for w in raw_w]
    weights[0] += round(1.0 - sum(weights), 6)

    # Portfolio initial base equity
    portfolio_value = round(10_000_000.0 + (seed % 50) * 100_000.0, 2)

    # Asset stress shock scenario (fractional price changes, e.g. -20% to +10%)
    shocks = [round(-0.25 + 0.35 * rng.random(), 4) for _ in range(n_assets)]

    # 90th percentile empirical threshold for Peaks-Over-Threshold (POT) EVT
    sorted_losses = sorted(losses)
    threshold = round(sorted_losses[int(0.88 * t_obs)], 6)

    # Clean i.i.d. backtest violation sequence (Bernoulli p = 0.01 across 250 days)
    # Expected number of exceptions is ~2.5, well within Kupiec non-rejection zone
    hits_iid = [1 if rng.random() < 0.012 else 0 for _ in range(250)]

    # Clustered backtest violation sequence: consecutive violations during a shock regime
    hits_clustered = [0] * 250
    cluster_start = 80 + (seed % 40)
    for idx in range(cluster_start, cluster_start + 4):
        hits_clustered[idx] = 1

    # Positive-definite 2x2 correlation matrix for copula tail evaluation
    rho = round(0.35 + 0.45 * rng.random(), 4)
    corr_matrix = [[1.0, rho], [rho, 1.0]]

    return {
        "seed": seed,
        "n_assets": n_assets,
        "t_obs": t_obs,
        "names": names,
        "losses": losses,
        "weights": weights,
        "portfolio_value": portfolio_value,
        "stress_shocks": shocks,
        "threshold": threshold,
        "alpha": 0.99,
        "hits_iid": hits_iid,
        "hits_clustered": hits_clustered,
        "corr_matrix": corr_matrix,
    }
