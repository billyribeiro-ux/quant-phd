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
REFERENCE = ROOT / "course" / "modules" / "S" / "S7" / "grader" / "reference.py"


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
    result = subprocess.run(
        [exe, "--input-type=module", "-e", source], capture_output=True, text=True, check=False, cwd=ROOT
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
