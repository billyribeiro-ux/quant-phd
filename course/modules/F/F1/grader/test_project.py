"""Acceptance suite for Atlas A7 (atlas.cross_section), the F1 project.

Runs identically in Pyodide and locally:

    QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import os
from collections.abc import Callable

import numpy as np
import pytest

try:
    import atlas.cross_section as a7
except ImportError:
    import reference as a7

from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST = make_instance(SEED)


def must_raise(call: Callable[[], object], condition: str) -> None:
    """Fail with a descriptive message unless call() raises ValueError."""
    try:
        call()
    except ValueError:
        return
    pytest.fail(f"{condition}: the contract requires a ValueError naming the violated condition.")


def test_delisting_return_adjustment() -> None:
    """Checks that delisting returns compound properly and Shumway missing rules apply."""
    raw_returns = np.asarray(INST["raw_returns"], dtype=np.float64)
    delist_codes = np.asarray(INST["delist_codes"], dtype=np.int32)
    delist_returns = np.asarray(INST["delist_returns"], dtype=np.float64)
    exchange_codes = np.asarray(INST["exchange_codes"], dtype=np.int32)

    adj = a7.apply_shumway_delisting(raw_returns, delist_codes, delist_returns, exchange_codes)

    assert len(adj) == len(raw_returns)
    assert np.all(np.isfinite(adj))

    # Test synthetic targeted cases
    test_ret = np.array([0.02, 0.05, 0.01, -0.04, 0.00], dtype=np.float64)
    test_dl_codes = np.array([100, 200, 500, 560, 200], dtype=np.int32)
    test_dl_ret = np.array([np.nan, 0.15, np.nan, np.nan, np.nan], dtype=np.float64)
    test_ex = np.array([1, 1, 1, 3, 2], dtype=np.int32)

    res = a7.apply_shumway_delisting(test_ret, test_dl_codes, test_dl_ret, test_ex)

    # 1. Active: 0.02
    assert pytest.approx(res[0], abs=1e-6) == 0.02
    # 2. Merger with reported return: (1 + 0.05) * (1 + 0.15) - 1 = 1.05 * 1.15 - 1 = 0.2075
    assert pytest.approx(res[1], abs=1e-6) == 0.2075
    # 3. NYSE Performance delisting with missing return: -30% Shumway penalty
    # (1 + 0.01) * (1 - 0.30) - 1 = 1.01 * 0.70 - 1 = -0.2930
    assert pytest.approx(res[2], abs=1e-6) == -0.2930
    # 4. NASDAQ Performance delisting with missing return: -55% Shumway & Sloan penalty
    # (1 - 0.04) * (1 - 0.55) - 1 = 0.96 * 0.45 - 1 = -0.5680
    assert pytest.approx(res[3], abs=1e-6) == -0.5680
    # 5. AMEX merger with missing return: 0.0 replacement
    # (1 + 0.00) * (1 + 0.0) - 1 = 0.00
    assert pytest.approx(res[4], abs=1e-6) == 0.00


def test_nyse_breakpoints_isolation() -> None:
    """Verifies that NYSE breakpoints isolate microcaps and differ from all-stock breakpoints."""
    chars = np.asarray(INST["signal1"], dtype=np.float64)
    ex = np.asarray(INST["exchange_codes"], dtype=np.int32)

    cuts_nyse = a7.compute_breakpoints(chars, ex, n_quantiles=5, use_nyse_only=True)
    cuts_all = a7.compute_breakpoints(chars, ex, n_quantiles=5, use_nyse_only=False)

    assert len(cuts_nyse) == 4
    assert len(cuts_all) == 4
    # Strictly increasing breakpoints
    assert np.all(np.diff(cuts_nyse) > 0.0)
    assert np.all(np.diff(cuts_all) > 0.0)

    # Synthetic test where NYSE distribution is higher than NASDAQ microcap distribution
    synth_chars = np.concatenate([np.linspace(10.0, 50.0, 30), np.linspace(1.0, 9.0, 50)])
    synth_ex = np.concatenate([np.ones(30, dtype=np.int32), np.full(50, 3, dtype=np.int32)])

    nyse_cuts = a7.compute_breakpoints(synth_chars, synth_ex, n_quantiles=5, use_nyse_only=True)
    all_cuts = a7.compute_breakpoints(synth_chars, synth_ex, n_quantiles=5, use_nyse_only=False)

    # NYSE-only breakpoints must be strictly higher than all-stock breakpoints
    assert np.all(nyse_cuts > all_cuts)


def test_portfolio_weighting_schemes() -> None:
    """Checks univariate sorting, value-weighting vs equal-weighting, and spread returns."""
    raw_returns = np.asarray(INST["raw_returns"], dtype=np.float64)
    delist_codes = np.asarray(INST["delist_codes"], dtype=np.int32)
    delist_returns = np.asarray(INST["delist_returns"], dtype=np.float64)
    ex = np.asarray(INST["exchange_codes"], dtype=np.int32)
    caps = np.asarray(INST["market_caps"], dtype=np.float64)
    sig = np.asarray(INST["signal1"], dtype=np.float64)

    adj_ret = a7.apply_shumway_delisting(raw_returns, delist_codes, delist_returns, ex)

    vw_res = a7.univariate_sort(adj_ret, sig, caps, ex, n_quantiles=5, use_nyse_only=True, weighting="value")
    ew_res = a7.univariate_sort(adj_ret, sig, caps, ex, n_quantiles=5, use_nyse_only=True, weighting="equal")

    vw_ports = np.asarray(vw_res["portfolio_returns"])
    ew_ports = np.asarray(ew_res["portfolio_returns"])

    assert len(vw_ports) == 5
    assert len(ew_ports) == 5
    # Value-weighted and equal-weighted returns should not be identically equal across all bins
    assert not np.allclose(vw_ports, ew_ports, atol=1e-7)

    # Spread return is top minus bottom
    assert pytest.approx(vw_res["spread_return"], abs=1e-8) == float(vw_ports[4] - vw_ports[0])
    assert pytest.approx(ew_res["spread_return"], abs=1e-8) == float(ew_ports[4] - ew_ports[0])

    # Stock counts must sum to total stock count
    counts = np.asarray(vw_res["counts"])
    assert int(np.sum(counts)) == len(raw_returns)


def test_bivariate_sort_execution() -> None:
    """Checks 2D independent and conditional portfolio sorts."""
    adj_ret = a7.apply_shumway_delisting(
        np.asarray(INST["raw_returns"]),
        np.asarray(INST["delist_codes"]),
        np.asarray(INST["delist_returns"]),
        np.asarray(INST["exchange_codes"]),
    )
    s1 = np.asarray(INST["signal1"])
    s2 = np.asarray(INST["signal2"])
    caps = np.asarray(INST["market_caps"])
    ex = np.asarray(INST["exchange_codes"])

    res_indep = a7.bivariate_sort(
        adj_ret, s1, s2, caps, ex, n_quantiles1=2, n_quantiles2=3, method="independent", weighting="value"
    )
    res_cond = a7.bivariate_sort(
        adj_ret, s1, s2, caps, ex, n_quantiles1=2, n_quantiles2=3, method="conditional", weighting="value"
    )

    grid_indep = np.asarray(res_indep["grid_returns"])
    grid_cond = np.asarray(res_cond["grid_returns"])

    assert grid_indep.shape == (2, 3)
    assert grid_cond.shape == (2, 3)
    assert np.all(np.isfinite(grid_indep))
    assert np.all(np.isfinite(grid_cond))

    assert isinstance(res_indep["factor_hml"], float)
    assert isinstance(res_indep["factor_smb"], float)


def test_fama_macbeth_shanken_se() -> None:
    """Verifies Fama-MacBeth two-pass slopes and Shanken errors-in-variables correction."""
    excess = np.asarray(INST["panel_excess"], dtype=np.float64)
    factors = np.asarray(INST["panel_factors"], dtype=np.float64)
    betas = np.asarray(INST["true_betas"], dtype=np.float64)

    fm = a7.fama_macbeth(excess, betas, factor_returns=factors)

    t_obs, _n_assets = excess.shape
    k_factors = betas.shape[1]

    assert len(fm.premia) == k_factors + 1
    assert len(fm.naive_se) == k_factors + 1
    assert len(fm.shanken_se) == k_factors + 1

    # Shanken standard errors on factor slopes must strictly exceed naive standard errors
    # due to errors-in-variables uncertainty correction (c >= 1.0 and (1/T)*Sigma_f > 0)
    for k in range(1, k_factors + 1):
        assert fm.shanken_se[k] > fm.naive_se[k]
        assert abs(fm.t_stat_shanken[k]) < abs(fm.t_stat_naive[k])

    # Check without factor_returns falls back to naive SE
    fm_naive_only = a7.fama_macbeth(excess, betas, factor_returns=None)
    assert np.allclose(fm_naive_only.shanken_se, fm_naive_only.naive_se, atol=1e-12)

    # Verify Shanken variance includes the additive (1/T) * Sigma_f factor covariance term
    f_ret = np.asarray(factors, dtype=np.float64)
    sigma_f = np.cov(f_ret, rowvar=False, ddof=1)
    lambda_f = fm.premia[1:]
    c_shanken = 1.0 + float(lambda_f.T @ np.linalg.solve(sigma_f, lambda_f))
    expected_factor_var = (c_shanken * (fm.naive_se[1] ** 2 * t_obs) + (1.0 / t_obs) * sigma_f[0, 0]) / t_obs
    assert pytest.approx(fm.shanken_se[1] ** 2, rel=1e-6) == expected_factor_var


def test_grs_exact_f_statistic() -> None:
    """Verifies Gibbons-Ross-Shanken (1989) exact test statistic calculation."""
    excess = np.asarray(INST["panel_excess"], dtype=np.float64)
    factors = np.asarray(INST["panel_factors"], dtype=np.float64)
    t_obs, n_assets = excess.shape
    k_factors = factors.shape[1]

    # Run time-series regressions for each asset to obtain alphas and residuals
    x_ts = np.column_stack([np.ones(t_obs, dtype=np.float64), factors])
    x_t_x = x_ts.T @ x_ts
    alphas = np.empty(n_assets, dtype=np.float64)
    residuals = np.empty((t_obs, n_assets), dtype=np.float64)

    for i in range(n_assets):
        y_i = excess[:, i]
        b = np.linalg.solve(x_t_x, x_ts.T @ y_i)
        alphas[i] = b[0]
        residuals[:, i] = y_i - x_ts @ b

    grs = a7.grs_test(alphas, residuals, factors)

    assert grs.stat > 0.0
    assert 0.0 <= grs.p_value <= 1.0
    assert grs.df_num == n_assets
    assert grs.df_denom == t_obs - n_assets - k_factors

    # Verify exact GRS formula with unbiased residual covariance degrees of freedom (T - K - 1)
    sigma_e = (residuals.T @ residuals) / float(t_obs - k_factors - 1)
    mu_f = np.mean(factors, axis=0)
    sigma_f = np.cov(factors, rowvar=False, ddof=1)
    sh2_f = float(mu_f.T @ np.linalg.solve(sigma_f, mu_f))
    expected_grs = (
        float(t_obs - n_assets - k_factors)
        / float(n_assets)
        * (1.0 / (1.0 + sh2_f))
        * float(alphas.T @ np.linalg.solve(sigma_e, alphas))
    )
    assert pytest.approx(grs.stat, rel=1e-6) == expected_grs

    # Verify scaling property: zero alphas produce zero GRS statistic
    zero_alphas = np.zeros(n_assets, dtype=np.float64)
    grs_zero = a7.grs_test(zero_alphas, residuals, factors)
    assert pytest.approx(grs_zero.stat, abs=1e-9) == 0.0
    assert pytest.approx(grs_zero.p_value, abs=1e-5) == 1.0


def test_input_validation() -> None:
    """Verifies that invalid dimensions, types, and constraints trigger ValueError."""
    dummy_ret = np.array([0.01, 0.02, 0.03], dtype=np.float64)
    dummy_ex = np.array([1, 2, 3], dtype=np.int32)
    dummy_caps = np.array([100.0, 200.0, 300.0], dtype=np.float64)

    # 1. Invalid n_quantiles
    must_raise(
        lambda: a7.compute_breakpoints(dummy_ret, dummy_ex, n_quantiles=1),
        "n_quantiles < 2",
    )

    # 2. No valid NYSE securities
    all_nasdaq = np.array([3, 3, 3], dtype=np.int32)
    must_raise(
        lambda: a7.compute_breakpoints(dummy_ret, all_nasdaq, n_quantiles=2, use_nyse_only=True),
        "no NYSE stocks with use_nyse_only=True",
    )

    # 3. Invalid weighting string
    must_raise(
        lambda: a7.univariate_sort(dummy_ret, dummy_ret, dummy_caps, dummy_ex, weighting="invalid"),
        "invalid weighting mode",
    )

    # 4. Strictly positive market caps required
    negative_caps = np.array([100.0, -50.0, 300.0], dtype=np.float64)
    must_raise(
        lambda: a7.univariate_sort(dummy_ret, dummy_ret, negative_caps, dummy_ex),
        "negative market cap",
    )

    # 5. GRS degrees of freedom non-positive
    small_res = np.ones((5, 10), dtype=np.float64)  # T=5, N=10 -> T < N
    small_factors = np.ones((5, 1), dtype=np.float64)
    small_alphas = np.ones(10, dtype=np.float64)
    must_raise(
        lambda: a7.grs_test(small_alphas, small_res, small_factors),
        "T <= N + K for GRS",
    )
