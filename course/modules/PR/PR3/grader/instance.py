"""Instance generator for PR3 Growth-Optimal Sizing autograded project.

SIMULATED: generated synthetic market and betting parameters.
"""

from __future__ import annotations

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate deterministic inputs for sizing policy under parameter uncertainty.

    Parameters
    ----------
    seed : int
        Pseudorandom seed determining market parameters.

    Returns
    -------
    dict[str, Any]
        Dictionary with keys:
        - seed: int
        - p: float (win rate)
        - b: float (odds / payoff ratio)
        - mu: float (asset expected return)
        - r: float (risk-free rate)
        - sigma: float (annual volatility)
        - t_obs: int (estimation sample size)
        - max_drawdown: float (maximum acceptable drawdown fraction D_max)
        - max_drawdown_prob: float (maximum acceptable probability of hitting D_max)
        - mu_vec: list[float] (3-asset expected return vector)
        - cov_mat: list[list[float]] (3x3 positive-definite covariance matrix)
    """
    rng = random.Random(seed)

    # Discrete bet parameters
    p = round(0.52 + 0.12 * rng.random(), 4)
    b = round(0.80 + 1.20 * rng.random(), 4)

    # Continuous single-asset parameters
    r = round(0.02 + 0.03 * rng.random(), 4)
    excess_mu = round(0.04 + 0.08 * rng.random(), 4)
    mu = round(r + excess_mu, 4)
    sigma = round(0.14 + 0.14 * rng.random(), 4)

    # Estimation parameters
    t_obs = 30 + (seed * 7) % 91  # between 30 and 120 observations
    max_drawdown = round(0.20 + 0.15 * rng.random(), 4)
    max_drawdown_prob = round(0.05 + 0.08 * rng.random(), 4)

    # 3-asset market parameters for multivariate GOP
    mu_vec = [round(r + 0.03 + 0.06 * rng.random(), 4) for _ in range(3)]
    vols = [round(0.15 + 0.10 * rng.random(), 4) for _ in range(3)]
    corr_12 = round(0.10 + 0.40 * rng.random(), 4)
    corr_13 = round(0.05 + 0.35 * rng.random(), 4)
    corr_23 = round(0.10 + 0.45 * rng.random(), 4)

    cov_mat = [
        [round(vols[0] ** 2, 6), round(corr_12 * vols[0] * vols[1], 6), round(corr_13 * vols[0] * vols[2], 6)],
        [round(corr_12 * vols[0] * vols[1], 6), round(vols[1] ** 2, 6), round(corr_23 * vols[1] * vols[2], 6)],
        [round(corr_13 * vols[0] * vols[2], 6), round(corr_23 * vols[1] * vols[2], 6), round(vols[2] ** 2, 6)],
    ]

    return {
        "seed": seed,
        "p": p,
        "b": b,
        "mu": mu,
        "r": r,
        "sigma": sigma,
        "t_obs": t_obs,
        "max_drawdown": max_drawdown,
        "max_drawdown_prob": max_drawdown_prob,
        "mu_vec": mu_vec,
        "cov_mat": cov_mat,
    }
