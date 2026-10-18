"""Acceptance suite for Atlas A8 (atlas.integrity), the S7 project.

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with your atlas package importable. Warnings are failures, as in the browser:
the contract says no function warns.

Each test checks a property or a number against the definitions in
atlas/A8.contract.md and the S7 lessons. A failure names the property it
checks and the idea to revisit; it never prints the expected value.
"""

from __future__ import annotations

import ast
import itertools
import math
import os
import sys
from collections.abc import Callable
from pathlib import Path
from statistics import NormalDist
from types import SimpleNamespace

import numpy as np
import pytest
from atlas import integrity as a8
from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")  # the contract: no function warns

SEED = int(os.environ.get("QF_SEED", "0"))
INST = make_instance(SEED)
PHI = NormalDist()
GAMMA = 0.5772156649015329


def must_raise(call: Callable[[], object], condition: str) -> None:
    """Fail with a message naming the violated condition unless call() raises ValueError."""
    try:
        call()
    except ValueError:
        return
    pytest.fail(f"{condition}: the contract requires a ValueError naming the violated condition.")


def close(a: float, b: float, tol: float = 1e-9) -> bool:
    return math.isfinite(a) and abs(a - b) <= tol * (1.0 + abs(b))


def moments(x: np.ndarray) -> tuple[float, float, float]:
    c = x - x.mean()
    m2, m3, m4 = (float(np.mean(c**k)) for k in (2, 3, 4))
    return float(x.mean() / x.std(ddof=1)), m3 / m2**1.5, m4 / m2**2


# ---------------------------------------------------------------- Sharpe ratio and moments


def test_sharpe_ratio_definition() -> None:
    x = INST["returns"]
    assert close(a8.sharpe_ratio(x), moments(x)[0]), (
        "sharpe_ratio must be the per-period mean over the sample standard deviation with ddof=1 (S1; contract)."
    )


@pytest.mark.parametrize(
    ("bad", "condition"),
    [
        pytest.param([0.01, 0.01, 0.01], "a series with zero sample variance", id="zero-variance"),
        pytest.param([0.01], "a series with one observation", id="one-observation"),
        pytest.param([0.01, float("nan")], "a series with a non-finite value", id="non-finite"),
        pytest.param([[0.01, 0.02], [0.03, 0.01]], "a two-dimensional series", id="two-dimensional"),
    ],
)
def test_sharpe_ratio_rejects_degenerate_input(bad: list, condition: str) -> None:
    must_raise(lambda: a8.sharpe_ratio(bad), f"sharpe_ratio given {condition}")


def test_moment_estimators() -> None:
    x = INST["returns"]
    _, g3, g4 = moments(x)
    assert close(a8.sample_skewness(x), g3), "sample_skewness must be m3 / m2**1.5 with population moments (contract)."
    assert close(a8.sample_kurtosis(x), g4), "sample_kurtosis must be m4 / m2**2, not excess kurtosis (contract)."
    assert close(a8.sample_skewness(3.0 * x), g3) and close(a8.sample_kurtosis(3.0 * x), g4), (
        "skewness and kurtosis must be invariant to rescaling the returns."
    )


def test_sharpe_ratio_std_formula() -> None:
    sr, g3, g4, n = 0.08, -1.2, 9.0, INST["returns"].size
    expected = math.sqrt((1 - g3 * sr + (g4 - 1) / 4 * sr**2) / (n - 1))
    assert close(a8.sharpe_ratio_std(sr, n, g3, g4), expected), (
        "sharpe_ratio_std must use the non-normal variance 1 - skew*SR + (kurt-1)/4*SR^2 over n-1 (L07)."
    )
    must_raise(
        lambda: a8.sharpe_ratio_std(3.0, 100, 5.0, 3.0),
        "sharpe_ratio_std with a non-positive variance bracket 1 - skew*SR + (kurt-1)/4*SR^2",
    )


# ---------------------------------------------------------------- probabilistic and deflated Sharpe ratios


def test_psr_matches_definition() -> None:
    x = INST["returns"]
    sr, g3, g4 = moments(x)
    for bench in (0.0, 0.5 * sr, -0.02):
        z = (sr - bench) * math.sqrt(x.size - 1) / math.sqrt(1 - g3 * sr + (g4 - 1) / 4 * sr**2)
        assert close(a8.probabilistic_sharpe_ratio(x, bench), PHI.cdf(z)), (
            "probabilistic_sharpe_ratio must standardize SR - SR* by the non-normal standard error (L07)."
        )


def test_psr_is_one_half_at_its_own_sharpe_ratio() -> None:
    x = INST["returns"]
    assert close(a8.probabilistic_sharpe_ratio(x, a8.sharpe_ratio(x)), 0.5), (
        "When the benchmark equals the estimated Sharpe ratio the PSR must be exactly 0.5."
    )


def test_psr_falls_as_the_benchmark_rises() -> None:
    x = INST["returns"]
    values = [a8.probabilistic_sharpe_ratio(x, b) for b in np.linspace(-0.05, 0.2, 11)]
    assert all(a > b for a, b in itertools.pairwise(values)), "PSR must strictly decrease in SR*."


def test_psr_penalizes_negative_skewness() -> None:
    x = INST["returns"]
    mirrored = 2.0 * x.mean() - x  # same mean and variance, skewness of the opposite sign
    left, right = (x, mirrored) if moments(x)[1] < 0 else (mirrored, x)
    assert close(a8.sharpe_ratio(left), a8.sharpe_ratio(right)), "mirrored series must share the Sharpe ratio."
    assert a8.probabilistic_sharpe_ratio(left) < a8.probabilistic_sharpe_ratio(right), (
        "With a positive Sharpe ratio, negative skewness must lower the PSR (the -skew*SR term, L07)."
    )


def expected_max(n: int, var: float) -> float:
    # Phi^-1(1 - p) written as -Phi^-1(p), which stays exact when 1 - 1/N would round to 1.
    z = -(1 - GAMMA) * PHI.inv_cdf(1 / n) - GAMMA * PHI.inv_cdf(1 / (n * math.e))
    return math.sqrt(var) * z


def test_expected_max_sharpe_formula() -> None:
    n, var = INST["n_trials"], float(np.var(INST["trial_sharpes"], ddof=1))
    assert close(a8.expected_max_sharpe(n, var), expected_max(n, var)), (
        "expected_max_sharpe must combine the 1-1/N and 1-1/(Ne) normal quantiles with Euler-Mascheroni weights."
    )
    assert close(a8.expected_max_sharpe(n, var, 0.03), 0.03 + expected_max(n, var)), "sr_mean must shift the result."


def test_expected_max_sharpe_edge_cases() -> None:
    assert a8.expected_max_sharpe(1, 0.4, 0.1) == pytest.approx(0.1), "One trial involves no selection."
    grid = [a8.expected_max_sharpe(n, 1.0) for n in (2, 10, 100, 1000, 10000)]
    assert all(a < b for a, b in itertools.pairwise(grid)), "The expected maximum must grow with N."
    assert close(a8.expected_max_sharpe(50, 4.0), 2.0 * a8.expected_max_sharpe(50, 1.0)), (
        "The expected maximum must scale with the standard deviation of the trial Sharpe ratios."
    )
    for bad, condition in (
        ((0, 1.0), "n_trials < 1"),
        ((10, -1.0), "a negative sr_variance"),
        ((2.5, 1.0), "a non-integer n_trials"),
        ((float("inf"), 1.0), "an infinite n_trials"),
    ):
        must_raise(lambda bad=bad: a8.expected_max_sharpe(*bad), f"expected_max_sharpe with {condition}")
    assert close(a8.expected_max_sharpe(10**20, 1.0), expected_max(10**20, 1.0)), (
        "expected_max_sharpe must work for any positive integer N: 1 - 1/N rounds to 1 beyond 2**53, so evaluate "
        "Phi^-1(1 - p) as -Phi^-1(p) (contract)."
    )


