"""x_star_weights skips the redundant-payoff check when T equals N (square payoffs), so linearly dependent payoffs return garbage weights.

Verifier mutant of course/modules/AP/AP1/grader/reference.py at 7216a6c: one realistic
student error, otherwise identical to the reference.

Conventions (the project specification, project.html §3):

* A sample of payoffs is a (T, N) array: row t is the payoff vector of the N assets in observed state t.
  Sample moments are equally weighted averages over the T rows (divide by T, never by T - 1), because the
  sample is treated as a market of T equally likely states, and only then do the sample identities hold
  exactly.
* Prices are a length-N vector, in the same units as the payoffs.
* A pricing error is E[m x] - p: positive when the SDF assigns the payoff more value than its price.
* x* = x' b with b = E[x x']^{-1} p is the unique SDF in the payoff space (Lesson 4, Theorem 3.2). The minimum-variance
  SDF with mean v is m_v = v + (x - E[x])' beta with beta = Cov(x)^{-1} (p - v E[x]) (Lesson 5, Theorem 2.1).

Every function is pure: it validates its inputs, raises ValueError, and
never prints, warns or mutates its arguments.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray

_RANK_TOL = 1e-10  # relative singular-value tolerance for linear independence


def _matrix(values: ArrayLike, name: str) -> NDArray[np.float64]:
    x = np.array(values, dtype=np.float64)  # a copy: callers' arrays are never touched
    if x.ndim != 2:
        raise ValueError(f"{name} must be two-dimensional (observations x assets)")
    if x.shape[0] < 1 or x.shape[1] < 1:
        raise ValueError(f"{name} needs at least one observation and one asset")
    if not np.all(np.isfinite(x)):
        raise ValueError(f"{name} must be finite")
    return x


def _vector(values: ArrayLike, name: str, length: int | None = None) -> NDArray[np.float64]:
    v = np.array(values, dtype=np.float64)
    if v.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    if length is not None and v.size != length:
        raise ValueError(f"{name} must have one entry per asset ({length}), not {v.size}")
    if not np.all(np.isfinite(v)):
        raise ValueError(f"{name} must be finite")
    return v


def _full_rank(x: NDArray[np.float64], name: str) -> None:
    if x.shape[0] < x.shape[1]:
        raise ValueError(f"{name} needs at least as many observations as assets")
    if x.shape[0] == x.shape[1]:
        return
    s = np.linalg.svd(x, compute_uv=False)
    if s[-1] <= _RANK_TOL * s[0]:
        raise ValueError(f"{name} must have linearly independent columns (no redundant payoff)")


def second_moment_matrix(payoffs: ArrayLike) -> NDArray[np.float64]:
    """Sample second-moment matrix E_T[x x'] = X'X / T of a (T, N) payoff sample."""
    x = _matrix(payoffs, "payoffs")
    return np.asarray(x.T @ x / x.shape[0], dtype=np.float64)


def x_star_weights(payoffs: ArrayLike, prices: ArrayLike) -> NDArray[np.float64]:
    """Weights b of the sample x* = x' b, with b = E_T[x x']^{-1} p."""
    x = _matrix(payoffs, "payoffs")
    p = _vector(prices, "prices", x.shape[1])
    _full_rank(x, "payoffs")
    return np.asarray(np.linalg.solve(x.T @ x / x.shape[0], p), dtype=np.float64)


def sdf_values(payoffs: ArrayLike, weights: ArrayLike) -> NDArray[np.float64]:
    """Values x' b of a linear SDF in each observed state: a length-T vector."""
    x = _matrix(payoffs, "payoffs")
    b = _vector(weights, "weights", x.shape[1])
    return np.asarray(x @ b, dtype=np.float64)


def pricing_errors(payoffs: ArrayLike, prices: ArrayLike, sdf: ArrayLike) -> NDArray[np.float64]:
    """Sample pricing errors E_T[m x] - p of the SDF values `sdf` (one per row of `payoffs`)."""
    x = _matrix(payoffs, "payoffs")
    p = _vector(prices, "prices", x.shape[1])
    m = _vector(sdf, "sdf")
    if m.size != x.shape[0]:
        raise ValueError(f"sdf must have one value per observation ({x.shape[0]}), not {m.size}")
    return np.asarray(x.T @ m / x.shape[0] - p, dtype=np.float64)


