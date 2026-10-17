"""Step-down critical value uses the floor((1-alpha)B)-th order statistic instead of the ceil((1-alpha)B)-th.

Verifier mutant of course/modules/S/S7/grader/reference.py (S7 / Atlas A8): one realistic
student error, otherwise identical to the reference.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from statistics import NormalDist
from typing import Protocol

import numpy as np
from numpy.typing import ArrayLike, NDArray

EULER_MASCHERONI = 0.5772156649015329
_STANDARD_NORMAL = NormalDist()


# ---------------------------------------------------------------- validation


def _series(returns: ArrayLike, name: str = "returns") -> NDArray[np.float64]:
    x = np.asarray(returns, dtype=np.float64)
    if x.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    if x.size < 2:
        raise ValueError(f"{name} needs at least 2 observations")
    if not np.all(np.isfinite(x)):
        raise ValueError(f"{name} must be finite")
    return x


def _matrix(values: ArrayLike, name: str) -> NDArray[np.float64]:
    x = np.asarray(values, dtype=np.float64)
    if x.ndim != 2:
        raise ValueError(f"{name} must be two-dimensional (periods x strategies)")
    if x.shape[0] < 2 or x.shape[1] < 1:
        raise ValueError(f"{name} needs at least 2 periods and 1 strategy")
    if not np.all(np.isfinite(x)):
        raise ValueError(f"{name} must be finite")
    return x


def _level(value: float, name: str) -> float:
    if not (0.0 < value < 1.0):
        raise ValueError(f"{name} must lie strictly between 0 and 1")
    return float(value)


# ---------------------------------------------------------------- Sharpe ratio and its distribution


def sharpe_ratio(returns: ArrayLike) -> float:
    """Per-period Sharpe ratio mean / std(ddof=1) of an excess-return series."""
    x = _series(returns)
    sd = float(np.std(x, ddof=1))
    if sd == 0.0:
        raise ValueError("returns have zero sample variance")
    return float(np.mean(x)) / sd


def _central_moment(x: NDArray[np.float64], k: int) -> float:
    return float(np.mean((x - np.mean(x)) ** k))


def sample_skewness(returns: ArrayLike) -> float:
    """Moment estimator m3 / m2**1.5."""
    x = _series(returns)
    m2 = _central_moment(x, 2)
    if m2 == 0.0:
        raise ValueError("returns have zero sample variance")
    return _central_moment(x, 3) / math.pow(m2, 1.5)


def sample_kurtosis(returns: ArrayLike) -> float:
    """Moment estimator m4 / m2**2 (not excess; 3 under normality)."""
    x = _series(returns)
    m2 = _central_moment(x, 2)
    if m2 == 0.0:
        raise ValueError("returns have zero sample variance")
    return _central_moment(x, 4) / m2**2


def sharpe_ratio_std(sharpe: float, n_obs: int, skewness: float, kurtosis: float) -> float:
    """Standard error of the estimated Sharpe ratio under skewness and kurtosis (iid returns)."""
    if n_obs < 2:
        raise ValueError("n_obs must be at least 2")
    if not all(math.isfinite(v) for v in (sharpe, skewness, kurtosis)):
        raise ValueError("sharpe, skewness and kurtosis must be finite")
    bracket = 1.0 - skewness * sharpe + (kurtosis - 1.0) / 4.0 * sharpe**2
    if bracket <= 0.0:
        raise ValueError("the variance bracket 1 - skew*SR + (kurt-1)/4*SR^2 must be positive")
    return math.sqrt(bracket / (n_obs - 1))


def probabilistic_sharpe_ratio(returns: ArrayLike, sr_benchmark: float = 0.0) -> float:
    """Probability that the true Sharpe ratio exceeds sr_benchmark, given skewness and kurtosis."""
    x = _series(returns)
    if not math.isfinite(sr_benchmark):
        raise ValueError("sr_benchmark must be finite")
    sr = sharpe_ratio(x)
    se = sharpe_ratio_std(sr, x.size, sample_skewness(x), sample_kurtosis(x))
    return _STANDARD_NORMAL.cdf((sr - sr_benchmark) / se)


def expected_max_sharpe(n_trials: int, sr_variance: float, sr_mean: float = 0.0) -> float:
    """Approximate expected maximum of n_trials independent normal Sharpe-ratio estimates."""
    if int(n_trials) != n_trials or n_trials < 1:
        raise ValueError("n_trials must be a positive integer")
    if not math.isfinite(sr_variance) or sr_variance < 0.0:
        raise ValueError("sr_variance must be finite and non-negative")
    if not math.isfinite(sr_mean):
        raise ValueError("sr_mean must be finite")
    if n_trials == 1:
        return float(sr_mean)
    n = float(n_trials)
    z = (1.0 - EULER_MASCHERONI) * _STANDARD_NORMAL.inv_cdf(1.0 - 1.0 / n) + EULER_MASCHERONI * (
        _STANDARD_NORMAL.inv_cdf(1.0 - 1.0 / (n * math.e))
    )
    return float(sr_mean) + math.sqrt(sr_variance) * z


def deflated_sharpe_ratio(returns: ArrayLike, trial_sharpes: ArrayLike, n_trials: int | None = None) -> float:
    """PSR of `returns` against the expected maximum Sharpe ratio of the trials under the null."""
    trials = _series(trial_sharpes, "trial_sharpes")
    n = trials.size if n_trials is None else n_trials
    sr0 = expected_max_sharpe(n, float(np.var(trials, ddof=1)), 0.0)
    return probabilistic_sharpe_ratio(returns, sr0)


# ---------------------------------------------------------------- false discovery rate


def benjamini_hochberg(pvalues: ArrayLike, q: float) -> NDArray[np.bool_]:
    """Benjamini-Hochberg step-up procedure at FDR level q; mask aligned with the input order."""
    q = _level(q, "q")
    p = np.asarray(pvalues, dtype=np.float64)
    if p.ndim != 1:
        raise ValueError("pvalues must be one-dimensional")
    if p.size == 0:
        return np.zeros(0, dtype=bool)
    if not np.all(np.isfinite(p)) or np.any(p < 0.0) or np.any(p > 1.0):
        raise ValueError("pvalues must lie in [0, 1]")
    m = p.size
    order = np.argsort(p, kind="stable")
    below = np.nonzero(p[order] <= q * np.arange(1, m + 1) / m)[0]
    reject = np.zeros(m, dtype=bool)
    if below.size:
        reject[order[: below[-1] + 1]] = True
    return reject


# ---------------------------------------------------------------- bootstrap and step-down


def stationary_bootstrap_indices(n_obs: int, mean_block: float, rng: np.random.Generator) -> NDArray[np.intp]:
    """One stationary-bootstrap resample of the time indices 0..n_obs-1."""
    if int(n_obs) != n_obs or n_obs < 1:
        raise ValueError("n_obs must be a positive integer")
    if not math.isfinite(mean_block) or mean_block < 1.0:
        raise ValueError("mean_block must be at least 1")
    n = int(n_obs)
    starts = rng.integers(0, n, size=n)
    new_block = rng.random(n) < 1.0 / mean_block
    new_block[0] = True
    # Vectorized form of: idx[t] = starts[t] if new_block[t] else (idx[t-1] + 1) mod n.
    positions = np.arange(n)
    block_start = np.maximum.accumulate(np.where(new_block, positions, 0))
    indices: NDArray[np.intp] = ((starts[block_start] + positions - block_start) % n).astype(np.intp)
    return indices


def stepdown_rejections(t_obs: ArrayLike, t_boot: ArrayLike, alpha: float) -> NDArray[np.bool_]:
    """Romano-Wolf step-down rejections from observed and centred bootstrap statistics."""
    alpha = _level(alpha, "alpha")
    t = np.asarray(t_obs, dtype=np.float64)
    boot = np.asarray(t_boot, dtype=np.float64)
    if t.ndim != 1 or boot.ndim != 2 or boot.shape[1] != t.size:
        raise ValueError("t_obs must be (K,) and t_boot (B, K)")
    if boot.shape[0] < 1:
        raise ValueError("t_boot needs at least one bootstrap draw")
    if not (np.all(np.isfinite(t)) and np.all(np.isfinite(boot))):
        raise ValueError("statistics must be finite")
    b = boot.shape[0]
    rank = max(1, int((1.0 - alpha) * b))
    rejected = np.zeros(t.size, dtype=bool)
    while not rejected.all():
        active = ~rejected
        maxima = np.sort(boot[:, active].max(axis=1))
        critical = maxima[rank - 1]
        new = active & (t > critical)
        if not new.any():
            break
        rejected |= new
    return rejected


def romano_wolf(
    differentials: ArrayLike,
    alpha: float = 0.05,
    n_boot: int = 1000,
    mean_block: float = 10.0,
    seed: int = 0,
) -> NDArray[np.bool_]:
    """Studentized Romano-Wolf StepM with the stationary bootstrap; H0_k: E[d_k] <= 0."""
    d = _matrix(differentials, "differentials")
    if int(n_boot) != n_boot or n_boot < 1:
        raise ValueError("n_boot must be a positive integer")
    n_obs = d.shape[0]
    sd = np.std(d, axis=0, ddof=1)
    if np.any(sd == 0.0):
        raise ValueError("every column of differentials needs positive sample variance")
    means = d.mean(axis=0)
    t_obs = means / (sd / math.sqrt(n_obs))
    rng = np.random.default_rng(seed)
    t_boot = np.empty((int(n_boot), d.shape[1]))
    for b in range(int(n_boot)):
        sample = d[stationary_bootstrap_indices(n_obs, mean_block, rng)]
        sd_b = np.std(sample, axis=0, ddof=1)
        sd_b[sd_b == 0.0] = np.finfo(np.float64).tiny
        t_boot[b] = (sample.mean(axis=0) - means) / (sd_b / math.sqrt(n_obs))
    return stepdown_rejections(t_obs, t_boot, alpha)


# ---------------------------------------------------------------- probability of backtest overfitting


@dataclass(frozen=True)
class PBOResult:
    pbo: float
    logits: NDArray[np.float64]
    n_combinations: int


def _sharpe_columns(block: NDArray[np.float64]) -> NDArray[np.float64]:
    mean = block.mean(axis=0)
    sd = block.std(axis=0, ddof=1)
    out: NDArray[np.float64] = np.empty(mean.shape, dtype=np.float64)
    for j in range(mean.size):
        if sd[j] > 0.0:
            out[j] = mean[j] / sd[j]
        elif mean[j] == 0.0:
            out[j] = 0.0
        else:
            out[j] = math.copysign(math.inf, mean[j])
    return out


def probability_of_backtest_overfitting(performance: ArrayLike, n_blocks: int = 16) -> PBOResult:
    """Combinatorially symmetric cross-validation estimate of the PBO."""
    m = _matrix(performance, "performance")
    n_obs, n_strategies = m.shape
    if n_strategies < 2:
        raise ValueError("performance needs at least 2 strategies")
    if int(n_blocks) != n_blocks or n_blocks < 2 or n_blocks % 2:
        raise ValueError("n_blocks must be an even integer >= 2")
    if n_blocks > n_obs:
        raise ValueError("n_blocks cannot exceed the number of periods")
    s = int(n_blocks)
    m = m[n_obs % s :]
    blocks = np.split(m, s)
    logits = []
    for combo in itertools.combinations(range(s), s // 2):
        chosen = set(combo)
        train = np.vstack([blocks[i] for i in range(s) if i in chosen])
        test = np.vstack([blocks[i] for i in range(s) if i not in chosen])
        best = int(np.argmax(_sharpe_columns(train)))
        oos = _sharpe_columns(test)
        lower = int(np.sum(oos < oos[best]))
        ties = int(np.sum(oos == oos[best])) - 1
        rank = 1.0 + lower + 0.5 * ties
        omega = rank / (n_strategies + 1.0)
        logits.append(math.log(omega / (1.0 - omega)))
    values = np.asarray(logits, dtype=np.float64)
    return PBOResult(pbo=float(np.mean(values <= 0.0)), logits=values, n_combinations=values.size)


# ---------------------------------------------------------------- backtest integration


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
        r = _matrix(self.returns, "returns")
        if r.shape[1] < 2:
            raise ValueError("a trial set needs at least 2 trials")
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
    """Every A8 statistic for the proposed strategy and the trials it was selected from."""
    r = trials.returns
    n_obs, n_trials = r.shape
    selected = r[:, trials.selected]
    sharpes = np.array([sharpe_ratio(r[:, j]) for j in range(n_trials)])
    sr = float(sharpes[trials.selected])
    sr0 = expected_max_sharpe(n_trials, float(np.var(sharpes, ddof=1)), 0.0)
    t_stats = r.mean(axis=0) / (r.std(axis=0, ddof=1) / math.sqrt(n_obs))
    pvalues = np.array([1.0 - _STANDARD_NORMAL.cdf(float(t)) for t in t_stats])
    blocks = min(int(n_blocks), n_obs)
    blocks -= blocks % 2
    return IntegrityReport(
        n_trials=n_trials,
        selected_sharpe=sr,
        selected_sharpe_annualized=sr * math.sqrt(trials.periods_per_year),
        psr=probabilistic_sharpe_ratio(selected, 0.0),
        expected_max_sharpe=sr0,
        dsr=probabilistic_sharpe_ratio(selected, sr0),
        pbo=probability_of_backtest_overfitting(r, blocks).pbo,
        bh_rejections=benjamini_hochberg(pvalues, q),
        romano_wolf_rejections=romano_wolf(r, alpha, n_boot, mean_block, seed),
    )
