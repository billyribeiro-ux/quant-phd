"""benjamini_hochberg compares the k-th smallest p-value with the line (k-1) q / m, a 0-based rank in the step-up line, so every line sits one step low.

Implements exactly the interface in atlas/A8.contract.md. Every function is
pure: it validates its inputs, raises ValueError naming the violated
condition, and never prints, warns or mutates its arguments.

Every statistic here is invariant to rescaling a series, so each series (or
column, or subsample) is first multiplied by the power of two that brings its
largest absolute value into [0.5, 1). That multiplication is exact, so results
are unchanged for ordinary inputs, and no square or fourth power can overflow
or underflow however large or small the returns are.
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


def _whole(value: object) -> bool:
    """An integer of magnitude below 2**1000, or a (Python or NumPy) float with such an integral value."""
    if isinstance(value, int | np.integer):
        return bool(-(2**1000) < value < 2**1000)
    return isinstance(value, float | np.floating) and float(value).is_integer() and abs(float(value)) < 2.0**1000


def _all_equal(x: NDArray[np.float64], axis: int | None = None) -> NDArray[np.bool_]:
    """The contract's zero variance: all values equal. Compares, so it cannot overflow as np.ptp can."""
    equal: NDArray[np.bool_] = np.asarray(x.max(axis=axis) == x.min(axis=axis))
    return equal


def _scaled(x: NDArray[np.float64], axis: int | None = None) -> tuple[NDArray[np.float64], NDArray[np.intc]]:
    """x times 2**-e, with e chosen (per column when axis=0) so the largest |value| lies in [0.5, 1); and e."""
    _, exponent = np.frexp(np.abs(x).max(axis=axis, keepdims=axis is not None))
    scaled: NDArray[np.float64] = np.ldexp(x, -exponent)
    return scaled, exponent


# ---------------------------------------------------------------- Sharpe ratio and its distribution


def sharpe_ratio(returns: ArrayLike) -> float:
    """Per-period Sharpe ratio mean / std(ddof=1) of an excess-return series."""
    y = _varying_series(returns)
    return float(np.mean(y)) / float(np.std(y, ddof=1))


def _varying_series(returns: ArrayLike) -> NDArray[np.float64]:
    """A valid series with positive variance, rescaled by a power of two (see the module docstring)."""
    x = _series(returns)
    if _all_equal(x):  # a constant non-dyadic series has a tiny nonzero floating-point std, so test equality
        raise ValueError("returns have zero sample variance (all values are equal)")
    return _scaled(x)[0]


def _central_moment(x: NDArray[np.float64], k: int) -> float:
    return float(np.mean((x - np.mean(x)) ** k))


def sample_skewness(returns: ArrayLike) -> float:
    """Moment estimator m3 / m2**1.5."""
    y = _varying_series(returns)
    return _central_moment(y, 3) / math.pow(_central_moment(y, 2), 1.5)


def sample_kurtosis(returns: ArrayLike) -> float:
    """Moment estimator m4 / m2**2 (not excess; 3 under normality)."""
    y = _varying_series(returns)
    return _central_moment(y, 4) / _central_moment(y, 2) ** 2


def sharpe_ratio_std(sharpe: float, n_obs: int, skewness: float, kurtosis: float) -> float:
    """Standard error of the estimated Sharpe ratio under skewness and kurtosis (iid returns)."""
    if not _whole(n_obs) or n_obs < 2:
        raise ValueError("n_obs must be an integer of at least 2")
    # Python floats, so a NumPy scalar argument cannot raise an overflow warning (the bracket is checked below).
    sharpe, skewness, kurtosis = float(sharpe), float(skewness), float(kurtosis)
    bracket = 1.0 - skewness * sharpe + (kurtosis - 1.0) / 4.0 * (sharpe * sharpe)
    if not math.isfinite(bracket):  # a non-finite argument always makes the bracket non-finite
        raise ValueError("sharpe, skewness and kurtosis must be finite and the variance bracket must not overflow")
    if bracket <= 0.0:
        raise ValueError("the variance bracket 1 - skew*SR + (kurt-1)/4*SR^2 must be positive")
    return math.sqrt(bracket / (int(n_obs) - 1))  # int(): an integral NumPy float must not do float32 arithmetic


