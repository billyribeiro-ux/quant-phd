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
    z = (1 - GAMMA) * PHI.inv_cdf(1 - 1 / n) + GAMMA * PHI.inv_cdf(1 - 1 / (n * math.e))
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
    ):
        must_raise(lambda bad=bad: a8.expected_max_sharpe(*bad), f"expected_max_sharpe with {condition}")


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
