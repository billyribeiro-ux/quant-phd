"""Acceptance test suite for X2 project: Currency factor replication (currency_factors.py).

Dual-mode: runs identically in the browser (Pyodide) and locally:
    QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error grader/test_project.py
"""

from __future__ import annotations

import importlib
import math
import os
from collections.abc import Callable
from typing import Any

import pytest

sol: Any = importlib.import_module(os.environ.get("QF_SOL", "currency_factors"))
make_instance: Callable[[int], dict[str, Any]] = importlib.import_module("instance").make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST = make_instance(SEED)


def expect(condition: bool, hint: str) -> None:
    """Fail with a descriptive hint if condition is false."""
    __tracebackhide__ = True
    if not condition:
        pytest.fail(hint, pytrace=False)


def must_raise(call: Callable[[], object], condition: str, *, substring: str = "") -> None:
    """Check that call() raises ValueError with optional required substring."""
    __tracebackhide__ = True
    try:
        call()
    except ValueError as err:
        if substring and substring not in str(err):
            pytest.fail(
                f"{condition}: ValueError message must contain '{substring}' (got: {err})",
                pytrace=False,
            )
        return
    except Exception as exc:
        pytest.fail(f"{condition}: expected ValueError, got {type(exc).__name__}: {exc}", pytrace=False)
    pytest.fail(f"{condition}: expected ValueError, none was raised", pytrace=False)


def test_input_validation() -> None:
    """Test required ValueError exceptions on invalid inputs."""
    spots_valid = [[1.0, 1.2], [1.02, 1.18], [1.01, 1.19]]
    forwards_valid = [[0.99, 1.21], [1.01, 1.19], [1.00, 1.20]]

    # 1. Excess returns checks
    must_raise(
        lambda: sol.compute_excess_returns([], []),
        "empty spots and forwards in compute_excess_returns",
        substring="non-empty",
    )
    must_raise(
        lambda: sol.compute_excess_returns(spots_valid[:1], forwards_valid[:1]),
        "fewer than 2 periods in compute_excess_returns",
        substring="At least 2 periods",
    )
    must_raise(
        lambda: sol.compute_excess_returns(spots_valid, forwards_valid[:2]),
        "mismatched length in compute_excess_returns",
        substring="identical length",
    )
    must_raise(
        lambda: sol.compute_excess_returns([[1.0], [1.0]], [[0.99], [0.99]]),
        "fewer than 2 currencies in compute_excess_returns",
        substring="At least 2 currencies",
    )

    # 2. Forward discounts checks
    must_raise(
        lambda: sol.compute_forward_discounts([], []),
        "empty spots and forwards in compute_forward_discounts",
        substring="non-empty",
    )

    # 3. Portfolio sorting checks
    rx_dummy = [[0.01, -0.01], [0.02, -0.02]]
    fd_dummy = [[-0.005, 0.005], [-0.004, 0.004]]
    must_raise(
        lambda: sol.sort_carry_portfolios(rx_dummy, fd_dummy, n_portfolios=1),
        "n_portfolios < 2 in sort_carry_portfolios",
        substring="at least 2",
    )
    must_raise(
        lambda: sol.sort_carry_portfolios(rx_dummy, fd_dummy, n_portfolios=5),
        "n_portfolios > n_currencies in sort_carry_portfolios",
        substring="cannot exceed number of currencies",
    )

    # 4. Volatility innovations checks
    must_raise(
        lambda: sol.estimate_volatility_innovations([], days_per_month=21),
        "empty daily returns in estimate_volatility_innovations",
        substring="non-empty",
    )
    must_raise(
        lambda: sol.estimate_volatility_innovations([[0.01, -0.01]], days_per_month=2),
        "days_per_month < 5 in estimate_volatility_innovations",
        substring="at least 5",
    )

    # 5. Full pipeline checks
    bad_inst = dict(INST)
    del bad_inst["spot_rates"]
    must_raise(
        lambda: sol.run_currency_factor_replication(bad_inst),
        "missing spot_rates in run_currency_factor_replication",
        substring="must contain spot_rates",
    )


