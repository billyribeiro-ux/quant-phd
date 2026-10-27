# MUTANT cutoff-inflated-2pct: cutoff inflated by 2 percent, so the fixed-N size falls to about 0.0465 (level too low)
"""Monte Carlo spot check of the Koning and van Meer Theorem 1 claims as S7 Lesson 1 uses them.

phi is the fixed-N test (N = 20, one-sided, level 0.05) of a simple null, N(0, 1) iid, and
phi_n = E_P[phi | F_n]. Claim 3: phi_N = phi. Martingale: E_P[phi_n] = E_P[phi] for every n.
Claim 1: E_P[phi_tau] <= 0.05 for stopping times tau. The seed is fixed, so the run is deterministic;
the tolerance is six standard errors of a Bernoulli(0.05) mean over 400,000 paths (6 x 0.000345).
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from scipy import stats  # type: ignore[import-untyped]

N = 20
REPS = 400_000
LEVEL = 0.05
TOLERANCE = 6 * (LEVEL * (1 - LEVEL) / REPS) ** 0.5


def _paths() -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    rng = np.random.default_rng(20261021)
    cumulative = np.cumsum(rng.standard_normal((REPS, N)), axis=1)
    cutoff = 1.02 * stats.norm.ppf(1 - LEVEL) * np.sqrt(N)
    reject = (cumulative[:, -1] > cutoff).astype(float)
    # phi_n = P(S_N > c | F_n) = 1 - Phi((c - S_n) / sqrt(N - n)) for n < N, and phi itself at n = N
    phi = np.empty_like(cumulative)
    for j in range(N - 1):
        phi[:, j] = stats.norm.sf((cutoff - cumulative[:, j]) / np.sqrt(N - (j + 1)))
    phi[:, -1] = reject
    return phi, reject


def test_the_last_conditional_expectation_is_the_test_itself() -> None:
    phi, reject = _paths()
    assert float(np.max(np.abs(phi[:, -1] - reject))) == 0.0


def test_the_fixed_n_test_has_its_level_and_phi_n_is_a_martingale() -> None:
    phi, reject = _paths()
    assert abs(float(reject.mean()) - LEVEL) < TOLERANCE
    means = phi.mean(axis=0)
    assert float(means.max()) < LEVEL + TOLERANCE
    assert float(means.min()) > LEVEL - TOLERANCE


def test_stopping_at_a_look_never_pushes_the_size_above_the_level() -> None:
    phi, _ = _paths()
    for threshold in (0.5, 0.2, 0.05):
        hit = phi >= threshold
        first = np.where(hit.any(axis=1), hit.argmax(axis=1), N - 1)
        stopped = phi[np.arange(REPS), first]
        assert float(stopped.mean()) <= LEVEL + TOLERANCE
