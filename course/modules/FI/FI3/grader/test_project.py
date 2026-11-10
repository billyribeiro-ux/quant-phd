"""Acceptance suite for the FI3 term-premium and rates-RV engine (atlas/term_premium.py).

Runs identically in the browser (Pyodide) and locally:
    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import os
from typing import Any

import numpy as np
import pytest
from atlas import term_premium as sol  # type: ignore[attr-defined]
from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)

MATURITIES = np.array(INST["maturities"], dtype=np.float64)
YIELDS = np.array(INST["yields"], dtype=np.float64)
SPOT_CURVE = np.array(INST["spot_curve"], dtype=np.float64)
SPOT_MATURITIES = np.array(INST["spot_maturities"], dtype=np.float64)
TRADE_MATURITIES = np.array(INST["trade_maturities"], dtype=np.float64)
TRADE_WEIGHTS = np.array(INST["trade_weights"], dtype=np.float64)
TRADE_YIELDS_T0 = np.array(INST["trade_yields_t0"], dtype=np.float64)
TRADE_YIELDS_T1 = np.array(INST["trade_yields_t1"], dtype=np.float64)
FINANCING_RATE = float(INST["financing_rate"])
DT = float(INST["dt"])


# ---------------------------------------------------------------------------
# 1. Forward-rate regressions & Fama-Bliss relations
# ---------------------------------------------------------------------------


def test_fwd_flat_curve_identity() -> None:
    """On a perfectly flat yield curve, all forward rates must equal the spot yield."""
    flat_yields = np.full((10, 5), 0.05, dtype=np.float64)
    mat = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64)
    fwd = sol.fama_bliss_forward_rates(flat_yields, mat)
    assert np.allclose(fwd, 0.05, atol=1e-12)


def test_fwd_monotonicity_and_shape() -> None:
    """When yields rise strictly with maturity, 1y forward rates strictly exceed spot yields."""
    curve = np.array([0.03, 0.04, 0.048, 0.054, 0.058], dtype=np.float64)
    mat = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64)
    fwd = sol.fama_bliss_forward_rates(curve, mat)
    assert fwd.shape == curve.shape
    # For k >= 1 forward rate > spot yield
    for k in range(1, len(mat)):
        assert fwd[k] > curve[k]


def test_fwd_instance_values() -> None:
    """Forward rates on the instance yields panel are finite and have matching shape."""
    fwd = sol.fama_bliss_forward_rates(YIELDS, MATURITIES)
    assert fwd.shape == YIELDS.shape
    assert np.all(np.isfinite(fwd))


def test_fwd_validation_errors() -> None:
    """Invalid maturities (non-increasing, negative, or dimension mismatch) raise ValueError."""
    with pytest.raises(ValueError):
        sol.fama_bliss_forward_rates(YIELDS, np.array([2.0, 1.0, 3.0, 4.0, 5.0]))
    with pytest.raises(ValueError):
        sol.fama_bliss_forward_rates(YIELDS, np.array([-1.0, 2.0, 3.0, 4.0, 5.0]))
    with pytest.raises(ValueError):
        sol.fama_bliss_forward_rates(YIELDS, np.array([1.0, 2.0]))


# ---------------------------------------------------------------------------
# 2. Excess bond returns
# ---------------------------------------------------------------------------


def test_excess_returns_flat_curve_zero() -> None:
    """Under a constant flat curve, excess bond return over the short rate is identically zero."""
    flat_yields = np.full((15, 5), 0.04, dtype=np.float64)
    rx = sol.excess_bond_returns(flat_yields, MATURITIES)
    assert rx.shape == (14, 4)
    assert np.allclose(rx, 0.0, atol=1e-12)


def test_excess_returns_duration_sensitivity() -> None:
    """Under a parallel yield increase of delta_y, excess return rx^{(n)} must equal -(n-1)*delta_y."""
    mat = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64)
    delta_y = 0.0050  # +50 bps
    shift_yields = np.array(
        [
            [0.040, 0.040, 0.040, 0.040, 0.040],
            [0.040 + delta_y, 0.040 + delta_y, 0.040 + delta_y, 0.040 + delta_y, 0.040 + delta_y],
        ],
        dtype=np.float64,
    )
    rx = sol.excess_bond_returns(shift_yields, mat)
    expected_rx = -(mat[1:] - 1.0) * delta_y
    assert np.allclose(rx[0], expected_rx, atol=1e-12)


def test_excess_returns_instance_properties() -> None:
    """Excess returns have shape (T-1, K-1) and vary across maturities."""
    rx = sol.excess_bond_returns(YIELDS, MATURITIES)
    t_obs, k_mat = YIELDS.shape
    assert rx.shape == (t_obs - 1, k_mat - 1)
    assert np.all(np.isfinite(rx))
    # Standard deviation of excess returns typically increases with maturity
    stds = np.std(rx, axis=0)
    assert stds[-1] > stds[0]


def test_excess_returns_validation() -> None:
    """Mismatched maturity grid raises ValueError."""
    with pytest.raises(ValueError):
        sol.excess_bond_returns(YIELDS[:1], MATURITIES)
    with pytest.raises(ValueError):
        sol.excess_bond_returns(YIELDS, np.array([1.0, 3.0, 5.0, 7.0, 10.0]))


# ---------------------------------------------------------------------------
# 3. Cochrane-Piazzesi factor
# ---------------------------------------------------------------------------


def test_cp_factor_keys_and_shapes() -> None:
    """Cochrane-Piazzesi factor dict contains gamma, cp_factor, r2, and loadings."""
    res = sol.cochrane_piazzesi_factor(YIELDS, MATURITIES)
    assert "gamma" in res and "cp_factor" in res and "r2" in res and "loadings" in res
    t_obs, _ = YIELDS.shape
    assert res["gamma"].shape == (6,)
    assert res["cp_factor"].shape == (t_obs - 1,)
    assert res["loadings"].shape == (4,)
    assert 0.0 <= res["r2"] <= 1.0


def test_cp_factor_positive_loadings() -> None:
    """Individual excess returns load positively on the single Cochrane-Piazzesi factor."""
    res = sol.cochrane_piazzesi_factor(YIELDS, MATURITIES)
    # The loadings b_n should all be strictly positive
    assert np.all(res["loadings"] > 0.0)
    # Loadings increase with maturity
    assert res["loadings"][-1] > res["loadings"][0]


# ---------------------------------------------------------------------------
# 4. ACM model-based term premium
# ---------------------------------------------------------------------------


def test_acm_term_premium_identity() -> None:
    """Term premium and expected short rate must sum exactly to fitted yields."""
    res = sol.acm_term_premium(YIELDS, MATURITIES, num_factors=3)
    assert "term_premium" in res
    assert "expected_short_rate" in res
    assert "fitted_yields" in res
    tp = res["term_premium"]
    esr = res["expected_short_rate"]
    fitted = res["fitted_yields"]
    assert tp.shape == YIELDS.shape
    assert esr.shape == YIELDS.shape
    assert np.allclose(tp + esr, fitted, atol=1e-12)


def test_acm_var_stability() -> None:
    """The estimated physical factor VAR(1) transition matrix Phi must be stable."""
    res = sol.acm_term_premium(YIELDS, MATURITIES, num_factors=3)
    phi = res["phi"]
    assert phi.shape == (3, 3)
    eigvals = np.linalg.eigvals(phi)
    assert np.all(np.abs(eigvals) < 1.05)


def test_acm_short_rate_term_premium_near_zero() -> None:
    """The term premium on the 1-year bond is zero or small compared to the 5-year bond."""
    res = sol.acm_term_premium(YIELDS, MATURITIES, num_factors=3)
    tp = res["term_premium"]
    std_tp_1y = np.std(tp[:, 0])
    std_tp_5y = np.std(tp[:, -1])
    assert std_tp_1y <= std_tp_5y + 1e-6


# ---------------------------------------------------------------------------
# 5. Carry & Roll-Down
# ---------------------------------------------------------------------------


def test_carry_roll_down_identities() -> None:
    """Total carry & roll-down is the exact sum of carry and roll-down."""
    res = sol.carry_and_roll_down(SPOT_CURVE, SPOT_MATURITIES, horizon=1.0)
    assert "carry" in res and "roll_down" in res and "total_carry_roll" in res
    assert np.allclose(res["total_carry_roll"], res["carry"] + res["roll_down"], atol=1e-14)
    assert np.allclose(res["annualized_carry_roll"], res["total_carry_roll"] / 1.0, atol=1e-14)


def test_carry_roll_flat_curve_zero_roll() -> None:
    """On a flat yield curve, roll-down is zero for all maturities."""
    flat = np.full(5, 0.04, dtype=np.float64)
    mat = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64)
    res = sol.carry_and_roll_down(flat, mat, horizon=1.0)
    assert np.allclose(res["roll_down"], 0.0, atol=1e-14)


def test_carry_roll_upward_curve_positive_roll() -> None:
    """On a strictly upward-sloping yield curve, roll-down is strictly positive for tau > horizon."""
    upward = np.array([0.02, 0.03, 0.038, 0.044, 0.048], dtype=np.float64)
    mat = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64)
    res = sol.carry_and_roll_down(upward, mat, horizon=1.0)
    # For tau > 1 (indices 1, 2, 3, 4), roll_down must be positive
    assert np.all(res["roll_down"][1:] > 0.0)


# ---------------------------------------------------------------------------
# 6. Curve Trade P&L Attribution
# ---------------------------------------------------------------------------


def test_curve_trade_pnl_articulation() -> None:
    """P&L attribution components sum to total P&L exactly."""
    res = sol.curve_trade_pnl_attribution(
        TRADE_WEIGHTS,
        TRADE_MATURITIES,
        TRADE_YIELDS_T0,
        TRADE_YIELDS_T1,
        DT,
        FINANCING_RATE,
    )
    expected_keys = {
        "carry_pnl",
        "rolldown_pnl",
        "level_pnl",
        "slope_pnl",
        "curvature_pnl",
        "convexity_pnl",
        "residual_pnl",
        "total_pnl",
    }
    assert expected_keys.issubset(res.keys())

    sum_components = (
        res["carry_pnl"]
        + res["rolldown_pnl"]
        + res["level_pnl"]
        + res["slope_pnl"]
        + res["curvature_pnl"]
        + res["convexity_pnl"]
        + res["residual_pnl"]
    )
    assert np.isclose(sum_components, res["total_pnl"], atol=1e-10)


def test_curve_trade_zero_movement_pnl() -> None:
    """When yields do not change, level, slope, and convexity P&Ls are zero."""
    res = sol.curve_trade_pnl_attribution(
        TRADE_WEIGHTS,
        TRADE_MATURITIES,
        TRADE_YIELDS_T0,
        TRADE_YIELDS_T0,  # no yield shift
        DT,
        FINANCING_RATE,
    )
    assert np.isclose(res["level_pnl"], 0.0, atol=1e-14)
    assert np.isclose(res["slope_pnl"], 0.0, atol=1e-14)
    assert np.isclose(res["convexity_pnl"], 0.0, atol=1e-14)