def test_excess_returns_and_discounts() -> None:
    """Verify mathematical definitions of excess returns and forward discounts."""
    spots = [
        [1.00, 2.00],
        [1.05, 1.90],
        [1.10, 1.95],
    ]
    forwards = [
        [0.98, 2.02],
        [1.04, 1.92],
        [1.08, 1.96],
    ]

    rx = sol.compute_excess_returns(spots, forwards)
    fd = sol.compute_forward_discounts(spots, forwards)

    expect(len(rx) == 2, f"Excess returns should have T-1=2 rows, got {len(rx)}")
    expect(len(fd) == 2, f"Forward discounts should have T-1=2 rows, got {len(fd)}")

    # Period 0 -> 1 for Currency 0:
    # S_{t+1}=1.05, F_t=0.98 -> rx = ln(1.05) - ln(0.98) = 0.068993
    expected_rx_00 = math.log(1.05) - math.log(0.98)
    expect(
        abs(rx[0][0] - expected_rx_00) < 1e-4,
        f"rx[0][0] should match {expected_rx_00:.5f}, got {rx[0][0]:.5f}",
    )

    # Forward discount at t=0 for Currency 0:
    # F_0=0.98, S_0=1.00 -> fd = ln(0.98) - ln(1.00) = -0.020203
    expected_fd_00 = math.log(0.98) - math.log(1.00)
    expect(
        abs(fd[0][0] - expected_fd_00) < 1e-4,
        f"fd[0][0] should match {expected_fd_00:.5f}, got {fd[0][0]:.5f}",
    )


def test_carry_portfolio_properties() -> None:
    """Verify sorting order and performance characteristics of carry portfolios."""
    spots = INST["spot_rates"]
    forwards = INST["forward_rates"]

    rx = sol.compute_excess_returns(spots, forwards)
    fd = sol.compute_forward_discounts(spots, forwards)

    carry_res = sol.sort_carry_portfolios(rx, fd, n_portfolios=5)

    port_rets = carry_res["portfolio_returns"]
    mean_rets = carry_res["mean_returns"]
    carry_res["std_returns"]
    carry_res["sharpe_ratios"]

    expect(len(mean_rets) == 5, f"Expected 5 portfolio returns, got {len(mean_rets)}")
    expect(len(port_rets) == len(rx), f"Portfolio return rows must match {len(rx)}")

    # Economic property: Top carry portfolio (P5) must outperform bottom carry portfolio (P1)
    # The carry spread (P5 - P1) must be positive on average
    carry_spread = mean_rets[-1] - mean_rets[0]
    expect(
        carry_spread > 0.0,
        f"Carry spread P5 - P1 must be positive, got {carry_spread:.4f} (P1={mean_rets[0]}, P5={mean_rets[-1]})",
    )

    # Annualization verification for portfolio 0:
    p0_rets = [port_rets[t][0] for t in range(len(port_rets))]
    m_p0 = sum(p0_rets) / len(p0_rets)
    expected_ann_mean = round(m_p0 * 12.0, 5)
    expect(
        abs(mean_rets[0] - expected_ann_mean) < 1e-4,
        f"P1 annualized mean return should be {expected_ann_mean}, got {mean_rets[0]}",
    )


def test_hml_and_dollar_properties() -> None:
    """Verify Dollar factor and HML-FX factor construction and properties."""
    spots = INST["spot_rates"]
    forwards = INST["forward_rates"]

    rx = sol.compute_excess_returns(spots, forwards)
    fd = sol.compute_forward_discounts(spots, forwards)
    carry_res = sol.sort_carry_portfolios(rx, fd, n_portfolios=5)
    port_rets = carry_res["portfolio_returns"]

    factors = sol.build_factors(port_rets)
    dol = factors["dollar_factor"]
    hml = factors["hml_fx"]

    expect(len(dol) == len(port_rets), "Dollar factor length must match portfolio returns")
    expect(len(hml) == len(port_rets), "HML-FX factor length must match portfolio returns")

    # For each period t, check exact formulas:
    for t in range(min(10, len(port_rets))):
        expected_dol = round(sum(port_rets[t]) / 5.0, 6)
        expected_hml = round(port_rets[t][-1] - port_rets[t][0], 6)
        expect(
            abs(dol[t] - expected_dol) < 1e-4,
            f"Dollar factor at t={t} should be {expected_dol}, got {dol[t]}",
        )
        expect(
            abs(hml[t] - expected_hml) < 1e-4,
            f"HML-FX factor at t={t} should be {expected_hml}, got {hml[t]}",
        )

    # Dollar neutrality test: HML factor mean should be positive and dollar-hedged
    mean_hml = sum(hml) / len(hml)
    expect(
        mean_hml > 0.0,
        f"HML factor mean return must be positive, got {mean_hml:.5f}",
    )


