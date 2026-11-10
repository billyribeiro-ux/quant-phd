"""Test suite for CAP1 replication package and audit engine."""

from __future__ import annotations

import os

import numpy as np
import pytest
from instance import make_instance
from replication_engine import (
    apply_delisting_adjustment,
    apply_share_code_filter,
    decompose_replication_divergence,
    estimate_regression,
    form_sorted_portfolios,
    verify_manifest,
    winsorize_cross_section,
)

# Seed derivation from environment or fallback
SEED = int(os.environ.get("QF_SEED", "42"))


@pytest.fixture(scope="module")
def inst() -> dict[str, object]:
    """Generate instance dataset for the active seed."""
    return make_instance(SEED)


def test_share_code_filtering(inst: dict[str, object]) -> None:
    """Verify CRSP share code and exchange filtering satisfies universe constraints."""
    permnos = np.asarray(inst["permnos"])
    shrcd = np.asarray(inst["shrcd"])
    exchcd = np.asarray(inst["exchcd"])

    mask = apply_share_code_filter(permnos, shrcd, exchcd, valid_shrcd=(10, 11), valid_exchcd=(1, 2, 3))
    assert mask.ndim == 1
    assert mask.dtype == np.bool_
    assert len(mask) == len(permnos)
    assert np.any(mask), "Filtering must retain ordinary common stocks"

    # Invariant: No retained stock has an invalid share code or exchange code
    retained_shrcd = shrcd[mask]
    retained_exchcd = exchcd[mask]
    assert np.all(np.isin(retained_shrcd, [10, 11])), "Retained shares must have SHRCD 10 or 11"
    assert np.all(np.isin(retained_exchcd, [1, 2, 3])), "Retained shares must trade on NYSE, AMEX, or NASDAQ"

    # Invariant: Excluded stocks must fail at least one criterion
    excluded_shrcd = shrcd[~mask]
    excluded_exchcd = exchcd[~mask]
    assert np.all((~np.isin(excluded_shrcd, [10, 11])) | (~np.isin(excluded_exchcd, [1, 2, 3])))


def test_delisting_adjustment_properties(inst: dict[str, object]) -> None:
    """Verify Shumway (1997) compounding and missing return imputation."""
    raw_ret = np.asarray(inst["raw_ret"], dtype=np.float64)
    dlret = np.asarray(inst["dlret"], dtype=np.float64)
    dlstcd = np.asarray(inst["dlstcd"])
    exchcd = np.asarray(inst["exchcd"])

    adj_ret = apply_delisting_adjustment(raw_ret, dlret, dlstcd, exchcd)
    assert len(adj_ret) == len(raw_ret)
    assert np.all(np.isfinite(adj_ret)), "Adjusted returns must be finite numbers"

    # Check non-delisted observations are untouched
    clean_mask = dlstcd == 0
    np.testing.assert_allclose(adj_ret[clean_mask], raw_ret[clean_mask], rtol=1e-12)

    # Check specific synthetic case
    test_ret = np.array([0.05, 0.02, 0.00])
    test_dlret = np.array([-0.20, np.nan, np.nan])
    test_dlstcd = np.array([580, 500, 200])  # perf, perf missing, non-perf missing
    test_exchcd = np.array([1, 3, 1])  # NYSE, NASDAQ, NYSE

    test_adj = apply_delisting_adjustment(test_ret, test_dlret, test_dlstcd, test_exchcd)
    # 1. Observed dlret: (1 + 0.05) * (1 - 0.20) - 1 = 1.05 * 0.80 - 1 = 0.84 - 1 = -0.16
    assert abs(test_adj[0] - (-0.16)) < 1e-6
    # 2. Missing dlret on NASDAQ perf delisting: default -55%: (1 + 0.02) * (1 - 0.55) - 1 = 1.02 * 0.45 - 1 = -0.541
    assert abs(test_adj[1] - (-0.541)) < 1e-6
    # 3. Missing dlret on non-perf delisting (code 200): default 0.0: (1 + 0.0) * (1 + 0.0) - 1 = 0.0
    assert abs(test_adj[2] - 0.0) < 1e-6


