"""Student error: Omits volatility scaling in TSMOM, setting position equal to direction sign alone without dividing by trailing volatility."""

from __future__ import annotations

import numpy as np
import scipy.stats


def compute_carry_factor(signals: np.ndarray, returns: np.ndarray) -> np.ndarray:
    """Build dollar-neutral cross-sectional carry factor returns."""
    if signals.shape != returns.shape:
        raise ValueError("signals and returns must have identical shapes")
    t_obs, n_assets = signals.shape
    if t_obs < 2 or n_assets < 2:
        raise ValueError("at least 2 time periods and 2 assets required")

    factor_rets = np.zeros(t_obs - 1)
    for t in range(t_obs - 1):
        sig = signals[t, :]
        demeaned = sig - np.mean(sig)
        denom = np.sum(np.abs(demeaned))
        if denom < 1e-12:
            weights = np.zeros(n_assets)
        else:
            weights = demeaned / denom
        factor_rets[t] = float(np.sum(weights * returns[t + 1, :]))

    return factor_rets


def compute_tsmom_factor(
    returns: np.ndarray,
    lookback: int = 12,
    target_vol: float = 0.10,
) -> np.ndarray:
    """Build time-series momentum factor with missing volatility scaling."""
    t_obs, n_assets = returns.shape
    if t_obs <= lookback:
        raise ValueError("returns length must exceed lookback horizon")

    n_eval = t_obs - lookback
    factor_rets = np.zeros(n_eval)

    for idx, t in enumerate(range(lookback, t_obs)):
        past_perf = np.sum(returns[t - lookback : t, :], axis=0)
        direction = np.sign(past_perf)
        # MUTANT ERROR: no 1/vol scaling
        pos = direction / float(n_assets)
        factor_rets[idx] = float(np.sum(pos * returns[t, :]))

    return factor_rets


def compute_value_factor(signals: np.ndarray, returns: np.ndarray) -> np.ndarray:
    """Build dollar-neutral cross-sectional value factor returns."""
    if signals.shape != returns.shape:
        raise ValueError("signals and returns must have identical shapes")
    t_obs, n_assets = signals.shape
    if t_obs < 2 or n_assets < 2:
        raise ValueError("at least 2 time periods and 2 assets required")

    factor_rets = np.zeros(t_obs - 1)
    for t in range(t_obs - 1):
        sig = signals[t, :]
        demeaned = sig - np.mean(sig)
        denom = np.sum(np.abs(demeaned))
        if denom < 1e-12:
            weights = np.zeros(n_assets)
        else:
            weights = demeaned / denom
        factor_rets[t] = float(np.sum(weights * returns[t + 1, :]))

    return factor_rets


def compute_factor_diagnostics(
    factor_returns: np.ndarray,
    annualization: float = 12.0,
) -> dict[str, float]:
    """Compute risk, return, and crash tail diagnostics for a factor return series."""
    if len(factor_returns) < 2:
        raise ValueError("at least 2 observations required for diagnostics")

    mean_val = float(np.mean(factor_returns))
    vol_val = float(np.std(factor_returns, ddof=1))

    mean_ann = mean_val * annualization * 100.0
    vol_ann = vol_val * np.sqrt(annualization) * 100.0
    sharpe = float(mean_ann / vol_ann) if vol_ann > 1e-8 else 0.0

    skew = float(scipy.stats.skew(factor_returns, bias=False))
    kurt = float(scipy.stats.kurtosis(factor_returns, bias=False))

    cum_ret = np.cumsum(factor_returns)
    running_max = np.maximum.accumulate(cum_ret)
    drawdowns = cum_ret - running_max
    max_dd = float(np.min(drawdowns) * 100.0) if len(drawdowns) > 0 else 0.0

    worst_m = float(np.min(factor_returns) * 100.0)

    return {
        "mean_ann": round(mean_ann, 2),
        "vol_ann": round(vol_ann, 2),
        "sharpe": round(sharpe, 2),
        "skewness": round(skew, 2),
        "kurtosis": round(kurt, 2),
        "max_drawdown": round(max_dd, 2),
        "worst_month": round(worst_m, 2),
    }


def construct_multi_asset_factor_book(
    instance_data: dict[str, object],
    weighting_scheme: str = "risk_parity",
) -> dict[str, object]:
    """Construct multi-asset factor book."""
    classes = ["rates", "fx", "commodities"]
    factor_streams: dict[str, np.ndarray] = {}
    lookback = 12

    for ac in classes:
        ac_data = instance_data[ac]
        assert isinstance(ac_data, dict)
        rets = ac_data["returns"]
        carry_sig = ac_data["carry"]
        val_sig = ac_data["value"]

        c_raw = compute_carry_factor(carry_sig, rets)
        m_raw = compute_tsmom_factor(rets, lookback=lookback)
        v_raw = compute_value_factor(val_sig, rets)

        start_idx = lookback - 1
        factor_streams[f"{ac}_carry"] = c_raw[start_idx:]
        factor_streams[f"{ac}_tsmom"] = m_raw
        factor_streams[f"{ac}_value"] = v_raw[start_idx:]

    factor_names = sorted(factor_streams.keys())
    k_factors = len(factor_names)
    matrix = np.column_stack([factor_streams[name] for name in factor_names])

    if weighting_scheme == "risk_parity":
        vols = np.std(matrix, axis=0, ddof=1)
        inv_vols = 1.0 / np.maximum(vols, 1e-6)
        weights = inv_vols / np.sum(inv_vols)
    elif weighting_scheme == "equal_weight":
        weights = np.ones(k_factors) / float(k_factors)
    else:
        raise ValueError(f"unknown weighting scheme: {weighting_scheme}")

    book_returns = matrix @ weights
    book_diag = compute_factor_diagnostics(book_returns)
    factor_diags = {name: compute_factor_diagnostics(factor_streams[name]) for name in factor_names}
    corr_matrix = np.corrcoef(matrix, rowvar=False)

    mean_standalone_sharpe = float(np.mean([d["sharpe"] for d in factor_diags.values()]))
    book_sharpe = book_diag["sharpe"]
    expansion_ratio = round(float(book_sharpe / mean_standalone_sharpe), 2) if mean_standalone_sharpe > 0 else 0.0

    return {
        "factor_names": factor_names,
        "weights": {name: round(float(w), 4) for name, w in zip(factor_names, weights, strict=True)},
        "book_returns": book_returns,
        "book_diagnostics": book_diag,
        "factor_diagnostics": factor_diags,
        "correlation_matrix": np.round(corr_matrix, 2),
        "mean_standalone_sharpe": round(mean_standalone_sharpe, 2),
        "expansion_ratio": expansion_ratio,
    }
