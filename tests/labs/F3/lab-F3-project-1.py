"""Lab F3-project-1: Project Rung 1 Worked Example - Multi-Asset Factor Book.

Executes a complete multi-asset factor allocation across Rates, FX, and
Commodities, constructing Carry, Time-Series Momentum, and Value factors,
evaluating cross-asset correlations, crash skewness, and Sharpe ratio expansion
under an equal-risk parity allocation engine.
"""

from __future__ import annotations

import numpy as np
import scipy.stats


def compute_carry_factor(signals: np.ndarray, returns: np.ndarray) -> np.ndarray:
    """Build dollar-neutral cross-sectional carry factor returns."""
    t_obs, n_assets = signals.shape
    factor_rets = np.zeros(t_obs - 1)
    for t in range(t_obs - 1):
        sig = signals[t, :]
        demeaned = sig - np.mean(sig)
        denom = np.sum(np.abs(demeaned))
        weights = np.zeros(n_assets) if denom < 1e-12 else demeaned / denom
        factor_rets[t] = float(np.sum(weights * returns[t + 1, :]))
    return factor_rets


def compute_tsmom_factor(
    returns: np.ndarray,
    lookback: int = 12,
    target_vol: float = 0.10,
) -> np.ndarray:
    """Build time-series momentum factor with trailing inverse-volatility scaling."""
    t_obs, n_assets = returns.shape
    n_eval = t_obs - lookback
    factor_rets = np.zeros(n_eval)
    for idx, t in enumerate(range(lookback, t_obs)):
        past_perf = np.sum(returns[t - lookback : t, :], axis=0)
        direction = np.sign(past_perf)
        vol_win = max(0, t - 24)
        hist_vol = np.std(returns[vol_win:t, :], axis=0, ddof=1) * np.sqrt(12.0)
        hist_vol = np.maximum(hist_vol, 0.02)
        pos = direction * (target_vol / hist_vol) / float(n_assets)
        factor_rets[idx] = float(np.sum(pos * returns[t, :]))
    return factor_rets


def compute_value_factor(signals: np.ndarray, returns: np.ndarray) -> np.ndarray:
    """Build dollar-neutral cross-sectional value factor returns."""
    t_obs, n_assets = signals.shape
    factor_rets = np.zeros(t_obs - 1)
    for t in range(t_obs - 1):
        sig = signals[t, :]
        demeaned = sig - np.mean(sig)
        denom = np.sum(np.abs(demeaned))
        weights = np.zeros(n_assets) if denom < 1e-12 else demeaned / denom
        factor_rets[t] = float(np.sum(weights * returns[t + 1, :]))
    return factor_rets


def compute_factor_diagnostics(
    factor_returns: np.ndarray,
    annualization: float = 12.0,
) -> dict[str, float]:
    """Compute risk, return, and crash tail diagnostics for a factor return series."""
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


def run_worked_example(seed: int = 42) -> dict[str, object]:
    """Execute the multi-asset factor book worked pipeline on synthetic multi-asset data."""
    rng = np.random.default_rng(seed)
    n_months = 120
    n_assets = 4

    classes = ["rates", "fx", "commodities"]
    factor_streams: dict[str, np.ndarray] = {}
    lookback = 12

    for ac in classes:
        rets = rng.normal(0.005, 0.03, size=(n_months, n_assets))
        carry_sig = rng.normal(0.02, 0.01, size=(n_months, n_assets))
        val_sig = rng.normal(0.0, 0.05, size=(n_months, n_assets))

        c_raw = compute_carry_factor(carry_sig, rets)
        m_raw = compute_tsmom_factor(rets, lookback=lookback)
        v_raw = compute_value_factor(val_sig, rets)

        start_idx = lookback - 1
        factor_streams[f"{ac}_carry"] = c_raw[start_idx:]
        factor_streams[f"{ac}_tsmom"] = m_raw
        factor_streams[f"{ac}_value"] = v_raw[start_idx:]

    factor_names = sorted(factor_streams.keys())
    matrix = np.column_stack([factor_streams[name] for name in factor_names])

    vols = np.std(matrix, axis=0, ddof=1)
    inv_vols = 1.0 / np.maximum(vols, 1e-6)
    weights = inv_vols / np.sum(inv_vols)

    book_returns = matrix @ weights
    book_diag = compute_factor_diagnostics(book_returns)
    factor_diags = {name: compute_factor_diagnostics(factor_streams[name]) for name in factor_names}
    mean_standalone_sharpe = float(np.mean([d["sharpe"] for d in factor_diags.values()]))
    book_sharpe = book_diag["sharpe"]
    expansion_ratio = round(float(book_sharpe / mean_standalone_sharpe), 2) if mean_standalone_sharpe > 0 else 0.0

    return {
        "factor_names": factor_names,
        "weights": {name: round(float(w), 4) for name, w in zip(factor_names, weights, strict=True)},
        "book_returns": book_returns,
        "book_diagnostics": book_diag,
        "factor_diagnostics": factor_diags,
        "mean_standalone_sharpe": round(mean_standalone_sharpe, 2),
        "expansion_ratio": expansion_ratio,
    }


def main() -> None:
    print("Project Rung 1 | Multi-Asset Factor Book Worked Example")
    print("=" * 80)
    book = run_worked_example(seed=42)
    diags = book["factor_diagnostics"]
    assert isinstance(diags, dict)
    weights = book["weights"]
    assert isinstance(weights, dict)

    hdr = (
        f"{'Stream':<18} | {'Weight':<8} | {'Mean %':<8} | {'Vol %':<8} | {'Sharpe':<8} | {'Skew':<6} | {'MaxDD %':<7}"
    )
    print(hdr)
    print("-" * 80)
    for name in sorted(diags.keys()):
        d = diags[name]
        w = weights[name]
        row = (
            f"{name:<18} | {w:<8.4f} | {d['mean_ann']:<8.2f} | {d['vol_ann']:<8.2f} | "
            f"{d['sharpe']:<8.2f} | {d['skewness']:<8.2f} | {d['max_drawdown']:<8.2f}"
        )
        print(row)
    print("-" * 80)
    b_diag = book["book_diagnostics"]
    assert isinstance(b_diag, dict)
    b_row = (
        f"{'Composite Book':<18} | {1.0000:<8.4f} | {b_diag['mean_ann']:<8.2f} | {b_diag['vol_ann']:<8.2f} | "
        f"{b_diag['sharpe']:<8.2f} | {b_diag['skewness']:<8.2f} | {b_diag['max_drawdown']:<8.2f}"
    )
    print(b_row)
    print("=" * 80)
    print(f"Mean Standalone Sharpe:  {book['mean_standalone_sharpe']:.2f}")
    print(f"Composite Book Sharpe:   {b_diag['sharpe']:.2f}")
    print(f"Diversification Ratio:   {book['expansion_ratio']:.2f}x expansion")


main()
