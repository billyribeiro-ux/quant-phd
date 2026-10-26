"""Starter for the AP1 project: sdf_recovery.py.

Implement every function to the specification on the project page (§3), then run the autograder there,
or locally with the browser's flags:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Conventions: a payoff sample is a (T, N) array whose row t is the payoff vector in observed state t;
sample moments divide by T; a pricing error is E[m x] - p. Every function must validate its inputs and
raise ValueError (a message saying what was wrong helps you debug); none may print, warn or mutate its
arguments. Use NumPy and the standard library only. The dataclass is complete.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray


def second_moment_matrix(payoffs: ArrayLike) -> NDArray[np.float64]:
    """Sample second-moment matrix E_T[x x'] = X'X / T of a (T, N) payoff sample."""
    raise NotImplementedError("second_moment_matrix")


def x_star_weights(payoffs: ArrayLike, prices: ArrayLike) -> NDArray[np.float64]:
    """Weights b of the sample x* = x' b, with b = E_T[x x']^{-1} p. Redundant payoffs raise ValueError."""
    raise NotImplementedError("x_star_weights")


def sdf_values(payoffs: ArrayLike, weights: ArrayLike) -> NDArray[np.float64]:
    """Values x' b of a linear SDF in each observed state: a length-T vector."""
    raise NotImplementedError("sdf_values")


def pricing_errors(payoffs: ArrayLike, prices: ArrayLike, sdf: ArrayLike) -> NDArray[np.float64]:
    """Sample pricing errors E_T[m x] - p of the SDF values `sdf` (one per row of `payoffs`)."""
    raise NotImplementedError("pricing_errors")


def population_x_star(probs: ArrayLike, payoffs: ArrayLike, prices: ArrayLike) -> NDArray[np.float64]:
    """Values of x* = x' E[x x']^{-1} p in each of S states with probabilities `probs` (payoffs is (S, N))."""
    raise NotImplementedError("population_x_star")


def min_variance_sdf(payoffs: ArrayLike, prices: ArrayLike, mean: float) -> tuple[float, NDArray[np.float64]]:
    """Minimum-variance SDF with E_T[m] = mean that prices the sample: m = a + x' b; returns (a, b).

    A singular payoff covariance matrix (for example a riskless payoff) raises ValueError.
    """
    raise NotImplementedError("min_variance_sdf")


def min_sdf_std(payoffs: ArrayLike, prices: ArrayLike, mean: float) -> float:
    """Smallest standard deviation (divide by T) of any SDF with mean `mean` that prices the sample."""
    raise NotImplementedError("min_sdf_std")


@dataclass(frozen=True)
class SDFRecovery:
    """x* estimated on a training sample and evaluated on a test sample."""

    weights: NDArray[np.float64]  # b, estimated on the training sample
    in_sample_errors: NDArray[np.float64]  # E_train[x* x] - p (zero up to rounding)
    out_of_sample_errors: NDArray[np.float64]  # E_test[x* x] - p, with the training weights
    out_of_sample_rms: float  # root mean square of out_of_sample_errors
    train_mean: float  # E_train[x*]
    train_std: float  # standard deviation of x* on the training sample (divide by T)
    test_share_negative: float  # share of test observations with x* < 0


def recover_sdf(train: ArrayLike, test: ArrayLike, prices: ArrayLike) -> SDFRecovery:
    """Estimate x* on `train`, check that it prices the training sample, and measure its errors on `test`."""
    raise NotImplementedError("recover_sdf")