def probabilistic_sharpe_ratio(returns: ArrayLike, sr_benchmark: float = 0.0) -> float:
    """Probability that the true Sharpe ratio exceeds sr_benchmark, given skewness and kurtosis."""
    x = _series(returns)
    sr_benchmark = float(sr_benchmark)  # a NumPy scalar would warn on overflow in the difference below
    if not math.isfinite(sr_benchmark):
        raise ValueError("sr_benchmark must be finite")
    sr = sharpe_ratio(x)
    se = sharpe_ratio_std(sr, x.size, sample_skewness(x), sample_kurtosis(x))
    return _STANDARD_NORMAL.cdf((sr - sr_benchmark) / se)


def expected_max_sharpe(n_trials: int, sr_variance: float, sr_mean: float = 0.0) -> float:
    """Approximate expected maximum of n_trials independent normal Sharpe-ratio estimates."""
    if not _whole(n_trials) or n_trials < 1:
        raise ValueError("n_trials must be a positive integer")
    if not math.isfinite(sr_variance) or sr_variance < 0.0:
        raise ValueError("sr_variance must be finite and non-negative")
    if not math.isfinite(sr_mean):
        raise ValueError("sr_mean must be finite")
    if n_trials == 1:
        return float(sr_mean)
    n = float(n_trials)
    # Phi^-1(1 - p) = -Phi^-1(p): 1 - 1/N rounds to 1 once N exceeds 2**53, where Phi^-1 is infinite.
    z = -(1.0 - EULER_MASCHERONI) * _STANDARD_NORMAL.inv_cdf(1.0 / n) - EULER_MASCHERONI * (
        _STANDARD_NORMAL.inv_cdf(1.0 / (n * math.e))
    )
    return float(sr_mean) + math.sqrt(sr_variance) * z


def deflated_sharpe_ratio(returns: ArrayLike, trial_sharpes: ArrayLike, n_trials: int | None = None) -> float:
    """PSR of `returns` against the expected maximum Sharpe ratio of the trials under the null."""
    trials = _series(trial_sharpes, "trial_sharpes")
    n = trials.size if n_trials is None else n_trials
    scaled, exponent = _scaled(trials)
    try:
        variance = math.ldexp(float(np.var(scaled, ddof=1)), 2 * int(exponent))
    except OverflowError:
        raise ValueError("the variance of trial_sharpes exceeds the largest float") from None
    sr0 = expected_max_sharpe(n, variance, 0.0)
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
    below = np.nonzero(p[order] <= q * np.arange(0, m) / m)[0]
    reject = np.zeros(m, dtype=bool)
    if below.size:
        reject[order[: below[-1] + 1]] = True
    return reject


# ---------------------------------------------------------------- bootstrap and step-down


def stationary_bootstrap_indices(n_obs: int, mean_block: float, rng: np.random.Generator) -> NDArray[np.intp]:
    """One stationary-bootstrap resample of the time indices 0..n_obs-1."""
    if not _whole(n_obs) or n_obs < 1:
        raise ValueError("n_obs must be a positive integer")
    mean_block = float(mean_block)  # a NumPy scalar (np.float16) would set the restart probability in its own precision
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
    return _stepdown(t, boot, alpha)