def population_x_star(probs: ArrayLike, payoffs: ArrayLike, prices: ArrayLike) -> NDArray[np.float64]:
    """Values of x* = x' E[x x']^{-1} p in each of S states with probabilities `probs` (payoffs is (S, N))."""
    pi = _vector(probs, "probs")
    x = _matrix(payoffs, "payoffs")
    if pi.size != x.shape[0]:
        raise ValueError(f"probs must have one entry per state ({x.shape[0]}), not {pi.size}")
    if np.any(pi <= 0.0):
        raise ValueError("probs must be strictly positive")
    if abs(float(pi.sum()) - 1.0) > 1e-9:
        raise ValueError("probs must sum to one")
    p = _vector(prices, "prices", x.shape[1])
    _full_rank(x, "payoffs")
    b = np.linalg.solve(x.T @ (pi[:, None] * x), p)
    return np.asarray(x @ b, dtype=np.float64)


def _centred(x: NDArray[np.float64]) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Sample mean and covariance (divide by T); raise if the covariance matrix is singular."""
    if x.shape[0] <= x.shape[1]:
        raise ValueError("payoffs need more observations than assets for a covariance matrix")
    mu = x.mean(axis=0)
    c = x - mu
    s = np.linalg.svd(c, compute_uv=False)
    if s[0] == 0.0 or s[-1] <= _RANK_TOL * max(s[0], float(np.abs(x).max())):
        raise ValueError(
            "the payoff covariance matrix is singular: a riskless (constant) payoff or a redundant combination "
            "pins E[m]; use x_star_weights instead"
        )
    return mu, np.asarray(c.T @ c / x.shape[0], dtype=np.float64)


def min_variance_sdf(payoffs: ArrayLike, prices: ArrayLike, mean: float) -> tuple[float, NDArray[np.float64]]:
    """Minimum-variance SDF with E_T[m] = mean that prices the sample: m = a + x' b; returns (a, b)."""
    x = _matrix(payoffs, "payoffs")
    p = _vector(prices, "prices", x.shape[1])
    v = float(mean)
    if not math.isfinite(v):
        raise ValueError("mean must be finite")
    mu, cov = _centred(x)
    beta = np.linalg.solve(cov, p - v * mu)
    return v - float(mu @ beta), np.asarray(beta, dtype=np.float64)


def min_sdf_std(payoffs: ArrayLike, prices: ArrayLike, mean: float) -> float:
    """Smallest standard deviation (divide by T) of any SDF with mean `mean` that prices the sample."""
    x = _matrix(payoffs, "payoffs")
    p = _vector(prices, "prices", x.shape[1])
    v = float(mean)
    if not math.isfinite(v):
        raise ValueError("mean must be finite")
    mu, cov = _centred(x)
    g = p - v * mu
    return math.sqrt(max(float(g @ np.linalg.solve(cov, g)), 0.0))


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
    tr = _matrix(train, "train")
    te = _matrix(test, "test")
    if te.shape[1] != tr.shape[1]:
        raise ValueError("train and test must have the same assets (columns)")
    p = _vector(prices, "prices", tr.shape[1])
    b = x_star_weights(tr, p)
    m_train = tr @ b
    m_test = te @ b
    in_err = tr.T @ m_train / tr.shape[0] - p
    out_err = te.T @ m_test / te.shape[0] - p
    return SDFRecovery(
        weights=np.asarray(b, dtype=np.float64),
        in_sample_errors=np.asarray(in_err, dtype=np.float64),
        out_of_sample_errors=np.asarray(out_err, dtype=np.float64),
        out_of_sample_rms=float(np.sqrt(np.mean(out_err**2))),
        train_mean=float(m_train.mean()),
        train_std=float(m_train.std()),
        test_share_negative=float(np.mean(m_test < 0.0)),
    )
