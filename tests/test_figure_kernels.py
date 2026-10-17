"""The browser's figure kernels agree with Python on the same inputs.

Figures compute their numbers live in JavaScript (course/assets/js/stats.js and
multitest.js). A figure that disagreed with the lesson or with the graded A8 API
would teach the wrong thing, so each kernel is run under Node on fixed inputs and
compared with the S7 reference solution (the contract's executable form) or with
Python's standard library.
"""

from __future__ import annotations

import functools
import importlib.util
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path
from statistics import NormalDist
from types import ModuleType
from typing import Any

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parent.parent
JS = ROOT / "course" / "assets" / "js"
S7 = ROOT / "course" / "modules" / "S" / "S7"
REFERENCE = S7 / "grader" / "reference.py"


@functools.cache
def reference() -> ModuleType:
    spec = importlib.util.spec_from_file_location("s7_reference", REFERENCE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses resolve their module while the class is built
    spec.loader.exec_module(module)
    return module


def node(script: str, payload: object) -> Any:
    """Run an ES-module script under Node with `payload` bound to the global INPUT; return its JSON output."""
    exe = shutil.which("node")
    assert exe, "Node.js is required for the figure-kernel tests (CI installs it)"
    source = f"globalThis.INPUT = {json.dumps(payload)};\n{script}"
    # The script goes on stdin: inputs can exceed the operating system's argument-length limit.
    result = subprocess.run(
        [exe, "--input-type=module"], input=source, capture_output=True, text=True, check=False, cwd=ROOT
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


IMPORTS = (
    f'import * as stats from "{(JS / "stats.js").as_uri()}";\nimport * as mt from "{(JS / "multitest.js").as_uri()}";\n'
)


def test_normal_distribution_matches_the_standard_library() -> None:
    xs = [round(-12 + 0.05 * i, 2) for i in range(481)]
    ps = [1e-12, 1e-9, 1e-6, 0.001, 0.025, 0.1, 0.3, 0.5, 0.7, 0.9, 0.975, 0.999, 1 - 1e-9]
    out = node(
        IMPORTS + "console.log(JSON.stringify({cdf: INPUT.xs.map(stats.normCdf), sf: INPUT.xs.map(stats.normSf),"
        " pdf: INPUT.xs.map(stats.normPdf), ppf: INPUT.ps.map(stats.normPpf)}));",
        {"xs": xs, "ps": ps},
    )
    phi = NormalDist()
    for x, cdf, sf, pdf in zip(xs, out["cdf"], out["sf"], out["pdf"], strict=True):
        assert abs(cdf - phi.cdf(x)) < 1e-15, x
        tail = 0.5 * math.erfc(x / math.sqrt(2))
        assert abs(sf - tail) <= 1e-8 * tail + 1e-300, x
        assert abs(pdf - phi.pdf(x)) < 1e-16, x
    for p, q in zip(ps, out["ppf"], strict=True):
        assert abs(q - phi.inv_cdf(p)) <= 1e-12 * max(1.0, abs(q)), p


def test_expected_maximum_matches_integration_and_the_reference_approximation() -> None:
    ns = [1, 2, 5, 10, 40, 100, 1000, 10000]
    out = node(
        IMPORTS + "console.log(JSON.stringify({exact: INPUT.map(stats.expectedMaxNormal),"
        " approx: INPUT.filter((n) => n >= 2).map(stats.approxExpectedMax)}));",
        ns,
    )
    grid = np.linspace(-9.0, 10.0, 200001)
    dense_cdf = 0.5 * np.vectorize(math.erfc)(-grid / math.sqrt(2))
    pdf = np.exp(-0.5 * grid**2) / math.sqrt(2 * math.pi)
    ref = reference()
    for n, exact in zip(ns, out["exact"], strict=True):
        integrand = grid * n * pdf * dense_cdf ** (n - 1)
        assert abs(exact - float(np.trapezoid(integrand, grid))) < 1e-7, n
    assert abs(out["exact"][0]) < 1e-12, "the expected maximum of one standard normal is 0"
    for n, approx in zip([n for n in ns if n >= 2], out["approx"], strict=True):
        assert abs(approx - ref.expected_max_sharpe(n, 1.0, 0.0)) < 1e-12, n


@pytest.mark.parametrize("seed", range(5))
def test_bh_by_holm_and_bonferroni_match_python(seed: int) -> None:
    rng = np.random.default_rng([31, seed])
    m = 40
    z = rng.standard_normal(m) + np.where(np.arange(m) < 12, 3.0, 0.0)
    p = [float(1 - NormalDist().cdf(float(v))) for v in z]
    p[5] = p[6]  # a tie, which every procedure must handle by its definition
    out = node(
        IMPORTS + "const [p, a] = [INPUT.p, INPUT.a]; console.log(JSON.stringify({bh: mt.benjaminiHochberg(p, a).mask,"
        " by: mt.benjaminiYekutieli(p, a).mask, holm: mt.holm(p, a).mask, bonf: mt.bonferroni(p, a)}));",
        {"p": p, "a": 0.1},
    )
    ref = reference()
    assert out["bh"] == ref.benjamini_hochberg(p, 0.1).tolist()
    c = sum(1 / j for j in range(1, m + 1))
    assert out["by"] == ref.benjamini_hochberg(p, 0.1 / c).tolist()
    order = np.argsort(p, kind="stable")
    holm = np.zeros(m, dtype=bool)
    for j, i in enumerate(order):
        if p[i] > 0.1 / (m - j):
            break
        holm[i] = True
    assert out["holm"] == holm.tolist()
    assert out["bonf"] == [v <= 0.1 / m for v in p]


@pytest.mark.parametrize("seed", range(5))
def test_stepdown_matches_the_reference(seed: int) -> None:
    rng = np.random.default_rng([37, seed])
    k, b = 12, 499
    t_boot = rng.standard_normal((b, k)) * 0.8 + rng.standard_normal((b, 1)) * 0.6
    t_obs = rng.standard_normal(k) + np.where(np.arange(k) < 4, 3.5, 0.0)
    out = node(
        IMPORTS + "console.log(JSON.stringify(mt.stepdown(INPUT.t, INPUT.boot, 0.05)));",
        {"t": t_obs.tolist(), "boot": t_boot.tolist()},
    )
    assert out["mask"] == reference().stepdown_rejections(t_obs, t_boot, 0.05).tolist()
    assert out["steps"][-1]["rejected"] == [] or len(out["steps"][-1]["active"]) == len(out["steps"][-1]["rejected"])


@pytest.mark.parametrize(("seed", "periods", "blocks"), [(0, 96, 8), (1, 101, 6), (2, 64, 4), (3, 250, 10)])
def test_cscv_matches_the_reference(seed: int, periods: int, blocks: int) -> None:
    rng = np.random.default_rng([41, seed])
    n = 7
    performance = rng.standard_normal((periods, n)) * 0.01 + np.where(np.arange(n) == 2, 0.002, 0.0)
    performance[:, 5] = np.round(performance[:, 5], 3)  # coarse values make out-of-sample ties possible
    out = node(
        IMPORTS + "const r = mt.cscv(INPUT.m, INPUT.s); console.log(JSON.stringify({pbo: r.pbo, logits: r.logits}));",
        {"m": performance.tolist(), "s": blocks},
    )
    expected = reference().probability_of_backtest_overfitting(performance, blocks)
    assert out["pbo"] == pytest.approx(expected.pbo, abs=1e-15)
    np.testing.assert_allclose(out["logits"], expected.logits, rtol=0, atol=1e-12)


def test_stationary_bootstrap_follows_the_index_chain_and_the_generator_is_deterministic() -> None:
    out = node(
        IMPORTS + "const g = stats.rng(INPUT.seed); const r = mt.stationaryBootstrap(INPUT.n, INPUT.b, g);"
        " const a = stats.rng(9), b = stats.rng(9), c = stats.rng(10);"
        " const z = stats.rng(3); const draws = Array.from({length: 200000}, () => z.normal());"
        " console.log(JSON.stringify({i: Array.from(r.indices), s: r.starts,"
        " same: [a.uniform(), a.uniform()].join() === [b.uniform(), b.uniform()].join(),"
        " differ: stats.rng(9).uniform() !== c.uniform(), m: stats.mean(draws), sd: stats.sd(draws)}));",
        {"seed": 5, "n": 200000, "b": 8.0},
    )
    idx, starts = out["i"], out["s"]
    n = len(idx)
    assert all(starts[t] or idx[t] == (idx[t - 1] + 1) % n for t in range(1, n)), "a block continues by +1 mod n"
    share = sum(starts[1:]) / (n - 1)
    assert abs(share - 1 / 8) < 4 * math.sqrt((1 / 8) * (7 / 8) / (n - 1)), "new blocks start with probability 1/b"
    counts = np.bincount(np.asarray(idx) * 10 // n, minlength=10)
    assert counts.min() > 0.9 * n / 10, "indices are spread uniformly over the sample"
    assert out["same"] and out["differ"], "the generator is deterministic per seed and differs across seeds"
    assert abs(out["m"]) < 0.01 and abs(out["sd"] - 1) < 0.01, "normal draws have mean 0 and variance 1"


def test_forking_paths_rate_matches_closed_forms_and_simulation() -> None:
    cases: list[tuple[int, float]] = [(1, 0.5), (10, 0.0), (10, 0.5), (10, 0.95), (40, 0.8), (5, 0.999)]
    out = node(
        f'import {{ falsePositiveRate }} from "{(S7 / "figures-L06.js").as_uri()}";\n'
        "console.log(JSON.stringify(INPUT.map(([k, r]) => falsePositiveRate(k, r, 0.05))));",
        cases,
    )
    assert out[0] == pytest.approx(0.05, abs=1e-9), "one analysis is a single test at its nominal level"
    assert out[1] == pytest.approx(1 - 0.95**10, abs=1e-12), "independent analyses: 1 - (1 - alpha)^K"
    rng = np.random.default_rng(43)
    crit = NormalDist().inv_cdf(0.975)
    draws = 400_000
    for (k, rho), rate in zip(cases[2:], out[2:], strict=True):
        common = math.sqrt(rho) * rng.standard_normal((draws, 1))
        z = common + math.sqrt(1 - rho) * rng.standard_normal((draws, k))
        simulated = float(np.mean(np.abs(z).max(axis=1) > crit))
        assert abs(rate - simulated) < 4 * math.sqrt(rate * (1 - rate) / draws), (k, rho)
        assert 0.05 <= rate <= min(1.0, k * 0.05), "Proposition 3.2's bounds"


def test_dsr_explorer_matches_the_reference_and_example_3_2() -> None:
    out = node(
        f'import {{ benchmarkSharpe, sharpeStdError }} from "{(S7 / "figures-L07.js").as_uri()}";\n'
        "console.log(JSON.stringify({sr0: INPUT.map(([n, s]) => benchmarkSharpe(n, s)),"
        " se: sharpeStdError(0.09, 756, -1.5, 8)}));",
        [[1, 0.03], [2, 0.03], [40, 0.03], [1000, 0.01]],
    )
    ref = reference()
    for (n, sd), sr0 in zip([[1, 0.03], [2, 0.03], [40, 0.03], [1000, 0.01]], out["sr0"], strict=True):
        assert sr0 == pytest.approx(ref.expected_max_sharpe(n, sd**2, 0.0), abs=1e-15)
    assert out["se"] == pytest.approx(ref.sharpe_ratio_std(0.09, 756, -1.5, 8.0), rel=1e-14)
    assert round(out["sr0"][2], 4) == 0.0657 and round(out["se"], 4) == 0.0390, "Example 3.2's printed values"


@pytest.mark.parametrize(("seed", "periods", "constant_column"), [(0, 120, False), (1, 250, False), (2, 6, True)])
def test_studentized_bootstrap_reproduces_the_reference_romano_wolf(
    seed: int, periods: int, constant_column: bool
) -> None:
    ref = reference()
    rng = np.random.default_rng([47, seed])
    d = rng.standard_normal((periods, 5)) + 0.25 * rng.standard_normal((periods, 1)) + np.array([0.3, 0.1, 0, 0, -0.2])
    if constant_column:
        d[:, 0] = 0.0
        d[-1, 0] = 1.0  # a resample that misses the last period is constant in column 0
    n_boot, mean_block = 199, 2.0
    draws = np.random.default_rng(seed)  # the same index vectors romano_wolf draws
    indices = [ref.stationary_bootstrap_indices(periods, mean_block, draws).tolist() for _ in range(n_boot)]
    separate = [
        [ref.stationary_bootstrap_indices(periods, mean_block, draws).tolist() for _ in range(5)] for _ in range(20)
    ]
    out = node(
        IMPORTS + "const j = mt.studentizedBootstrap(INPUT.d, INPUT.idx, true);"
        " const s = mt.studentizedBootstrap(INPUT.d, INPUT.sep, false);"
        " console.log(JSON.stringify({t: j.t, boot: j.boot, mask: mt.stepdown(j.t, j.boot, 0.1).mask, sep: s.boot,"
        " corr: mt.correlation(INPUT.d.map((r) => r[0]), INPUT.d.map((r) => r[1]))}));",
        {"d": d.tolist(), "idx": indices, "sep": separate},
    )
    mean, sd = d.mean(0), d.std(0, ddof=1)
    np.testing.assert_allclose(out["t"], mean / (sd / math.sqrt(periods)), rtol=1e-12)
    expected = []
    for idx in indices:
        sample = d[idx]
        sd_b = sample.std(0, ddof=1)
        sd_b = np.where(sd_b == 0.0, sd, sd_b)
        expected.append((sample.mean(0) - mean) / (sd_b / math.sqrt(periods)))
    np.testing.assert_allclose(out["boot"], expected, rtol=1e-10, atol=1e-12)
    assert out["mask"] == ref.romano_wolf(d, 0.1, n_boot, mean_block, seed).tolist(), "same decisions as romano_wolf"
    cols = np.array([[d[draw[k], k] for k in range(5)] for draw in separate])  # (B, K, T)
    sep_sd = np.where(cols.std(2, ddof=1) == 0.0, sd, cols.std(2, ddof=1))
    np.testing.assert_allclose(
        out["sep"], (cols.mean(2) - mean) / (sep_sd / math.sqrt(periods)), rtol=1e-10, atol=1e-12
    )
    assert out["corr"] == pytest.approx(float(np.corrcoef(d[:, 0], d[:, 1])[0, 1]), abs=1e-12)


def test_new_kernels_match_python() -> None:
    rng = np.random.default_rng(53)
    p = rng.random(500)
    x = np.cumsum(rng.standard_normal(64)) * 0.1 + rng.standard_normal(64)
    out = node(
        IMPORTS + "const c = mt.circularAutocovariance(INPUT.x);"
        " console.log(JSON.stringify({pi0: [0.3, 0.5, 0.8].map((l) => mt.storeyPi0(INPUT.p, l)), c,"
        " v: [1, 2.5, 7, 64].map((b) => mt.bootstrapVarianceOfMean(c, b))}));",
        {"p": p.tolist(), "x": x.tolist()},
    )
    for lam, got in zip([0.3, 0.5, 0.8], out["pi0"], strict=True):
        assert got == pytest.approx(float(np.mean(p > lam)) / (1 - lam), rel=1e-12)
    n = x.size
    dev = x - x.mean()
    c = np.array([np.mean(dev * np.roll(dev, -h)) for h in range(n)])
    np.testing.assert_allclose(out["c"], c, rtol=1e-12, atol=1e-14)
    for b, got in zip([1, 2.5, 7, 64], out["v"], strict=True):
        h = np.arange(1, n)
        expected = (c[0] + 2 * np.sum((1 - h / n) * (1 - 1 / b) ** h * c[1:])) / n  # L04 formula (2)
        assert got == pytest.approx(float(expected), rel=1e-12)
    # Formula (2) is the exact stationary-bootstrap variance: compare with resampling by the reference.
    ref = reference()
    draws = np.random.default_rng(5)
    means = [x[ref.stationary_bootstrap_indices(n, 7.0, draws)].mean() for _ in range(40_000)]
    assert float(np.var(means)) == pytest.approx(out["v"][2], rel=0.03)


def test_reality_check_and_spa_kernel_matches_lab_3() -> None:
    rng = np.random.default_rng(59)
    t_obs, k = 300, 30
    d = rng.standard_normal((t_obs, k)) + np.where(np.arange(k) == 0, 0.15, np.where(np.arange(k) >= 10, -0.25, 0.0))
    idx = np.random.default_rng(61).integers(0, t_obs, size=(400, t_obs))
    boot = d[idx].mean(axis=1)
    means, sd = d.mean(0), d.std(0, ddof=1)
    out = node(
        IMPORTS + "const r = mt.realityCheckSpa(INPUT.m, INPUT.s, INPUT.b, INPUT.t, INPUT.k);"
        " console.log(JSON.stringify({v: r.v, t: r.tObs, rc: r.pRc, spa: r.pSpa, n: r.recentred}));",
        {"m": means.tolist(), "s": sd.tolist(), "b": boot.tolist(), "t": t_obs, "k": k},
    )
    # L04 Lab 3's formulas, verbatim.
    v = np.sqrt(t_obs) * means.max()
    p_rc = np.mean((np.sqrt(t_obs) * (boot - means)).max(axis=1) >= v)
    threshold = sd * np.sqrt(2.0 * np.log(np.log(t_obs)) / t_obs)
    centre = np.where(means <= -threshold, means, 0.0)
    t_max = max(float((np.sqrt(t_obs) * means / sd).max()), 0.0)
    t_star = np.maximum((np.sqrt(t_obs) * (boot - means + centre) / sd).max(axis=1), 0.0)
    assert out["v"] == pytest.approx(float(v), rel=1e-12) and out["t"] == pytest.approx(t_max, rel=1e-12)
    assert out["rc"] == pytest.approx(float(p_rc), abs=1e-15)
    assert out["spa"] == pytest.approx(float(np.mean(t_star >= t_max)), abs=1e-15)
    assert out["n"] == int(np.sum(centre != 0))


def ranks_within(values: list[float], index: int, tolerance: float) -> bool:
    """Whether values[index] lies within `tolerance` ranks of the median of `values`."""
    rank = sum(v < values[index] for v in values)
    return abs(rank - (len(values) - 1) / 2) <= tolerance


def test_simulated_figure_defaults_are_median_draws() -> None:
    l03, l04, l05, l08 = (
        f'"{(S7 / f).as_uri()}"' for f in ("figures-L03.js", "figures-L04.js", "figures-L05.js", "figures-L08.js")
    )
    out = node(
        f"import * as f3 from {l03}; import * as f4 from {l04}; import * as f5 from {l05}; import * as f8 from {l08};\n"
        + IMPORTS
        + "const seeds = (a, b) => Array.from({length: b - a + 1}, (_, i) => a + i);\n"
        "const pi0 = seeds(1, 200).map((s) => mt.storeyPi0(f3.pvalueSample(s), 0.5));\n"
        "const blocks = seeds(1, 200).map((s) => f4.blockDraw(s, 4).blocks.length);\n"
        "const peaks = seeds(1, 200).map((s) => f4.varianceCurve(f4.ar1Autocovariance(s, 0.5), 0.5)"
        ".reduce((a, p) => (p[1] > a[1] ? p : a)));\n"
        "const rc = seeds(2000, 2029).map((s) => { const u = f4.universe(s);"
        " const a = mt.realityCheckSpa(u.means, u.sds, u.bootMeans, 500, 10);"
        " return [a.v, a.pRc, mt.realityCheckSpa(u.means, u.sds, u.bootMeans, 500, 110).pRc]; });\n"
        "const stepm = seeds(0, 299).map((s) => { const r = f5.study(s).result;"
        " return [r.steps[0].rejected.length, r.mask.filter(Boolean).length]; });\n"
        "const pbo = seeds(1, 200).map((s) => mt.cscv(f8.simulate(s, false), 8).pbo);\n"
        "console.log(JSON.stringify({pi0, blocks, peaks, rc, stepm, pbo, d: [f3.PVALUE_DEFAULT_SEED,"
        " f4.DEFAULT_BLOCK_SEED, f4.DEFAULT_AR_SEED, f4.DEFAULT_RC_SEED, f5.DEFAULT_SEED, f8.DEFAULT_CSCV_SEED]}));",
        {},
    )
    d3, dblock, dar, drc, d5, d8 = out["d"]
    assert out["pi0"][d3 - 1] == sorted(out["pi0"])[99], "L03 histogram: the default estimate is the median"
    assert out["blocks"][dblock - 1] == sorted(out["blocks"])[99], "L04 blocks: the default block count is the median"
    peak_b = [p[0] for p in out["peaks"]]
    peak_h = [p[1] for p in out["peaks"]]
    assert ranks_within(peak_b, dar - 1, 3) and ranks_within(peak_h, dar - 1, 3), "L04 variance: a median peak"
    for j in range(3):
        assert ranks_within([r[j] for r in out["rc"]], drc - 2000, 3), f"L04 RC/SPA statistic {j} near its median"
    single, total = ([s[j] for s in out["stepm"]] for j in (0, 1))
    assert single[d5] == sorted(single)[150] and total[d5] == sorted(total)[150], "L05 StepM: a median study"
    assert ranks_within(out["pbo"], d8 - 1, 3), "L08 CSCV: a median history (PBO with no edge)"