def test_cross_sectional_winsorization_properties(inst: dict[str, object]) -> None:
    """Verify that winsorization applies independently per month without inter-temporal leakage."""
    signal = np.asarray(inst["signal"], dtype=np.float64)
    months = np.asarray(inst["months"])

    winsored = winsorize_cross_section(signal, months, lower_quantile=0.05, upper_quantile=0.95)
    assert len(winsored) == len(signal)

    for m in np.unique(months)[:10]:
        m_mask = months == m
        orig_m = signal[m_mask]
        win_m = winsored[m_mask]

        q_lo = float(np.quantile(orig_m, 0.05))
        q_hi = float(np.quantile(orig_m, 0.95))

        assert float(np.min(win_m)) >= q_lo - 1e-9, "Minimum value cannot be below lower quantile"
        assert float(np.max(win_m)) <= q_hi + 1e-9, "Maximum value cannot be above upper quantile"

        # Check values strictly inside the quantiles are untouched
        interior = (orig_m > q_lo + 1e-9) & (orig_m < q_hi - 1e-9)
        np.testing.assert_allclose(win_m[interior], orig_m[interior], rtol=1e-12)


def test_portfolio_sorting_and_weighting(inst: dict[str, object]) -> None:
    """Verify decile/quintile portfolio sorting, long-short spread, and weighting differences."""
    signal = np.asarray(inst["signal"], dtype=np.float64)
    raw_ret = np.asarray(inst["raw_ret"], dtype=np.float64)
    me = np.asarray(inst["me"], dtype=np.float64)
    months = np.asarray(inst["months"])

    port_rets_vw, spread_vw = form_sorted_portfolios(signal, raw_ret, me, months, n_portfolios=5, weighting="vw")
    port_rets_ew, spread_ew = form_sorted_portfolios(signal, raw_ret, me, months, n_portfolios=5, weighting="ew")

    n_months = len(np.unique(months))
    assert port_rets_vw.shape == (n_months, 5)
    assert len(spread_vw) == n_months

    # Invariant: Spread return equals Portfolio 5 minus Portfolio 1
    np.testing.assert_allclose(spread_vw, port_rets_vw[:, 4] - port_rets_vw[:, 0], rtol=1e-12)
    np.testing.assert_allclose(spread_ew, port_rets_ew[:, 4] - port_rets_ew[:, 0], rtol=1e-12)

    # Invariant: Value-weighted returns differ from Equal-weighted returns
    assert not np.allclose(spread_vw, spread_ew), "VW and EW portfolio spreads must reflect weighting differences"