def test_volatility_innovation_properties() -> None:
    """Verify global FX volatility aggregation and AR(1) innovation residual properties."""
    daily_returns = INST["daily_returns"]

    vol_info = sol.estimate_volatility_innovations(daily_returns, days_per_month=21)

    m_vol = vol_info["monthly_vol"]
    innov = vol_info["vol_innovations"]
    rho = vol_info["ar1_rho"]

    expect(len(m_vol) >= 3, "Monthly vol must contain at least 3 observations")
    expect(len(innov) == len(m_vol) - 1, "Innovations length must be monthly_vol length - 1")

    # AR(1) persistence rho should be stationary
    expect(
        -0.95 < rho < 0.99,
        f"AR(1) persistence coefficient rho should be stationary, got {rho}",
    )

    # Innovations are regression residuals, so their sample mean must be close to zero
    mean_innov = sum(innov) / len(innov)
    expect(
        abs(mean_innov) < 1e-4,
        f"Mean of AR(1) volatility innovations must be approximately zero, got {mean_innov}",
    )

    # Innovations must not be identical to raw monthly volatility levels
    expect(
        abs(innov[0] - m_vol[1]) > 1e-4,
        "Volatility innovations must be residuals, not raw volatility levels",
    )


def test_fama_macbeth_properties() -> None:
    """Verify two-pass Fama-MacBeth beta estimation and cross-sectional pricing."""
    spots = INST["spot_rates"]
    forwards = INST["forward_rates"]

    rx = sol.compute_excess_returns(spots, forwards)
    fd = sol.compute_forward_discounts(spots, forwards)
    carry_res = sol.sort_carry_portfolios(rx, fd, n_portfolios=5)
    port_rets = carry_res["portfolio_returns"]

    factors = sol.build_factors(port_rets)
    dol = factors["dollar_factor"]
    hml = factors["hml_fx"]

    t_eval = len(port_rets)
    factor_mat = [[dol[t], hml[t]] for t in range(t_eval)]

    fm_res = sol.fama_macbeth_twostep(
        port_rets,
        factor_mat,
        factor_names=["DOL", "HML"],
    )

    betas = fm_res["betas"]
    lambdas = fm_res["lambda_premia"]
    r2 = fm_res["r_squared"]
    mape = fm_res["mape"]

    expect(len(betas) == 5, f"Expected 5 sets of betas, got {len(betas)}")
    expect(len(lambdas) == 2, f"Expected 2 factor risk premia, got {len(lambdas)}")

    # Lustig et al. (2011) Theorem:
    # 1. Level factor: All portfolios have beta_DOL close to 1.0
    for k in range(5):
        beta_dol_k = betas[k][0]
        expect(
            abs(beta_dol_k - 1.0) < 0.45,
            f"Portfolio {k + 1} beta to Dollar factor must be close to 1.0, got {beta_dol_k}",
        )

    # 2. Slope factor: beta_HML must increase from P1 to P5
    # beta_HML(P1) < 0, beta_HML(P5) > 0
    beta_hml_p1 = betas[0][1]
    beta_hml_p5 = betas[-1][1]
    expect(
        beta_hml_p1 < 0.0,
        f"Portfolio 1 beta to HML-FX should be negative, got {beta_hml_p1}",
    )
    expect(
        beta_hml_p5 > 0.0,
        f"Portfolio 5 beta to HML-FX should be positive, got {beta_hml_p5}",
    )
    expect(
        beta_hml_p5 > beta_hml_p1,
        f"HML-FX beta must increase from P1 to P5 ({beta_hml_p1} vs {beta_hml_p5})",
    )

    # Cross-sectional explanatory power
    expect(
        r2 > 0.50,
        f"Lustig 2-factor model cross-sectional R^2 should exceed 0.50, got {r2}",
    )
    expect(
        mape < 0.05,
        f"Mean absolute pricing error should be small, got {mape}",
    )


def test_full_replication_pipeline() -> None:
    """Verify that run_currency_factor_replication executes completely and structures output."""
    res = sol.run_currency_factor_replication(INST)

    expect("carry_portfolios" in res, "Results must contain 'carry_portfolios'")
    expect("factors" in res, "Results must contain 'factors'")
    expect("lustig_model" in res, "Results must contain 'lustig_model'")
    expect("menkhoff_model" in res, "Results must contain 'menkhoff_model'")

    lustig_r2 = res["lustig_model"]["r_squared"]
    menkhoff_r2 = res["menkhoff_model"]["r_squared"]

    expect(lustig_r2 > 0.50, f"Lustig model R2 must be > 0.50, got {lustig_r2}")
    expect(menkhoff_r2 > -0.50, f"Menkhoff model R2 must be bounded, got {menkhoff_r2}")

    # Verify that factor list length matches time series
    t_ret = len(res["carry_portfolios"]["portfolio_returns"])
    expect(
        len(res["factors"]["dollar_factor"]) == t_ret,
        "Factor series length must match portfolio returns length",
    )
