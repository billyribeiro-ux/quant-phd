"""CS6 Autograder Pytest Suite: Parallel Portfolio Monte Carlo VaR Engine.

Validates mathematical correctness, bit-for-bit parallel reproducibility,
exact serial reconciliation, and error handling.
"""

from __future__ import annotations

import math
import os
from typing import Any

import instance as inst_mod
import numpy as np
import pytest
import reference as sol_mod


@pytest.fixture
def seed() -> int:
    """Extract current seed from environment or default to 0."""
    return int(os.environ.get("QF_SEED", "0"))


@pytest.fixture
def instance(seed: int) -> dict[str, Any]:
    """Generate deterministic instance for current seed."""
    return inst_mod.make_instance(seed)


def test_instance_validity(instance: dict[str, Any]) -> None:
    """Verify instance invariants: positive spots, valid correlation matrix, positive paths."""
    n_assets = int(instance["n_assets"])
    s0 = np.asarray(instance["s0"], dtype=np.float64)
    vols = np.asarray(instance["volatilities"], dtype=np.float64)
    corr = np.asarray(instance["corr_matrix"], dtype=np.float64)

    assert len(s0) == n_assets
    assert np.all(s0 > 0.0), "Initial spot prices must be strictly positive"
    assert np.all(vols > 0.0), "Volatilities must be strictly positive"
    assert corr.shape == (n_assets, n_assets), "Correlation matrix must be n_assets x n_assets"
    assert np.allclose(corr, corr.T, atol=1e-5), "Correlation matrix must be symmetric"
    assert np.allclose(np.diag(corr), 1.0, atol=1e-5), "Correlation diagonals must equal 1.0"

    eigenvalues = np.linalg.eigvalsh(corr)
    assert np.all(eigenvalues > 1e-4), "Correlation matrix must be strictly positive definite"


def test_cholesky_factor(instance: dict[str, Any]) -> None:
    """Verify Cholesky decomposition L is lower triangular and satisfies L @ L.T = corr."""
    corr = np.asarray(instance["corr_matrix"], dtype=np.float64)
    l_mat = sol_mod.cholesky_factor(instance["corr_matrix"])

    assert l_mat.shape == corr.shape
    assert np.allclose(np.triu(l_mat, k=1), 0.0), "Cholesky factor must be strictly lower triangular"
    reconstructed = l_mat @ l_mat.T
    assert np.allclose(reconstructed, corr, atol=1e-5), "Cholesky product L @ L.T must reconstruct correlation matrix"


def test_reproducible_stream_independence(instance: dict[str, Any]) -> None:
    """Verify counter-based RNG streams guarantee chunking invariance and bit-for-bit identity."""
    # Chunk generation of 40 paths in two parts vs single call
    chunk_a = sol_mod.simulate_paths_chunk(instance, start_idx=0, count=20)
    chunk_b = sol_mod.simulate_paths_chunk(instance, start_idx=20, count=20)
    combined = np.vstack([chunk_a, chunk_b])

    single_pass = sol_mod.simulate_paths_chunk(instance, start_idx=0, count=40)

    assert single_pass.shape == (40, int(instance["n_assets"]))
    assert np.array_equal(combined, single_pass), (
        "Partitioned path generation must equal contiguous single-pass generation bit-for-bit."
    )


def test_serial_simulation_properties(instance: dict[str, Any]) -> None:
    """Verify serial simulation outputs, loss dimension, and the ES >= VaR tail inequality."""
    res = sol_mod.run_serial_simulation(instance)
    n_paths = int(instance["n_paths"])
    losses = np.asarray(res["losses"], dtype=np.float64)

    assert losses.shape == (n_paths,), f"Losses array must have length n_paths ({n_paths})"
    assert np.all(np.isfinite(losses)), "Losses array must contain only finite numbers"

    var_val = float(res["var"])
    es_val = float(res["es"])

    assert np.isfinite(var_val), "VaR must be a finite float"
    assert np.isfinite(es_val), "Expected Shortfall must be a finite float"
    assert es_val >= var_val - 1e-9, f"Expected Shortfall ({es_val}) must be >= VaR ({var_val})"


