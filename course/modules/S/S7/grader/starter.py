"""Starter for Atlas A8: atlas/integrity.py.

Implement every function so that it matches atlas/A8.contract.md exactly, then
run the autograder on the S7 project page, or locally with the browser's flags:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

The dataclasses are complete.
Every function must validate its inputs and raise ValueError naming the
violated condition; none may print, warn or mutate its arguments. A series
has zero variance when all its values are equal (test that, not std == 0),
and every statistic must be unchanged when the returns are multiplied by a
power of two, at any magnitude (the contract's Scale row).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import numpy as np
from numpy.typing import ArrayLike, NDArray

EULER_MASCHERONI = 0.5772156649015329


def sharpe_ratio(returns: ArrayLike) -> float:
    """Per-period Sharpe ratio: mean / std(ddof=1). Needs >= 2 finite observations, not all equal."""
    raise NotImplementedError("sharpe_ratio")


def sample_skewness(returns: ArrayLike) -> float:
    """Moment estimator m3 / m2**1.5 with m_k = mean((r - mean(r))**k). Zero variance raises ValueError."""
    raise NotImplementedError("sample_skewness")


def sample_kurtosis(returns: ArrayLike) -> float:
    """Moment estimator m4 / m2**2 (not excess: 3 for a normal). Zero variance raises ValueError."""
    raise NotImplementedError("sample_kurtosis")


def sharpe_ratio_std(sharpe: float, n_obs: int, skewness: float, kurtosis: float) -> float:
    """sqrt((1 - skewness*sharpe + (kurtosis - 1)/4 * sharpe**2) / (n_obs - 1))."""
    raise NotImplementedError("sharpe_ratio_std")


def probabilistic_sharpe_ratio(returns: ArrayLike, sr_benchmark: float = 0.0) -> float:
    """Phi((SR - sr_benchmark) / sharpe_ratio_std(SR, T, skew, kurt)), all estimated from returns."""
    raise NotImplementedError("probabilistic_sharpe_ratio")


def expected_max_sharpe(n_trials: int, sr_variance: float, sr_mean: float = 0.0) -> float:
    """sr_mean + sqrt(var) * ((1-g) Phi^-1(1-1/N) + g Phi^-1(1-1/(N e))); N == 1 returns sr_mean."""
    raise NotImplementedError("expected_max_sharpe")


def deflated_sharpe_ratio(returns: ArrayLike, trial_sharpes: ArrayLike, n_trials: int | None = None) -> float:
    """PSR of returns at SR0 = expected_max_sharpe(N, var(trial_sharpes, ddof=1), 0)."""
    raise NotImplementedError("deflated_sharpe_ratio")


def benjamini_hochberg(pvalues: ArrayLike, q: float) -> NDArray[np.bool_]:
    """Step-up FDR procedure; boolean mask aligned with the input order."""
    raise NotImplementedError("benjamini_hochberg")


def stationary_bootstrap_indices(n_obs: int, mean_block: float, rng: np.random.Generator) -> NDArray[np.intp]:
    """One stationary-bootstrap resample of the time indices 0..n_obs-1 (geometric blocks, wrap-around)."""
    raise NotImplementedError("stationary_bootstrap_indices")


def stepdown_rejections(t_obs: ArrayLike, t_boot: ArrayLike, alpha: float) -> NDArray[np.bool_]:
    """Romano-Wolf step-down from observed (K,) and centred bootstrap (B, K) statistics."""
    raise NotImplementedError("stepdown_rejections")


def romano_wolf(
    differentials: ArrayLike,
    alpha: float = 0.05,
    n_boot: int = 1000,
    mean_block: float = 10.0,
    seed: int = 0,
) -> NDArray[np.bool_]:
    """Studentized StepM with the stationary bootstrap, resampling whole periods jointly.

    Draw idx_b = stationary_bootstrap_indices(T, mean_block, rng) for b = 1, ..., n_boot in order, all from the
    single rng = np.random.default_rng(seed).
    """
    raise NotImplementedError("romano_wolf")


@dataclass(frozen=True)
class PBOResult:
    pbo: float
    logits: NDArray[np.float64]
    n_combinations: int


def probability_of_backtest_overfitting(performance: ArrayLike, n_blocks: int = 16) -> PBOResult:
    """CSCV estimate of the probability of backtest overfitting (see the contract for every convention)."""
    raise NotImplementedError("probability_of_backtest_overfitting")


class BacktestLike(Protocol):
    trial_returns: ArrayLike
    selected: int
    periods_per_year: int


@dataclass(frozen=True)
class TrialSet:
    returns: NDArray[np.float64]
    selected: int
    periods_per_year: int

    def __post_init__(self) -> None:
        r = np.asarray(self.returns, dtype=np.float64)
        if r.ndim != 2 or r.shape[0] < 2 or r.shape[1] < 2 or not np.all(np.isfinite(r)):
            raise ValueError("returns must be a finite (T, N) matrix with T >= 2 and N >= 2")
        if not (0 <= self.selected < r.shape[1]):
            raise ValueError("selected must index a column of returns")
        if self.periods_per_year < 1:
            raise ValueError("periods_per_year must be positive")
        object.__setattr__(self, "returns", r)

    @classmethod
    def from_backtest(cls, result: BacktestLike) -> TrialSet:
        return cls(
            np.asarray(result.trial_returns, dtype=np.float64), int(result.selected), int(result.periods_per_year)
        )


@dataclass(frozen=True)
class IntegrityReport:
    n_trials: int
    selected_sharpe: float
    selected_sharpe_annualized: float
    psr: float
    expected_max_sharpe: float
    dsr: float
    pbo: float
    bh_rejections: NDArray[np.bool_]
    romano_wolf_rejections: NDArray[np.bool_]


def integrity_report(
    trials: TrialSet,
    *,
    alpha: float = 0.05,
    q: float = 0.05,
    n_blocks: int = 16,
    n_boot: int = 1000,
    mean_block: float = 10.0,
    seed: int = 0,
) -> IntegrityReport:
    """Every A8 statistic for the selected strategy and the trials it was chosen from."""
    raise NotImplementedError("integrity_report")
