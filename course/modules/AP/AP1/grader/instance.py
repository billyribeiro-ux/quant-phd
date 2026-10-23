"""Per-learner instances for the AP1 autograder (SDF recovery).

make_instance(seed) is deterministic, produces only valid instances, and changes
the answers (not just labels) from seed to seed: the number of states and
assets, the state probabilities, the true stochastic discount factor, the
payoffs, whether a riskless payoff is traded, and the lengths of the training
and test samples all vary with the seed. All data are SIMULATED.

The economy is a one-period market on S states with probabilities ``probs``.
A strictly positive SDF ``m_true`` prices N payoffs (the columns of
``payoffs``), so ``prices = payoffs.T @ (probs * m_true)`` and the market is
free of arbitrage. N is at most S - 2, so the market does not span every
state and the SDF is not unique. ``train`` and ``test`` are samples of states
drawn from ``probs``: each row is the payoff vector in the drawn state.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray


def _full_column_rank(x: NDArray[np.float64]) -> bool:
    return bool(np.linalg.matrix_rank(x) == x.shape[1])


def make_instance(seed: int) -> dict[str, Any]:
    rng = np.random.default_rng([11, 1, int(seed)])

    n_states = int(rng.integers(6, 15))
    n_assets = int(rng.integers(3, min(n_states - 2, 6) + 1))
    probs = rng.dirichlet(np.full(n_states, 3.0))
    m_true = np.exp(rng.normal(-0.02, float(rng.uniform(0.15, 0.5)), n_states))

    riskless = bool(rng.random() < 0.5)
    vols = rng.uniform(0.05, 0.6, n_assets)
    payoffs = 1.0 + rng.normal(0.0, 1.0, (n_states, n_assets)) * vols
    if riskless:
        payoffs[:, 0] = 1.0
    prices = payoffs.T @ (probs * m_true)
    while np.any(prices < 0.3):  # every payoff has a positive price, so it has a gross return
        payoffs = np.where(prices < 0.3, payoffs + 0.25, payoffs)
        prices = payoffs.T @ (probs * m_true)

    # Training and test samples of states; resampled until the training payoffs and a constant are linearly
    # independent, so the sample second-moment matrix and the covariance matrix of the risky payoffs are invertible.
    n_train = int(rng.integers(120, 361))
    n_test = int(rng.integers(60, 241))
    while True:
        train_states = rng.choice(n_states, size=n_train, p=probs)
        sample = payoffs[train_states]
        if _full_column_rank(np.column_stack([np.ones(n_train), sample[:, 1:] if riskless else sample])):
            break
    test_states = rng.choice(n_states, size=n_test, p=probs)

    return {
        "seed": int(seed),
        "probs": probs,
        "m_true": m_true,
        "payoffs": payoffs,
        "prices": prices,
        "riskless": riskless,
        "train": payoffs[train_states],
        "test": payoffs[test_states],
    }