def test_parallel_serial_exact_reconciliation(instance: dict[str, Any]) -> None:
    """Verify that parallel simulation reconciles exactly with serial simulation."""
    serial_res = sol_mod.run_serial_simulation(instance)
    parallel_res = sol_mod.run_parallel_simulation(instance, n_workers=4)

    rec = sol_mod.reconcile_runs(serial_res, parallel_res, tol=1e-7)

    assert rec["reconciled"] is True, "Serial and parallel simulation results failed reconciliation"
    assert rec["max_loss_diff"] <= 1e-7, (
        f"Maximum loss difference {rec['max_loss_diff']} exceeds floating-point tolerance"
    )
    assert rec["var_diff"] <= 1e-7, f"VaR discrepancy {rec['var_diff']} exceeds tolerance"
    assert rec["es_diff"] <= 1e-7, f"ES discrepancy {rec['es_diff']} exceeds tolerance"


def test_alpha_monotonicity(instance: dict[str, Any]) -> None:
    """Verify that higher confidence level alpha yields equal or higher VaR."""
    inst_95 = dict(instance)
    inst_95["alpha"] = 0.95
    res_95 = sol_mod.run_serial_simulation(inst_95)

    inst_99 = dict(instance)
    inst_99["alpha"] = 0.99
    res_99 = sol_mod.run_serial_simulation(inst_99)

    assert res_99["var"] >= res_95["var"] - 1e-9, f"99% VaR ({res_99['var']}) must be >= 95% VaR ({res_95['var']})"


def test_black_scholes_price_parity() -> None:
    """Verify Black-Scholes pricing satisfies no-arbitrage put-call parity."""
    spot = 100.0
    strike = 100.0
    expiry = 1.0
    rate = 0.05
    vol = 0.20

    call = float(sol_mod.black_scholes_price(spot, strike, expiry, rate, vol, is_call=True))
    put = float(sol_mod.black_scholes_price(spot, strike, expiry, rate, vol, is_call=False))

    expected_diff = spot - strike * math.exp(-rate * expiry)
    assert math.isclose(call - put, expected_diff, abs_tol=1e-5), (
        f"Put-call parity violation: Call - Put ({call - put}) != S - K*exp(-rT) ({expected_diff})"
    )


def test_invalid_inputs(instance: dict[str, Any]) -> None:
    """Verify that solver rejects invalid inputs with ValueError."""
    with pytest.raises(ValueError):
        bad_inst = dict(instance)
        bad_inst["n_paths"] = 0
        sol_mod.run_serial_simulation(bad_inst)

    with pytest.raises(ValueError):
        bad_inst = dict(instance)
        bad_inst["n_paths"] = -50
        sol_mod.run_serial_simulation(bad_inst)

    with pytest.raises(ValueError):
        sol_mod.compute_var_es(np.array([1.0, 2.0]), alpha=1.5)

    with pytest.raises(ValueError):
        sol_mod.compute_var_es(np.array([1.0, 2.0]), alpha=-0.1)

    with pytest.raises(ValueError):
        sol_mod.run_parallel_simulation(instance, n_workers=0)


def test_benchmark_scaling(instance: dict[str, Any]) -> None:
    """Verify scaling benchmark output structure and single-worker baseline identity."""
    # Test on smaller path count for speed
    bench_inst = dict(instance)
    bench_inst["n_paths"] = 1000

    results = sol_mod.benchmark_scaling(bench_inst, worker_counts=[1, 2])

    assert 1 in results
    assert 2 in results
    assert results[1]["speedup"] == 1.0
    assert results[1]["efficiency"] == 1.0
    assert results[2]["runtime_s"] > 0.0
    assert results[2]["speedup"] > 0.0
    assert results[2]["efficiency"] > 0.0