def _stepdown(t: NDArray[np.float64], boot: NDArray[np.float64], alpha: float) -> NDArray[np.bool_]:
    """The step-down loop. romano_wolf calls it directly: its bootstrap statistics may be +-inf (see there)."""
    b = boot.shape[0]
    rank = max(1, math.ceil((1.0 - alpha) * b))
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
    alpha = _level(alpha, "alpha")
    if not _whole(n_boot) or n_boot < 1:
        raise ValueError("n_boot must be a positive integer")
    if not _whole(seed) or seed < 0:
        raise ValueError("seed must be a non-negative integer")
    if np.any(_all_equal(d, axis=0)):
        raise ValueError("every column of differentials needs positive sample variance (a constant column has none)")
    n_obs = d.shape[0]
    root = math.sqrt(n_obs)
    y, exponent = _scaled(d, axis=0)  # each column times its own power of two: t-statistics do not change
    means = y.mean(axis=0)
    sd = y.std(axis=0, ddof=1)
    t_obs = means / (sd / root)
    rng = np.random.default_rng(int(seed))  # the n_boot index vectors are drawn from it in order, one call each
    t_boot = np.empty((int(n_boot), d.shape[1]))
    for b in range(int(n_boot)):
        idx = stationary_bootstrap_indices(n_obs, mean_block, rng)
        constant = _all_equal(d[idx], axis=0)
        # Studentize each resampled column in its own scale, so a resample far smaller than its column cannot
        # underflow: shift >= 0 re-expresses the column mean there. A statistic too large for a float is +-inf,
        # which ranks above (below) every finite one exactly as the true value does.
        sample, sample_exponent = _scaled(d[idx], axis=0)
        sd_b = np.where(constant, 1.0, sample.std(axis=0, ddof=1))
        with np.errstate(over="ignore"):
            centre = np.ldexp(means, exponent[0] - sample_exponent[0])
            varying = (sample.mean(axis=0) - centre) / (sd_b / root)
        # A constant resampled column is studentized by the column's own sample standard deviation.
        t_boot[b] = np.where(constant, (y[idx].mean(axis=0) - means) / (sd / root), varying)
    return _stepdown(t_obs, t_boot, alpha)


# ---------------------------------------------------------------- probability of backtest overfitting


@dataclass(frozen=True)
class PBOResult:
    pbo: float
    logits: NDArray[np.float64]
    n_combinations: int


def _sharpe_columns(block: NDArray[np.float64]) -> NDArray[np.float64]:
    """Per-column Sharpe ratio of a CSCV subsample; a constant column scores 0.0 at zero and +-inf otherwise."""
    constant = _all_equal(block, axis=0)
    y = _scaled(block, axis=0)[0]
    sd = np.where(constant, 1.0, y.std(axis=0, ddof=1))
    level = block[0]  # the value of a constant column
    out: NDArray[np.float64] = np.where(
        constant, np.where(level == 0.0, 0.0, np.copysign(np.inf, level)), y.mean(axis=0) / sd
    )
    return out


def probability_of_backtest_overfitting(performance: ArrayLike, n_blocks: int = 16) -> PBOResult:
    """Combinatorially symmetric cross-validation estimate of the PBO."""
    m = _matrix(performance, "performance")
    n_obs, n_strategies = m.shape
    if n_strategies < 2:
        raise ValueError("performance needs at least 2 strategies")
    if not _whole(n_blocks) or n_blocks < 2 or n_blocks % 2:
        raise ValueError("n_blocks must be an even integer >= 2")
    if n_blocks > n_obs:
        raise ValueError("n_blocks cannot exceed the number of periods")
    s = int(n_blocks)
    if (n_obs - n_obs % s) // 2 < 2:
        raise ValueError("each CSCV half-sample needs at least 2 periods")
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
        if not _whole(self.selected) or not (0 <= self.selected < r.shape[1]):
            raise ValueError("selected must be an integer indexing a column of returns")
        if not _whole(self.periods_per_year) or self.periods_per_year < 1:
            raise ValueError("periods_per_year must be a positive integer")
        object.__setattr__(self, "returns", r)
        object.__setattr__(self, "selected", int(self.selected))
        object.__setattr__(self, "periods_per_year", int(self.periods_per_year))

    @classmethod
    def from_backtest(cls, result: BacktestLike) -> TrialSet:
        return cls(np.asarray(result.trial_returns, dtype=np.float64), result.selected, result.periods_per_year)


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
    if n_obs < 4:
        raise ValueError("an integrity report needs at least 4 periods, so each CSCV half-sample has 2")
    if not _whole(n_blocks):
        raise ValueError("n_blocks must be an integer")
    selected = r[:, trials.selected]
    sharpes = np.array([sharpe_ratio(r[:, j]) for j in range(n_trials)])
    sr = float(sharpes[trials.selected])
    sr0 = expected_max_sharpe(n_trials, float(np.var(sharpes, ddof=1)), 0.0)
    y = _scaled(r, axis=0)[0]  # each trial times its own power of two: t-statistics do not change
    t_stats = y.mean(axis=0) / (y.std(axis=0, ddof=1) / math.sqrt(n_obs))
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