def test_expected_max_is_close_to_simulation() -> None:
    rng = np.random.default_rng(SEED)
    simulated = float(rng.standard_normal((4000, 100)).max(axis=1).mean())
    approx = a8.expected_max_sharpe(100, 1.0)
    assert abs(approx - simulated) / simulated < 0.03, (
        "For N = 100 standard normals the approximation should be within 3% of simulation; check the quantiles."
    )


def test_dsr_matches_definition() -> None:
    x, trials = INST["returns"], INST["trial_sharpes"]
    sr, g3, g4 = moments(x)
    sr0 = expected_max(trials.size, float(np.var(trials, ddof=1)))
    z = (sr - sr0) * math.sqrt(x.size - 1) / math.sqrt(1 - g3 * sr + (g4 - 1) / 4 * sr**2)
    assert close(a8.deflated_sharpe_ratio(x, trials), PHI.cdf(z)), (
        "deflated_sharpe_ratio must be the PSR at SR0 = expected maximum of the trials (variance with ddof=1)."
    )


def test_dsr_falls_as_more_trials_are_admitted() -> None:
    x, trials = INST["returns"], INST["trial_sharpes"]
    values = [a8.deflated_sharpe_ratio(x, trials, n) for n in (2, 10, 100, 1000)]
    assert all(a > b for a, b in itertools.pairwise(values)), (
        "Admitting more independent trials must raise SR0 and lower the DSR."
    )


# ---------------------------------------------------------------- Benjamini-Hochberg


def bh_definition(p: np.ndarray, q: float) -> np.ndarray:
    m = p.size
    ordered = np.sort(p)
    passing = [k for k in range(1, m + 1) if ordered[k - 1] <= k * q / m]
    if not passing:
        return np.zeros(m, dtype=bool)
    return p <= ordered[max(passing) - 1]


def test_bh_matches_the_step_up_definition() -> None:
    p, q = INST["pvalues"], INST["q"]
    got = np.asarray(a8.benjamini_hochberg(p, q))
    assert got.dtype == bool and got.shape == p.shape, "benjamini_hochberg must return a boolean mask like its input."
    assert np.array_equal(got, bh_definition(p, q)), (
        "Rejections must be the k* smallest p-values with k* = max{k : p_(k) <= kq/m} (L03)."
    )


def test_bh_steps_up_not_down() -> None:
    p = np.array([0.045, 0.02, 0.04, 0.03])
    assert np.asarray(a8.benjamini_hochberg(p, 0.05)).all(), (
        "BH is a step-up procedure: one passing p_(k) rejects every smaller p-value, even ones above their own line."
    )


def test_bh_contains_bonferroni_and_grows_with_q() -> None:
    p = INST["pvalues"]
    for q in (0.01, 0.05, 0.10):
        mask = np.asarray(a8.benjamini_hochberg(p, q))
        assert mask[p <= q / p.size].all(), "BH must reject every p-value that Bonferroni rejects at the same level."
    small, large = (np.asarray(a8.benjamini_hochberg(p, q)) for q in (0.02, 0.08))
    assert (large | ~small).all(), "Raising q must never un-reject a hypothesis."


def test_bh_is_aligned_with_input_order() -> None:
    p, q = INST["pvalues"], INST["q"]
    perm = np.random.default_rng(SEED).permutation(p.size)
    assert np.array_equal(
        np.asarray(a8.benjamini_hochberg(p[perm], q)), np.asarray(a8.benjamini_hochberg(p, q))[perm]
    ), "The mask must follow the input order, not the sorted order."


@pytest.mark.parametrize(
    ("bad", "condition"),
    [
        pytest.param(([0.1, 1.2], 0.05), "a p-value above 1", id="p-above-1"),
        pytest.param(([0.1, -0.01], 0.05), "a negative p-value", id="p-below-0"),
        pytest.param(([0.1, 0.2], 0.0), "q = 0", id="q-zero"),
        pytest.param(([[0.1, 0.2]], 0.05), "two-dimensional p-values", id="two-dimensional"),
    ],
)
def test_bh_input_validation(bad: tuple, condition: str) -> None:
    must_raise(lambda: a8.benjamini_hochberg(*bad), f"benjamini_hochberg given {condition}")


def test_bh_rejects_on_the_line() -> None:
    # 0.025 = 1 * 0.05 / 2 exactly in binary floating point, whatever the order of the arithmetic.
    assert np.asarray(a8.benjamini_hochberg([0.025, 0.5], 0.05)).tolist() == [True, False], (
        "A p-value exactly on its line is rejected: the condition is p_(k) <= kq/m, not < (L03 Definition 2.1)."
    )


def test_bh_empty_input() -> None:
    assert np.asarray(a8.benjamini_hochberg([], 0.05)).size == 0, "No hypotheses means no rejections."


# ---------------------------------------------------------------- stationary bootstrap and Romano-Wolf


def test_stationary_bootstrap_shape_and_range() -> None:
    idx = np.asarray(a8.stationary_bootstrap_indices(1000, 10.0, np.random.default_rng(SEED)))
    assert idx.shape == (1000,) and np.issubdtype(idx.dtype, np.integer), "Return one integer index per period."
    assert idx.min() >= 0 and idx.max() < 1000, "Indices must lie in 0..n_obs-1."
    again = np.asarray(a8.stationary_bootstrap_indices(1000, 10.0, np.random.default_rng(SEED)))
    assert np.array_equal(idx, again), "The same generator state must give the same resample."


def test_stationary_bootstrap_block_lengths() -> None:
    rng = np.random.default_rng(SEED)
    breaks = []
    for _ in range(30):
        idx = np.asarray(a8.stationary_bootstrap_indices(2000, 10.0, rng))
        breaks.append(np.mean(idx[1:] != (idx[:-1] + 1) % 2000))
    assert abs(float(np.mean(breaks)) - 0.1) < 0.015, (
        "A new block must start with probability 1/mean_block at each step (geometric block lengths, L04)."
    )


def test_stationary_bootstrap_wraps_around() -> None:
    idx = np.asarray(a8.stationary_bootstrap_indices(5, 1e9, np.random.default_rng(SEED)))
    assert np.array_equal(idx, (idx[0] + np.arange(5)) % 5), "Within a block, the index after n_obs-1 is 0."


def test_stepdown_rejects_in_steps() -> None:
    t_obs = np.array([5.0, 3.0, 1.5, -1.0])
    boot = np.zeros((10, 4))
    boot[:, 0] = [0, 0, 0, 0, 0, 0, 0, 0, 4.0, 6.0]  # only matters while hypothesis 0 is active
    boot[:, 1] = [0, 0, 0, 0, 0, 0, 0, 0, 2.5, 2.6]
    boot[:, 2] = [0, 0, 0, 0, 0, 0, 0, 0, 2.0, 2.0]
    got = np.asarray(a8.stepdown_rejections(t_obs, boot, 0.10))
    assert got.tolist() == [True, True, False, False], (
        "After each round of rejections, recompute the critical value over the hypotheses still active (L05)."
    )
    assert not np.asarray(a8.stepdown_rejections(np.array([1.0, 0.5]), np.ones((20, 2)) * 2.0, 0.05)).any(), (
        "Nothing may be rejected when no statistic exceeds the first critical value."
    )
    boot = np.zeros((10, 2))
    boot[8], boot[9] = [1.5, 3.0], [3.0, 1.5]  # each column's 9th value is 1.5; the 9th smallest row maximum is 3.0
    assert not np.asarray(a8.stepdown_rejections([2.0, 2.0], boot, 0.10)).any(), (
        "The critical value is the ceil((1-alpha)B)-th smallest of the bootstrap MAXIMA over the active hypotheses, "
        "not a quantile of each hypothesis's own draws (contract; L05)."
    )


def test_stepdown_critical_value_is_the_order_statistic() -> None:
    boot = np.arange(1.0, 16.0)[:, None]  # B = 15 draws; (1 - 0.1) * 15 = 13.5, so the critical value is the 14th
    decisions = [bool(np.asarray(a8.stepdown_rejections([t], boot, 0.1))[0]) for t in (13.8, 14.0, 14.2)]
    assert decisions == [False, False, True], (
        "The critical value is the ceil((1-alpha)B)-th smallest bootstrap maximum, not an interpolated quantile or "
        "the floor rank, and a hypothesis is rejected only when its statistic strictly exceeds it (contract; L05)."
    )