def test_regression_inference_and_clustering(inst: dict[str, object]) -> None:
    """Verify regression estimation, positive semi-definiteness, and clustered standard errors."""
    mkt = np.asarray(inst["mkt"], dtype=np.float64)
    smb = np.asarray(inst["smb"], dtype=np.float64)
    hml = np.asarray(inst["hml"], dtype=np.float64)
    t_len = len(mkt)

    # Dependent variable: synthetic factor spread
    y = 0.004 + 0.6 * mkt + 0.2 * smb + 0.1 * hml + np.random.default_rng(SEED).normal(0.0, 0.02, size=t_len)
    x_mat = np.column_stack([np.ones(t_len), mkt, smb, hml])

    res_ols = estimate_regression(y, x_mat, method="ols")
    res_white = estimate_regression(y, x_mat, method="white")
    res_nw = estimate_regression(y, x_mat, method="newey_west", nw_lags=3)

    assert len(res_ols.params) == 4
    assert np.all(res_ols.bse > 0.0), "OLS standard errors must be strictly positive"
    assert np.all(res_white.bse > 0.0), "White standard errors must be strictly positive"
    assert np.all(res_nw.bse > 0.0), "Newey-West standard errors must be strictly positive"

    # Panel regression for clustering tests
    permnos = np.asarray(inst["permnos"])
    months = np.asarray(inst["months"])
    raw_ret = np.asarray(inst["raw_ret"], dtype=np.float64)
    signal = np.asarray(inst["signal"], dtype=np.float64)

    x_panel = np.column_stack([np.ones(len(raw_ret)), signal])
    res_firm = estimate_regression(raw_ret, x_panel, method="cluster_entity", cluster_entity=permnos)
    res_time = estimate_regression(raw_ret, x_panel, method="cluster_time", cluster_time=months)
    res_2way = estimate_regression(
        raw_ret,
        x_panel,
        method="cluster_twoway",
        cluster_entity=permnos,
        cluster_time=months,
    )

    assert len(res_firm.bse) == 2
    assert len(res_time.bse) == 2
    assert len(res_2way.bse) == 2
    assert np.all(res_firm.bse > 0.0)
    assert np.all(res_time.bse > 0.0)
    assert np.all(res_2way.bse > 0.0)

    # Invariant: Finite-sample degrees of freedom factor G/(G-1) * (N-1)/(N-K) is applied
    g_count = len(np.unique(permnos))
    n_obs_p = len(raw_ret)
    k_p = 2
    expected_df_factor = np.sqrt((g_count / (g_count - 1)) * ((n_obs_p - 1) / (n_obs_p - k_p)))
    xtx_inv_p = np.linalg.pinv(x_panel.T @ x_panel)
    resid_p = raw_ret - x_panel @ res_firm.params
    meat_unadj = np.zeros((k_p, k_p))
    for g in np.unique(permnos):
        score_g = x_panel[permnos == g].T @ resid_p[permnos == g]
        meat_unadj += np.outer(score_g, score_g)
    se_unadjusted = np.sqrt(np.diag(xtx_inv_p @ meat_unadj @ xtx_inv_p))
    np.testing.assert_allclose(res_firm.bse, se_unadjusted * expected_df_factor, rtol=1e-8)

    # Invariant: R-squared in [0, 1]
    assert 0.0 <= res_ols.r_squared <= 1.0


def test_divergence_decomposition_articulation() -> None:
    """Verify articulation identity of replication divergence decomposition."""
    stages = {
        "original_published": 0.850,
        "sample_period_alignment": 0.780,
        "shrcd_filter_ordinary_common": 0.710,
        "shumway_delisting_adjustment": 0.540,
        "cross_sectional_winsorization": 0.520,
        "value_weighting": 0.380,
    }

    decomp = decompose_replication_divergence(stages)
    assert "total_divergence" in decomp
    assert "articulation_gap" in decomp

    expected_total = 0.380 - 0.850
    assert abs(decomp["total_divergence"] - expected_total) < 1e-12
    # The articulation gap must be zero: sum of incremental steps equals total change
    assert abs(decomp["articulation_gap"]) < 1e-12

    # Verify individual step values
    assert abs(decomp["delta_sample_period_alignment"] - (0.780 - 0.850)) < 1e-12
    assert abs(decomp["delta_shrcd_filter_ordinary_common"] - (0.710 - 0.780)) < 1e-12
    assert abs(decomp["delta_shumway_delisting_adjustment"] - (0.540 - 0.710)) < 1e-12


def test_manifest_verification() -> None:
    """Verify cryptographic verification of replication package outputs."""
    import hashlib

    file1 = b"replicated_table_1: beta=0.45, t=2.31\n"
    file2 = b"replicated_table_2: alpha=0.12, t=1.84\n"

    h1 = hashlib.sha256(file1).hexdigest()
    h2 = hashlib.sha256(file2).hexdigest()

    manifest = {"table1.csv": h1, "table2.csv": h2}
    files_ok = {"table1.csv": file1, "table2.csv": file2}
    assert verify_manifest(manifest, files_ok) is True

    # Tampered file
    files_corrupted = {"table1.csv": file1 + b"tampered", "table2.csv": file2}
    assert verify_manifest(manifest, files_corrupted) is False

    # Missing file
    files_missing = {"table1.csv": file1}
    assert verify_manifest(manifest, files_missing) is False