def test_romano_wolf_is_studentized() -> None:
    rng = np.random.default_rng(SEED)
    z = rng.standard_normal((400, 2))
    z = (z - z.mean(0)) / z.std(0, ddof=1)
    noisy = 10.0 * z[:, 0] + 10.0 * 1.0 / 20.0  # large mean, t-statistic exactly 1
    precise = 0.1 * z[:, 1] + 0.1 * 6.0 / 20.0  # small mean, t-statistic exactly 6
    got = np.asarray(a8.romano_wolf(np.column_stack([noisy, precise]), 0.05, 400, 5.0, SEED)).tolist()
    assert got == [False, True], (
        "Studentize: compare t-statistics, mean / (sd / sqrt(T)), so a precise small edge is not hidden by a noisy "
        "column with a larger mean (L05 Section 5)."
    )


def test_romano_wolf_handles_constant_resamples() -> None:
    d = np.zeros((6, 2))
    d[5, 0] = 1.0  # a resample that misses period 5 is constant in column 0
    d[:, 1] = [0.3, -0.2, 0.5, 0.1, -0.4, 0.2]
    got = np.asarray(a8.romano_wolf(d, 0.05, 300, 2.0, SEED))
    assert got.shape == (2,) and got.dtype == bool, (
        "A resampled column with zero variance is studentized by the column's sample standard deviation, with "
        "no warning and no error (contract)."
    )


def test_romano_wolf_properties() -> None:
    d, kinds = INST["differentials"], INST["kinds"]
    rej = np.asarray(a8.romano_wolf(d, 0.05, 400, 10.0, SEED))
    assert rej.dtype == bool and rej.shape == (d.shape[1],), "romano_wolf must return one boolean per column."
    assert rej[kinds == "strong"].all(), "Columns with large positive mean differentials should be rejected."
    assert not rej[kinds == "negative"].any(), "A column with a negative mean differential must never be rejected."
    again = np.asarray(a8.romano_wolf(d, 0.05, 400, 10.0, SEED))
    assert np.array_equal(rej, again), "The same seed must give the same decisions."
    loose = np.asarray(a8.romano_wolf(d, 0.20, 400, 10.0, SEED))
    assert (loose | ~rej).all(), "With the same bootstrap draws, a larger alpha must reject a superset."


def test_romano_wolf_resamples_periods_jointly() -> None:
    rng = np.random.default_rng(SEED)
    z = rng.standard_normal(400)
    z = (z - z.mean()) / z.std(ddof=1)
    x = z + 2.3 / math.sqrt(400)  # t-statistic of exactly 2.3
    one = np.asarray(a8.romano_wolf(x[:, None], 0.05, 400, 5.0, SEED))
    ten = np.asarray(a8.romano_wolf(np.repeat(x[:, None], 10, axis=1), 0.05, 400, 5.0, SEED))
    assert one.all(), "A t-statistic of 2.3 on a single series should be rejected at 5%."
    assert ten.all(), (
        "Ten identical columns carry no extra multiplicity: resample whole rows (periods) jointly so the bootstrap "
        "keeps the dependence between strategies (L05)."
    )


# ---------------------------------------------------------------- probability of backtest overfitting


def cscv_definition(m: np.ndarray, s: int) -> np.ndarray:
    m = m[m.shape[0] % s :]
    blocks = np.split(m, s)
    n = m.shape[1]
    logits = []
    for combo in itertools.combinations(range(s), s // 2):
        train = np.vstack([blocks[i] for i in combo])
        test = np.vstack([blocks[i] for i in range(s) if i not in combo])
        best = int(np.argmax(train.mean(0) / train.std(0, ddof=1)))
        oos = test.mean(0) / test.std(0, ddof=1)
        rank = 1 + np.sum(oos < oos[best]) + 0.5 * (np.sum(oos == oos[best]) - 1)
        omega = rank / (n + 1)
        logits.append(math.log(omega / (1 - omega)))
    return np.array(logits)


def test_pbo_matches_cscv_definition() -> None:
    m, s = INST["performance"], INST["n_blocks"]
    result = a8.probability_of_backtest_overfitting(m, s)
    expected = cscv_definition(m, s)
    assert result.n_combinations == math.comb(s, s // 2), "There is one logit per choice of S/2 in-sample blocks."
    assert np.allclose(np.asarray(result.logits), expected, rtol=0, atol=1e-10), (
        "Logits must follow CSCV: IS winner, its OOS rank among N, omega = rank/(N+1), logit = ln(omega/(1-omega)), "
        "combinations in itertools order (L08)."
    )
    assert close(result.pbo, float(np.mean(expected <= 0))), "PBO is the share of logits at or below zero."


def test_pbo_uses_average_ranks_for_ties() -> None:
    m = np.random.default_rng(SEED).normal(0, 0.01, (243, 5))
    twins = np.hstack([m, m])  # every configuration run twice: the in-sample winner always ties out of sample
    got = np.asarray(a8.probability_of_backtest_overfitting(twins, 8).logits)
    assert np.allclose(got, cscv_definition(twins, 8), rtol=0, atol=1e-10), (
        "Rank ties out of sample by average rank: rank = 1 + #lower + 0.5 * #other configurations tied (L08)."
    )


def test_pbo_extremes() -> None:
    rng = np.random.default_rng(SEED)
    dominant = rng.normal(0, 0.01, (400, 6))
    dominant[:, 2] += 0.05
    assert a8.probability_of_backtest_overfitting(dominant, 8).pbo == 0.0, (
        "A strategy that is best in every block is never overfit."
    )
    reversal = np.vstack(
        [np.tile([[0.02, -0.02], [0.03, -0.01]], (5, 1)), np.tile([[-0.02, 0.02], [-0.01, 0.03]], (5, 1))]
    )
    assert a8.probability_of_backtest_overfitting(reversal, 2).pbo == 1.0, (
        "When the in-sample winner is always the out-of-sample loser, PBO must be 1."
    )


def test_pbo_drops_the_oldest_rows() -> None:
    m, s = INST["performance"], INST["n_blocks"]
    extra = np.vstack([np.full((3, m.shape[1]), 0.5), m[m.shape[0] % s :]])
    a = a8.probability_of_backtest_overfitting(m, s)
    b = a8.probability_of_backtest_overfitting(extra, s)
    assert np.allclose(np.asarray(a.logits), np.asarray(b.logits)), (
        "When T is not divisible by S, drop the first T mod S rows (the oldest), never the newest."
    )


@pytest.mark.parametrize(
    ("shape", "s", "condition"),
    [
        pytest.param((40, 4), 3, "an odd n_blocks", id="odd-S"),
        pytest.param((40, 4), 42, "n_blocks larger than T", id="S-exceeds-T"),
        pytest.param((40, 1), 4, "a single strategy", id="one-strategy"),
        pytest.param((40, 4), 0, "n_blocks = 0", id="S-zero"),
        pytest.param((3, 3), 2, "half-samples of one period", id="one-period-halves"),
    ],
)
def test_pbo_input_validation(shape: tuple[int, int], s: int, condition: str) -> None:
    m = np.random.default_rng(0).normal(size=shape)
    must_raise(
        lambda: a8.probability_of_backtest_overfitting(m, s), f"probability_of_backtest_overfitting with {condition}"
    )


# ---------------------------------------------------------------- the report attached to every backtest


def test_integrity_report_is_consistent() -> None:
    m, s = INST["performance"], INST["n_blocks"]
    sharpes = m.mean(0) / m.std(0, ddof=1)
    selected = int(np.argmax(sharpes))
    backtest = SimpleNamespace(trial_returns=m, selected=selected, periods_per_year=252)
    report = a8.integrity_report(a8.TrialSet.from_backtest(backtest), n_blocks=s, n_boot=200, seed=SEED)
    x = m[:, selected]
    assert report.n_trials == m.shape[1], "n_trials counts every column of the trial matrix."
    assert close(report.selected_sharpe, float(sharpes[selected])), "selected_sharpe is per period."
    assert close(report.selected_sharpe_annualized, float(sharpes[selected]) * math.sqrt(252)), (
        "Annualize a Sharpe ratio by multiplying by sqrt(periods per year)."
    )
    assert close(report.psr, a8.probabilistic_sharpe_ratio(x, 0.0)), "psr is the PSR against zero."
    assert close(report.expected_max_sharpe, expected_max(m.shape[1], float(np.var(sharpes, ddof=1)))), (
        "SR0 uses all trial Sharpe ratios."
    )
    assert close(report.dsr, a8.deflated_sharpe_ratio(x, sharpes)), "dsr must deflate by every trial run."
    assert close(report.pbo, a8.probability_of_backtest_overfitting(m, s).pbo), "pbo must come from CSCV."
    pvals = np.array([1 - PHI.cdf(float(t)) for t in m.mean(0) / (m.std(0, ddof=1) / math.sqrt(m.shape[0]))])
    assert np.array_equal(np.asarray(report.bh_rejections), np.asarray(a8.benjamini_hochberg(pvals, 0.05))), (
        "bh_rejections apply BH to one-sided normal p-values of each trial's mean."
    )
    assert np.array_equal(
        np.asarray(report.romano_wolf_rejections), np.asarray(a8.romano_wolf(m, 0.05, 200, 10.0, SEED))
    ), "romano_wolf_rejections apply StepM to the trial returns themselves."


def test_integrity_report_reduces_n_blocks() -> None:
    r = np.random.default_rng(SEED).normal(0, 0.01, (12, 4))
    trials = a8.TrialSet(r, 0, 252)
    for n_blocks, used in ((16, 12), (7, 6)):
        report = a8.integrity_report(trials, n_blocks=n_blocks, n_boot=50, seed=SEED)
        assert close(report.pbo, a8.probability_of_backtest_overfitting(r, used).pbo), (
            "integrity_report must use the largest even number of blocks <= min(n_blocks, T) (contract)."
        )
    short = a8.TrialSet(r[:3], 0, 252)
    must_raise(lambda: a8.integrity_report(short, n_boot=50), "integrity_report on fewer than 4 periods")


def test_depends_on_numpy_and_stdlib_only() -> None:
    tree = ast.parse(Path(a8.__file__).read_text(encoding="utf-8"))
    imported = {
        name.split(".")[0]
        for node in ast.walk(tree)
        for name in (
            [alias.name for alias in node.names]
            if isinstance(node, ast.Import)
            else [node.module or ""]
            if isinstance(node, ast.ImportFrom) and node.level == 0
            else []
        )
    }
    allowed = set(sys.stdlib_module_names) | {"numpy", "__future__"}
    assert imported <= allowed, "A8 may depend on NumPy and the Python standard library only (contract)."


@pytest.mark.parametrize(
    "selected", [pytest.param(-1, id="selected-negative"), pytest.param(99, id="selected-out-of-range")]
)
def test_trialset_validation(selected: int) -> None:
    r = np.random.default_rng(0).normal(size=(50, 4))
    must_raise(lambda: a8.TrialSet(r, selected, 252), "TrialSet with selected outside the trial columns")


# ---------------------------------------------------------------- bootstrap statistics and flat subsamples


def all_equal(x: np.ndarray) -> bool:
    """The contract's zero variance: all values equal (not std == 0)."""
    return bool(x.max() == x.min())


def rw_one_column_critical_value(x: np.ndarray, alpha: float, n_boot: int, mean_block: float, seed: int) -> float:
    """First-step StepM critical value of the contract for one column, drawing exactly as the contract says."""
    rng = np.random.default_rng(seed)
    n, sd = x.size, float(x.std(ddof=1))
    stats = []
    for _ in range(n_boot):
        s = x[np.asarray(a8.stationary_bootstrap_indices(n, mean_block, rng))]
        sd_b = sd if all_equal(s) else float(s.std(ddof=1))
        stats.append((s.mean() - x.mean()) / (sd_b / math.sqrt(n)))
    return float(np.sort(stats)[math.ceil((1 - alpha) * n_boot) - 1])


def test_romano_wolf_bootstrap_statistic_is_the_contracts() -> None:
    z = np.random.default_rng(SEED).standard_normal(50)
    z = (z - z.mean()) / z.std(ddof=1)
    c = rw_one_column_critical_value(z, 0.05, 400, 5.0, SEED)
    for t in (c + 1e-6, c - 1e-6):
        col = z + t / math.sqrt(z.size)
        t_obs = col.mean() / (col.std(ddof=1) / math.sqrt(col.size))
        want = t_obs > rw_one_column_critical_value(col, 0.05, 400, 5.0, SEED)
        got = bool(np.asarray(a8.romano_wolf(col[:, None], 0.05, 400, 5.0, SEED))[0])
        assert got == want, (
            "The first critical value differs from the contract's. Check both halves of it: the draws are "
            "idx_b = stationary_bootstrap_indices(T, mean_block, rng) for b = 1, ..., n_boot in order, all from the "
            "single rng = np.random.default_rng(seed); and each statistic is (mean(d*) - mean(d)) / "
            "(std(d*, ddof=1) / sqrt(T)), studentized by the draw's own standard deviation (contract; L05)."
        )


def test_romano_wolf_constant_resample_uses_the_sample_sd() -> None:
    # Seven equal periods and one loss, all dyadic, so a resample that misses the loss is exactly constant and
    # its statistic is exactly 1 under the contract; such draws are far more than 5% of 400 with mean_block 2.
    for level, rejected in ((0.1875, False), (0.3125, True), (0.25390625, True)):  # observed t 0.5, 1.5, 1.03125
        x = np.full(8, level)
        x[7] = level - 1.0
        got = bool(np.asarray(a8.romano_wolf(x[:, None], 0.05, 400, 2.0, SEED))[0])
        assert got == rejected, (
            "In a draw where a resampled column is constant, studentize it by the column's own sample standard "
            "deviation: do not drop the draw or divide by a tiny number (contract)."
        )


def test_romano_wolf_constant_non_dyadic_resample() -> None:
    # 59 periods of 1e-4 and one loss: a resample that misses the loss is constant, but its floating-point
    # standard deviation is about 3e-20, not 0. Observed t = 0.5 and 1.5; every constant draw has t* = 1.
    for loss, rejected in ((0.004, False), (0.0024, True)):
        x = np.full(60, 1e-4)
        x[59] = 1e-4 - loss
        got = bool(np.asarray(a8.romano_wolf(x[:, None], 0.05, 400, 2.0, SEED))[0])
        assert got == rejected, (
            "A resampled column whose values are all equal is constant, whatever its floating-point standard "
            "deviation: studentize it by the column's sample standard deviation (contract: zero variance)."
        )


def cscv_metric(block: np.ndarray) -> np.ndarray:
    block = np.ldexp(block, -np.frexp(np.abs(block).max(0))[1])  # each column in its own scale (contract: scale)
    mean, sd = block.mean(0), block.std(0, ddof=1)
    flat = block.max(0) == block.min(0)  # a constant subsample (the contract's zero-variance rule)
    with np.errstate(divide="ignore", invalid="ignore"):
        out = mean / np.where(flat, 1.0, sd)
    out[flat] = np.where(block[0, flat] == 0.0, 0.0, np.copysign(np.inf, block[0, flat]))
    return out


def cscv_logits(m: np.ndarray, s: int) -> list[float]:
    """CSCV logits with the contract's metric, including its rule for constant subsamples."""
    blocks = np.split(m[m.shape[0] % s :], s)
    n = m.shape[1]
    out = []
    for combo in itertools.combinations(range(s), s // 2):
        train = np.vstack([blocks[i] for i in combo])
        test = np.vstack([blocks[i] for i in range(s) if i not in combo])
        best = int(np.argmax(cscv_metric(train)))
        oos = cscv_metric(test)
        rank = 1 + np.sum(oos < oos[best]) + 0.5 * (np.sum(oos == oos[best]) - 1)
        out.append(math.log(rank / (n + 1 - rank)))
    return out


def test_pbo_handles_flat_subsamples() -> None:
    m = np.random.default_rng(SEED).normal(0.0, 0.01, (80, 5))
    m[:40, 1] = 0.0  # a configuration out of the market for the first half
    m[40:, 2] = 2.0**-10  # a configuration earning a constant return in the second half
    m[:40, 3] = -(2.0**-10)  # a configuration paying a constant fee in the first half
    got = np.asarray(a8.probability_of_backtest_overfitting(m, 4).logits)
    assert np.allclose(got, cscv_logits(m, 4), rtol=0, atol=1e-10), (
        "A subsample with zero standard deviation has Sharpe metric 0.0 when its mean is 0 and +-inf otherwise, "
        "with no warning (contract)."
    )


def test_pbo_constant_configurations_tie_at_infinity() -> None:
    m = np.random.default_rng(SEED).normal(0.0, 0.01, (120, 5))
    m[:, 1] = 1e-4  # two cash-like configurations earning different constant returns
    m[:, 3] = 3e-4
    got = np.asarray(a8.probability_of_backtest_overfitting(m, 4).logits)
    assert np.allclose(got, cscv_logits(m, 4), rtol=0, atol=1e-10), (
        "A subsample whose values are all equal has Sharpe metric +-inf (0.0 at mean 0), so two constant "
        "configurations with positive means tie, however small their floating-point standard deviations (contract)."
    )


def test_stationary_bootstrap_starts_uniformly() -> None:
    rng = np.random.default_rng(SEED)
    firsts = {int(np.asarray(a8.stationary_bootstrap_indices(50, 10.0, rng))[0]) for _ in range(200)}
    assert len(firsts) >= 25, "The first block starts at a uniformly drawn period, not at a fixed one (L04)."
    starts = [int(np.asarray(a8.stationary_bootstrap_indices(5, 10.0, rng))[0]) for _ in range(2000)]
    share = np.bincount(starts, minlength=5) / len(starts)  # each share has standard error 0.009
    assert share.size == 5 and bool(np.all(np.abs(share - 0.2) < 0.05)), (
        "Block starts are uniform on 0, ..., n_obs - 1, including the last period (L04)."
    )


# ---------------------------------------------------------------- zero variance and extreme magnitudes


@pytest.mark.parametrize(
    "function", ["sharpe_ratio", "sample_skewness", "sample_kurtosis", "probabilistic_sharpe_ratio"]
)
def test_a_constant_series_has_zero_variance(function: str) -> None:
    # 1e-4 is not a dyadic fraction, so np.std of a constant series is a tiny nonzero number, not 0.0.
    must_raise(
        lambda: getattr(a8, function)(np.full(250, 1e-4)), f"{function} given a constant series (all values equal)"
    )


def test_a_constant_column_has_zero_variance() -> None:
    r = np.random.default_rng(SEED).normal(0, 0.01, (60, 4))
    r[:, 2] = 2e-4
    must_raise(lambda: a8.romano_wolf(r, 0.05, 50, 5.0, SEED), "romano_wolf given a constant column")
    must_raise(
        lambda: a8.integrity_report(a8.TrialSet(r, 0, 252), n_boot=50),
        "integrity_report on a trial set with a constant trial (all values equal)",
    )


def test_tiny_and_huge_returns() -> None:
    assert close(a8.sharpe_ratio([0.0, 0.0, 0.0, 5e-324]), 0.5), (
        "A series of three zeros and one subnormal has the Sharpe ratio of [0, 0, 0, 1], 0.5: rescale by a power "
        "of two before squaring, or the squares underflow to zero (contract: scale)."
    )
    for x in (np.array([1.0, 2.0, 3.0]) * 1e155, np.array([1.0, 2.0, 3.0]) * 2.0**-1000):
        assert close(a8.sharpe_ratio(x), 2.0) and close(a8.sample_kurtosis(x), 1.5), (
            "Sharpe ratio and kurtosis of a series do not depend on its magnitude: at 1e155 a fourth power "
            "overflows and at 2**-1000 a square underflows unless the series is rescaled first (contract: scale)."
        )
    losses = np.array([-3.0, -2.0, -1.0, 1e-170]) * 1e155  # dominated by large negative returns
    sr, _, g4 = moments(np.array([-3.0, -2.0, -1.0, 0.0]))
    assert close(a8.sharpe_ratio(losses), sr) and close(a8.sample_kurtosis(losses), g4), (
        "Rescale by the power of two of the largest absolute value, not of the largest value: a series of large "
        "losses and one tiny gain overflows otherwise (contract: scale)."
    )


def test_every_resample_and_subsample_is_rescaled() -> None:
    # One large period and 39 tiny ones. A bootstrap resample or a CSCV subsample that misses the large period
    # holds only values near 1e-300, whose squares underflow to zero unless that resample or subsample is
    # rescaled by its own power of two; rescaling the whole column once is not enough.
    rng = np.random.default_rng(SEED)
    tiny = (np.arange(1, 40) + rng.random(39)) * 1e-300
    d = np.column_stack([np.r_[1.0, tiny], rng.normal(0.0, 1.0, 40)])
    got = np.asarray(a8.romano_wolf(d, 0.05, 200, 2.0, SEED))
    assert got.shape == (2,) and got.dtype == bool, (
        "romano_wolf must studentize every resample in its own scale, with no warning (contract: scale)."
    )
    for first, rest in ((1e300, tiny), (1.0, np.where(np.arange(39) % 2 == 0, 1e-300, np.nextafter(1e-300, 1.0)))):
        d = np.column_stack([np.r_[first, rest], rng.normal(0.0, 1.0, 40)])
        got = np.asarray(a8.romano_wolf(d, 0.05, 200, 2.0, SEED))
        assert got.shape == (2,) and got.dtype == bool, (
            "A bootstrap statistic too large for a float is +-inf, quietly: guard the overflow when the column mean "
            "is re-expressed in a resample's scale and when it is studentized (contract: romano_wolf, scale)."
        )
    m = rng.normal(0.0, 0.01, (40, 4))
    m[:, 1] = np.r_[np.full(10, 0.02), tiny[:30]]
    logits = np.asarray(a8.probability_of_backtest_overfitting(m, 4).logits)
    assert np.allclose(logits, cscv_logits(m, 4), rtol=0, atol=1e-10), (
        "CSCV must compute each subsample's Sharpe ratio in that subsample's own scale, with no warning "
        "(contract: scale)."
    )


def test_numpy_scalar_arguments_do_not_warn() -> None:
    must_raise(
        lambda: a8.sharpe_ratio_std(np.float64(1e200), 100, 0.0, 3.0),
        "sharpe_ratio_std whose variance bracket overflows for a NumPy scalar Sharpe ratio",
    )
    assert close(a8.probabilistic_sharpe_ratio(INST["returns"], np.float64(-1e308)), 1.0), (
        "A NumPy scalar benchmark must not warn: convert scalar arguments with float() before arithmetic "
        "(contract: scalars)."
    )


@pytest.mark.parametrize("k", [pytest.param(500, id="times-2^500"), pytest.param(-500, id="times-2^-500")])
def test_statistics_are_invariant_to_power_of_two_scaling(k: int) -> None:
    x, trials = INST["returns"], INST["trial_sharpes"]
    big = np.ldexp(x, k)
    for function in ("sharpe_ratio", "sample_skewness", "sample_kurtosis", "probabilistic_sharpe_ratio"):
        assert close(getattr(a8, function)(big), getattr(a8, function)(x), 1e-12), (
            f"{function}: multiplying the returns by 2**{k} must change nothing and warn nothing (contract: scale)."
        )
    assert close(a8.deflated_sharpe_ratio(big, trials), a8.deflated_sharpe_ratio(x, trials), 1e-12), (
        f"deflated_sharpe_ratio: multiplying the returns by 2**{k} must change nothing (contract: scale)."
    )
    d = INST["differentials"]
    signs = np.where(np.arange(d.shape[1]) % 2 == 0, k, -k)  # alternate columns up and down by 2**|k|
    assert np.array_equal(
        np.asarray(a8.romano_wolf(np.ldexp(d, signs), 0.05, 200, 10.0, SEED)),
        np.asarray(a8.romano_wolf(d, 0.05, 200, 10.0, SEED)),
    ), "romano_wolf: scaling each column by a power of two must leave every decision unchanged (contract: scale)."
    m, s = INST["performance"], INST["n_blocks"]
    scaled_m = np.ldexp(m, np.where(np.arange(m.shape[1]) % 2 == 0, k, -k))
    assert np.allclose(
        np.asarray(a8.probability_of_backtest_overfitting(scaled_m, s).logits),
        np.asarray(a8.probability_of_backtest_overfitting(m, s).logits),
        rtol=0,
        atol=1e-12,
    ), "PBO: CSCV ranks Sharpe ratios, so scaling a configuration by a power of two changes nothing (contract: scale)."


# ---------------------------------------------------------------- input validation


def _matrix_cases(function: Callable[[object], object], name: str) -> list[object]:
    return [
        pytest.param(
            lambda: function([0.01, 0.02, 0.03, 0.01]), f"{name} given a one-dimensional matrix", id=f"{name}-1d"
        ),
        pytest.param(
            lambda: function([[0.01, 0.02], [float("nan"), 0.01], [0.03, 0.02], [0.0, 0.01]]),
            f"{name} given a non-finite value",
            id=f"{name}-non-finite",
        ),
    ]


def _differentials() -> np.ndarray:
    return np.random.default_rng(SEED).normal(0.0, 1.0, (40, 3))


@pytest.mark.parametrize(
    ("call", "condition"),
    [
        pytest.param(
            lambda: a8.stationary_bootstrap_indices(50, 0.5, np.random.default_rng(SEED)),
            "stationary_bootstrap_indices with mean_block < 1",
            id="sb-mean-block-below-1",
        ),
        pytest.param(
            lambda: a8.stationary_bootstrap_indices(50, float("nan"), np.random.default_rng(SEED)),
            "stationary_bootstrap_indices with a non-finite mean_block",
            id="sb-mean-block-nan",
        ),
        pytest.param(
            lambda: a8.stationary_bootstrap_indices(0, 5.0, np.random.default_rng(SEED)),
            "stationary_bootstrap_indices with n_obs = 0",
            id="sb-n-obs-zero",
        ),
        pytest.param(
            lambda: a8.stationary_bootstrap_indices(2.5, 5.0, np.random.default_rng(SEED)),
            "stationary_bootstrap_indices with a non-integer n_obs",
            id="sb-n-obs-fractional",
        ),
        pytest.param(
            lambda: a8.stepdown_rejections([1.0, 2.0], np.zeros((10, 2)), 0.0),
            "stepdown_rejections with alpha = 0",
            id="stepdown-alpha-zero",
        ),
        pytest.param(
            lambda: a8.stepdown_rejections([1.0, 2.0], np.zeros((10, 3)), 0.05),
            "stepdown_rejections with t_boot columns that do not match t_obs",
            id="stepdown-shape",
        ),
        pytest.param(
            lambda: a8.stepdown_rejections([1.0, 2.0], np.zeros((0, 2)), 0.05),
            "stepdown_rejections with no bootstrap draws",
            id="stepdown-no-draws",
        ),
        pytest.param(
            lambda: a8.stepdown_rejections([1.0, float("nan")], np.zeros((10, 2)), 0.05),
            "stepdown_rejections with a non-finite statistic",
            id="stepdown-non-finite",
        ),
        pytest.param(
            lambda: a8.romano_wolf(_differentials(), 0.05, 0, 5.0, SEED),
            "romano_wolf with n_boot = 0",
            id="rw-n-boot-zero",
        ),
        pytest.param(
            lambda: a8.romano_wolf(_differentials(), 0.05, 12.5, 5.0, SEED),
            "romano_wolf with a non-integer n_boot",
            id="rw-n-boot-fractional",
        ),
        pytest.param(
            lambda: a8.romano_wolf(_differentials(), 1.5, 20, 5.0, SEED),
            "romano_wolf with alpha outside (0, 1)",
            id="rw-alpha",
        ),
        pytest.param(
            lambda: a8.romano_wolf(_differentials(), 0.05, 20, 0.5, SEED),
            "romano_wolf with mean_block < 1",
            id="rw-mean-block",
        ),
        pytest.param(
            lambda: a8.sharpe_ratio_std(0.1, 1, 0.0, 3.0), "sharpe_ratio_std with n_obs = 1", id="se-n-obs-one"
        ),
        pytest.param(
            lambda: a8.sharpe_ratio_std(float("nan"), 100, 0.0, 3.0),
            "sharpe_ratio_std with a non-finite Sharpe ratio",
            id="se-non-finite",
        ),
        pytest.param(
            lambda: a8.sharpe_ratio_std(1e200, 100, 0.0, 3.0),
            "sharpe_ratio_std with a variance bracket that overflows",
            id="se-overflow",
        ),
        pytest.param(
            lambda: a8.sharpe_ratio_std(2.0, 100, 0.5, 1.0),  # 1 - 0.5 * 2 + 0 * 4 = 0 exactly
            "sharpe_ratio_std with a zero variance bracket (it must be positive)",
            id="se-zero-bracket",
        ),
        pytest.param(
            lambda: a8.probabilistic_sharpe_ratio(INST["returns"], float("nan")),
            "probabilistic_sharpe_ratio with a non-finite benchmark",
            id="psr-benchmark-nan",
        ),
        pytest.param(
            lambda: a8.expected_max_sharpe(10, 1.0, float("nan")),
            "expected_max_sharpe with a non-finite sr_mean",
            id="ems-sr-mean-nan",
        ),
        pytest.param(
            lambda: a8.expected_max_sharpe(10, float("inf")),
            "expected_max_sharpe with a non-finite sr_variance",
            id="ems-sr-variance-inf",
        ),
        pytest.param(
            lambda: a8.deflated_sharpe_ratio(INST["returns"], [0.05]),
            "deflated_sharpe_ratio with one trial Sharpe ratio",
            id="dsr-one-trial",
        ),
        pytest.param(
            lambda: a8.deflated_sharpe_ratio(INST["returns"], [0.05, float("nan")]),
            "deflated_sharpe_ratio with a non-finite trial Sharpe ratio",
            id="dsr-non-finite",
        ),
        pytest.param(
            lambda: a8.deflated_sharpe_ratio(INST["returns"], [1e200, -1e200]),
            "deflated_sharpe_ratio with trial Sharpe ratios whose variance exceeds the largest float",
            id="dsr-variance-overflow",
        ),
        pytest.param(
            lambda: a8.deflated_sharpe_ratio(INST["returns"], INST["trial_sharpes"], 0),
            "deflated_sharpe_ratio with n_trials = 0",
            id="dsr-n-trials-zero",
        ),
        *_matrix_cases(lambda m: a8.romano_wolf(m, 0.05, 20, 2.0, SEED), "romano_wolf"),
        *_matrix_cases(lambda m: a8.probability_of_backtest_overfitting(m, 2), "probability_of_backtest_overfitting"),
        *_matrix_cases(lambda m: a8.TrialSet(m, 0, 252), "TrialSet"),
        pytest.param(
            lambda: a8.TrialSet(np.random.default_rng(0).normal(size=(1, 4)), 0, 252),
            "TrialSet with one period",
            id="trialset-one-period",
        ),
        pytest.param(
            lambda: a8.TrialSet(np.random.default_rng(0).normal(size=(50, 1)), 0, 252),
            "TrialSet with one trial",
            id="trialset-one-trial",
        ),
        pytest.param(
            lambda: a8.TrialSet(np.random.default_rng(0).normal(size=(50, 4)), 0, 0),
            "TrialSet with periods_per_year = 0",
            id="trialset-periods-per-year",
        ),
        pytest.param(
            lambda: a8.integrity_report(
                a8.TrialSet(np.random.default_rng(0).normal(size=(50, 4)), 0, 252), q=0.0, n_blocks=4, n_boot=20
            ),
            "integrity_report with q = 0",
            id="report-q-zero",
        ),
        # Every non-finite value an argument can carry, NaN and infinity alike.
        pytest.param(
            lambda: a8.benjamini_hochberg([0.1, float("nan")], 0.05),
            "benjamini_hochberg given a NaN p-value",
            id="bh-p-nan",
        ),
        pytest.param(
            lambda: a8.probabilistic_sharpe_ratio(INST["returns"], float("inf")),
            "probabilistic_sharpe_ratio with an infinite benchmark",
            id="psr-benchmark-inf",
        ),
        pytest.param(
            lambda: a8.sharpe_ratio([0.01, float("inf"), 0.02]),
            "sharpe_ratio given an infinite return",
            id="series-inf",
        ),
        pytest.param(
            lambda: a8.expected_max_sharpe(10, float("nan")),
            "expected_max_sharpe with a NaN sr_variance",
            id="ems-sr-variance-nan",
        ),
        pytest.param(
            lambda: a8.expected_max_sharpe(10, 1.0, float("inf")),
            "expected_max_sharpe with an infinite sr_mean",
            id="ems-sr-mean-inf",
        ),
        pytest.param(
            lambda: a8.deflated_sharpe_ratio(INST["returns"], [0.05, float("inf")]),
            "deflated_sharpe_ratio with an infinite trial Sharpe ratio",
            id="dsr-trial-inf",
        ),
        pytest.param(
            lambda: a8.stationary_bootstrap_indices(50, float("inf"), np.random.default_rng(SEED)),
            "stationary_bootstrap_indices with an infinite mean_block",
            id="sb-mean-block-inf",
        ),
        pytest.param(
            lambda: a8.stepdown_rejections([1.0, 2.0], np.full((10, 2), float("inf")), 0.05),
            "stepdown_rejections with an infinite bootstrap statistic",
            id="stepdown-boot-inf",
        ),
        pytest.param(
            lambda: a8.romano_wolf(np.where(np.eye(40, 3, dtype=bool), np.inf, _differentials()), 0.05, 20, 5.0, SEED),
            "romano_wolf given an infinite differential",
            id="rw-inf",
        ),
        # Integer arguments: inf and fractional values are not integers (contract: scalars).
        pytest.param(
            lambda: a8.sharpe_ratio_std(0.1, float("inf"), 0.0, 3.0),
            "sharpe_ratio_std with an infinite n_obs",
            id="se-n-obs-inf",
        ),
        pytest.param(
            lambda: a8.stationary_bootstrap_indices(float("inf"), 5.0, np.random.default_rng(SEED)),
            "stationary_bootstrap_indices with an infinite n_obs",
            id="sb-n-obs-inf",
        ),
        pytest.param(
            lambda: a8.romano_wolf(_differentials(), 0.05, float("inf"), 5.0, SEED),
            "romano_wolf with an infinite n_boot",
            id="rw-n-boot-inf",
        ),
        pytest.param(
            lambda: a8.probability_of_backtest_overfitting(_differentials(), float("inf")),
            "probability_of_backtest_overfitting with an infinite n_blocks",
            id="pbo-n-blocks-inf",
        ),
        pytest.param(
            lambda: a8.integrity_report(
                a8.TrialSet(np.random.default_rng(0).normal(size=(50, 4)), 0, 252), n_blocks=float("inf"), n_boot=20
            ),
            "integrity_report with an infinite n_blocks",
            id="report-n-blocks-inf",
        ),
        pytest.param(
            lambda: a8.TrialSet(np.random.default_rng(0).normal(size=(50, 4)), 1.5, 252),
            "TrialSet with a fractional selected",
            id="trialset-selected-fractional",
        ),
        pytest.param(
            lambda: a8.TrialSet(np.random.default_rng(0).normal(size=(50, 4)), 0, float("inf")),
            "TrialSet with an infinite periods_per_year",
            id="trialset-periods-per-year-inf",
        ),
    ],
)
def test_input_validation(call: Callable[[], object], condition: str) -> None:
    must_raise(call, condition)


@pytest.mark.parametrize("function", ["sample_skewness", "sample_kurtosis", "probabilistic_sharpe_ratio"])
@pytest.mark.parametrize(
    "bad",
    [
        pytest.param([[0.01, 0.02], [0.03, 0.01]], id="two-dimensional"),
        pytest.param([0.01, float("nan"), 0.02], id="non-finite"),
    ],
)
def test_series_functions_validate_their_input(function: str, bad: list) -> None:
    must_raise(lambda: getattr(a8, function)(bad), f"{function} given an invalid series")


def test_numpy_integer_and_float_arguments_are_accepted() -> None:
    # The contract's Scalars row: Python or NumPy numbers; an integer argument may be an integral float.
    n, var = INST["n_trials"], float(np.var(INST["trial_sharpes"], ddof=1))
    for as_given in (np.int64(n), np.float32(n), np.float64(n)):
        assert close(a8.expected_max_sharpe(as_given, var), expected_max(n, var)), (
            "An integer argument may be a NumPy integer or an integral float (contract: scalars)."
        )
    m, s = INST["performance"], INST["n_blocks"]
    assert close(
        a8.probability_of_backtest_overfitting(m, np.int64(s)).pbo, a8.probability_of_backtest_overfitting(m, s).pbo
    ), "probability_of_backtest_overfitting must accept a NumPy integer n_blocks (contract: scalars)."
    d = INST["differentials"]
    assert np.array_equal(
        np.asarray(a8.romano_wolf(d, 0.05, np.int64(50), 10.0, np.int64(SEED))),
        np.asarray(a8.romano_wolf(d, 0.05, 50, 10.0, SEED)),
    ), "romano_wolf must accept NumPy integers for n_boot and seed (contract: scalars)."
    trials = a8.TrialSet(m, np.argmax(m.mean(0) / m.std(0, ddof=1)), np.int64(252))
    assert isinstance(trials.selected, int), "TrialSet must accept a NumPy integer selected, as np.argmax returns."


@pytest.mark.parametrize(
    ("call", "condition"),
    [
        # from_backtest validates, never truncates
        pytest.param(
            lambda: a8.TrialSet.from_backtest(
                SimpleNamespace(
                    trial_returns=np.random.default_rng(0).normal(size=(50, 4)), selected=1.5, periods_per_year=252
                )
            ),
            "TrialSet.from_backtest with a fractional selected",
            id="from-backtest-selected-fractional",
        ),
        pytest.param(
            lambda: a8.TrialSet.from_backtest(
                SimpleNamespace(
                    trial_returns=np.random.default_rng(0).normal(size=(50, 4)),
                    selected=float("inf"),
                    periods_per_year=252,
                )
            ),
            "TrialSet.from_backtest with an infinite selected",
            id="from-backtest-selected-inf",
        ),
        pytest.param(
            lambda: a8.TrialSet.from_backtest(
                SimpleNamespace(
                    trial_returns=np.random.default_rng(0).normal(size=(50, 4)), selected=0, periods_per_year=251.5
                )
            ),
            "TrialSet.from_backtest with a fractional periods_per_year",
            id="from-backtest-ppy-fractional",
        ),
        # integers beyond the contract's bound
        pytest.param(
            lambda: a8.expected_max_sharpe(10**400, 1.0), "expected_max_sharpe with N >= 2**1000", id="ems-n-huge"
        ),
        pytest.param(
            lambda: a8.sharpe_ratio_std(0.1, 10**400, 0.0, 3.0),
            "sharpe_ratio_std with n_obs >= 2**1000",
            id="se-n-obs-huge",
        ),
        # integrality, not only finiteness
        pytest.param(
            lambda: a8.sharpe_ratio_std(0.1, 2.5, 0.0, 3.0),
            "sharpe_ratio_std with a fractional n_obs",
            id="se-n-obs-fractional",
        ),
        pytest.param(
            lambda: a8.TrialSet(np.random.default_rng(0).normal(size=(50, 4)), 0, 251.5),
            "TrialSet with a fractional periods_per_year",
            id="trialset-periods-per-year-fractional",
        ),
        # seed
        pytest.param(
            lambda: a8.romano_wolf(_differentials(), 0.05, 20, 5.0, 1.5),
            "romano_wolf with a fractional seed",
            id="rw-seed-fractional",
        ),
        pytest.param(
            lambda: a8.romano_wolf(_differentials(), 0.05, 20, 5.0, -1),
            "romano_wolf with a negative seed",
            id="rw-seed-negative",
        ),
    ],
)
def test_integer_argument_validation(call: Callable[[], object], condition: str) -> None:
    must_raise(call, condition)


def test_expected_max_sharpe_near_the_integer_bound() -> None:
    assert close(a8.expected_max_sharpe(2**999, 1.0), expected_max(2**999, 1.0)), (
        "expected_max_sharpe must work for every N below 2**1000 (contract)."
    )


# ---------------------------------------------------------------- integer arguments, extreme floats, report wiring


def test_integral_float_arguments_act_as_integers() -> None:
    d, m, s = INST["differentials"], INST["performance"], INST["n_blocks"]
    assert np.array_equal(
        np.asarray(a8.romano_wolf(d, 0.05, 50.0, 10.0, float(SEED))),
        np.asarray(a8.romano_wolf(d, 0.05, 50, 10.0, SEED)),
    ), "An integral float seed or n_boot is that integer: draw from np.random.default_rng(int(seed)) (contract)."
    assert np.array_equal(
        np.asarray(a8.probability_of_backtest_overfitting(m, float(s)).logits),
        np.asarray(a8.probability_of_backtest_overfitting(m, s).logits),
    ), "An integral float n_blocks is that integer: convert it before slicing and combining blocks (contract: scalars)."
    assert close(a8.sharpe_ratio_std(0.1, np.float32(100.0), 0.0, 3.0), math.sqrt(1.005 / 99), 1e-12), (
        "An integral NumPy float n_obs must not lower the precision of the standard error (contract: scalars)."
    )
    assert close(a8.sharpe_ratio_std(1e20, np.float32(100.0), 0.0, 3.0), math.sqrt((1.0 + 0.5e40) / 99)), (
        "A finite variance bracket must not overflow because n_obs is a NumPy float32 (contract: scalars)."
    )
    for seed in range(50):
        assert np.array_equal(
            np.asarray(a8.stationary_bootstrap_indices(1000, np.float16(3.0), np.random.default_rng(seed))),
            np.asarray(a8.stationary_bootstrap_indices(1000, 3.0, np.random.default_rng(seed))),
        ), "Convert a NumPy mean_block with float() before computing 1/mean_block (contract: scalars)."


@pytest.mark.parametrize(
    ("call", "condition"),
    [
        pytest.param(
            lambda: a8.expected_max_sharpe(2**1000, 1.0), "expected_max_sharpe with N = 2**1000", id="ems-n-bound"
        ),
        pytest.param(
            lambda: a8.sharpe_ratio_std(0.1, 2**1000, 0.0, 3.0),
            "sharpe_ratio_std with n_obs = 2**1000",
            id="se-n-bound",
        ),
        pytest.param(
            lambda: a8.expected_max_sharpe(1e305, 1.0),
            "expected_max_sharpe with an integral float N above 2**1000",
            id="ems-float-n-huge",
        ),
        pytest.param(
            lambda: a8.sharpe_ratio_std(0.1, 1e305, 0.0, 3.0),
            "sharpe_ratio_std with an integral float n_obs above 2**1000",
            id="se-float-n-huge",
        ),
    ],
)
def test_integer_bound_is_strict_for_ints_and_floats(call: Callable[[], object], condition: str) -> None:
    must_raise(call, condition)


def test_largest_floats() -> None:
    x = np.array([1e308, -1e308, 5e307, 2e307])  # the range exceeds the largest float; the largest |value| > 2**1023
    sr, _, g4 = moments(np.ldexp(x, -1024))  # exact
    assert close(a8.sharpe_ratio(x), sr) and close(a8.sample_kurtosis(x), g4), (
        "At the largest floats, test zero variance by comparing max and min (np.ptp overflows) and rescale with "
        "np.ldexp (2.0**1024 overflows) (contract: zero variance, scale)."
    )


def _rw_matrix() -> np.ndarray:
    z = np.random.default_rng(2026).standard_normal((60, 6))
    z = (z - z.mean(0)) / z.std(0, ddof=1)
    return 0.01 * (z + np.array([2.6, 2.3, 2.0, 1.7, 1.2, 0.5]) / np.sqrt(60))


def test_integrity_report_forwards_alpha_and_seed() -> None:
    m = _rw_matrix()  # borderline columns: the decisions depend on alpha and on the bootstrap draws
    trials = a8.TrialSet(m, 0, 252)
    for alpha, seed in ((0.05, 1), (0.25, 0)):
        report = a8.integrity_report(trials, alpha=alpha, n_blocks=6, n_boot=50, seed=seed)
        assert np.array_equal(
            np.asarray(report.romano_wolf_rejections), np.asarray(a8.romano_wolf(m, alpha, 50, 10.0, seed))
        ), "romano_wolf_rejections must use the report's alpha, n_boot, mean_block and seed (contract)."
    for mean_block in (2.0, 40.0):
        report = a8.integrity_report(trials, alpha=0.05, n_blocks=6, n_boot=50, mean_block=mean_block, seed=SEED)
        assert np.array_equal(
            np.asarray(report.romano_wolf_rejections), np.asarray(a8.romano_wolf(m, 0.05, 50, mean_block, SEED))
        ), "romano_wolf_rejections must use the report's mean_block (contract)."
    t_stats = m.mean(axis=0) / (m.std(axis=0, ddof=1) / math.sqrt(m.shape[0]))
    pvalues = np.array([1.0 - PHI.cdf(float(t)) for t in t_stats])
    for q in (0.01, 0.25):
        report = a8.integrity_report(trials, alpha=0.05, q=q, n_blocks=6, n_boot=50, seed=SEED)
        assert np.array_equal(np.asarray(report.bh_rejections), np.asarray(a8.benjamini_hochberg(pvalues, q))), (
            "bh_rejections must use the report's q, not alpha (contract)."
        )


def test_report_pvalues_use_the_sample_standard_deviation() -> None:
    z = np.random.default_rng(SEED).standard_normal((40, 3))
    z = (z - z.mean(0)) / z.std(0, ddof=1)
    trials = a8.TrialSet(0.01 * (z + 1.635 / math.sqrt(40)), 0, 12)  # every t-statistic is 1.635: p = 0.0510
    report = a8.integrity_report(trials, n_blocks=4, n_boot=50)
    assert not np.asarray(report.bh_rejections).any(), (
        "The one-sided p-values use t = mean / (sd / sqrt(T)) with the sample standard deviation (ddof=1); with "
        "ddof=0 every t-statistic here would be 1.656 and every p-value 0.049 (contract: integrity_report)."
    )


@pytest.mark.parametrize("k", [pytest.param(600, id="times-2^600"), pytest.param(-600, id="times-2^-600")])
def test_integrity_report_is_invariant_to_power_of_two_scaling(k: int) -> None:
    m, s = INST["performance"], INST["n_blocks"]
    base = a8.integrity_report(a8.TrialSet(m, 0, 252), n_blocks=s, n_boot=50, seed=SEED)
    big = a8.integrity_report(a8.TrialSet(np.ldexp(m, k), 0, 252), n_blocks=s, n_boot=50, seed=SEED)
    assert np.array_equal(np.asarray(big.bh_rejections), np.asarray(base.bh_rejections)) and close(big.dsr, base.dsr), (
        "integrity_report: scaling every trial by a power of two changes nothing and warns nothing; compute the "
        "trials' t-statistics in each trial's own scale (contract: scale)."
    )


def test_equal_trial_sharpe_ratios_are_valid() -> None:
    x = INST["returns"]
    assert a8.expected_max_sharpe(10, 0.0) == 0.0, "With zero trial variance the expected maximum is sr_mean."
    assert close(a8.deflated_sharpe_ratio(x, [0.05, 0.05, 0.05]), a8.probabilistic_sharpe_ratio(x, 0.0)), (
        "Equal trial Sharpe ratios have variance 0, so SR0 = 0 and the DSR is the PSR against 0: the zero-variance "
        "rule is for return series, not for trial_sharpes (contract: deflated_sharpe_ratio)."
    )
