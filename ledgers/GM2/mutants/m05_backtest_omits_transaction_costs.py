"""Mutant 5: omits transaction friction during portfolio rebalancing.

Student mistake: ignores transaction costs in backtest_regime_strategy, reporting inflated gross returns.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def classify_regimes_realtime(
    growth: np.ndarray,
    inflation: np.ndarray,
    lookback: int = 36,
    burn_in: int = 24,
) -> tuple[np.ndarray, np.ndarray]:
    n = len(growth)
    regimes = np.full(n, -1, dtype=int)
    probs = np.full((n, 4), 0.25, dtype=np.float64)

    for t in range(burn_in, n):
        start = max(0, t - lookback + 1)
        w_growth = growth[start : t + 1]
        w_infl = inflation[start : t + 1]

        mean_g = float(np.mean(w_growth))
        std_g = float(np.std(w_growth, ddof=1)) if len(w_growth) > 1 else 1.0
        mean_pi = float(np.mean(w_infl))
        std_pi = float(np.std(w_infl, ddof=1)) if len(w_infl) > 1 else 1.0

        std_g = max(std_g, 1e-6)
        std_pi = max(std_pi, 1e-6)

        z_g = (growth[t] - mean_g) / std_g
        z_pi = (inflation[t] - mean_pi) / std_pi

        if z_g >= 0.0 and z_pi < 0.0:
            regimes[t] = 0
        elif z_g >= 0.0 and z_pi >= 0.0:
            regimes[t] = 1
        elif z_g < 0.0 and z_pi >= 0.0:
            regimes[t] = 2
        else:
            regimes[t] = 3

        p_g = 1.0 / (1.0 + np.exp(-1.5 * z_g))
        p_pi = 1.0 / (1.0 + np.exp(-1.5 * z_pi))

        raw_p = np.array([p_g * (1.0 - p_pi), p_g * p_pi, (1.0 - p_g) * p_pi, (1.0 - p_g) * (1.0 - p_pi)])
        total_p = np.sum(raw_p)
        probs[t] = raw_p / total_p if total_p > 1e-12 else np.full(4, 0.25)

    return regimes, probs


def estimate_regime_moments(
    returns: np.ndarray,
    regimes: np.ndarray,
    min_obs: int = 12,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    _, n_assets = returns.shape
    expected_returns = np.zeros((4, n_assets))
    cov_matrices = np.zeros((4, n_assets, n_assets))
    se_returns = np.zeros((4, n_assets))

    valid_mask = regimes >= 0
    full_sample = returns[valid_mask] if np.any(valid_mask) else returns
    global_mean = np.mean(full_sample, axis=0) * 12.0
    global_cov = np.cov(full_sample, rowvar=False) * 12.0
    global_std = np.std(full_sample, axis=0, ddof=1) * np.sqrt(12.0)

    for k in range(4):
        mask_k = regimes == k
        count_k = int(np.sum(mask_k))
        if count_k >= min_obs:
            sub = returns[mask_k]
            mean_k = np.mean(sub, axis=0) * 12.0
            cov_k = np.cov(sub, rowvar=False) * 12.0
            cov_k = 0.5 * (cov_k + cov_k.T) + 1e-5 * np.eye(n_assets)
            std_k = np.std(sub, axis=0, ddof=1) * np.sqrt(12.0)
            se_k = std_k / np.sqrt(count_k / 12.0)

            expected_returns[k] = mean_k
            cov_matrices[k] = cov_k
            se_returns[k] = se_k
        else:
            expected_returns[k] = global_mean
            cov_matrices[k] = 0.5 * (global_cov + global_cov.T) + 1e-5 * np.eye(n_assets)
            se_returns[k] = global_std / np.sqrt(max(count_k, 1) / 12.0)

    return expected_returns, cov_matrices, se_returns


def _project_simplex(v: np.ndarray) -> np.ndarray:
    n = len(v)
    u = np.sort(v)[::-1]
    cssv = np.cumsum(u) - 1.0
    ind = np.arange(1, n + 1)
    cond = u - cssv / ind > 0
    if not np.any(cond):
        return np.full(n, 1.0 / n)
    rho = np.nonzero(cond)[0][-1]
    theta = cssv[rho] / (rho + 1)
    w = np.maximum(v - theta, 0.0)
    denom = np.sum(w)
    return w / denom if denom > 1e-12 else np.full(n, 1.0 / n)


def optimize_regime_allocation(
    regime_probs: np.ndarray,
    expected_returns: np.ndarray,
    cov_matrices: np.ndarray,
    risk_aversion: float = 3.0,
    max_leverage: float = 1.0,
) -> np.ndarray:
    is_2d = regime_probs.ndim == 2
    probs_array = regime_probs if is_2d else regime_probs[np.newaxis, :]
    n_steps, n_regimes = probs_array.shape
    n_assets = expected_returns.shape[1]

    weights_out = np.zeros((n_steps, n_assets))

    for t in range(n_steps):
        p_t = probs_array[t]
        mu_blend = np.sum(p_t[:, np.newaxis] * expected_returns, axis=0)

        sigma_blend = np.zeros((n_assets, n_assets))
        for k in range(n_regimes):
            diff = expected_returns[k] - mu_blend
            dispersion = np.outer(diff, diff)
            sigma_blend += p_t[k] * (cov_matrices[k] + dispersion)

        sigma_blend = 0.5 * (sigma_blend + sigma_blend.T) + 1e-4 * np.eye(n_assets)
        inv_sigma = np.linalg.pinv(sigma_blend)
        unconstrained_w = (1.0 / max(risk_aversion, 0.1)) * (inv_sigma @ mu_blend)
        w_opt = _project_simplex(unconstrained_w) * max_leverage
        weights_out[t] = w_opt

    return weights_out if is_2d else weights_out[0]


def backtest_regime_strategy(
    asset_returns: np.ndarray,
    weights: np.ndarray,
    transaction_cost_bps: float = 10.0,
    burn_in: int = 24,
) -> dict[str, Any]:
    n_months, n_assets = asset_returns.shape
    active_months = n_months - burn_in

    net_returns = np.zeros(active_months)
    turnover = np.zeros(active_months)
    prev_w = np.full(n_assets, 1.0 / n_assets)

    for idx, t in enumerate(range(burn_in, n_months)):
        target_w = weights[t]
        turn_t = float(np.sum(np.abs(target_w - prev_w)))
        # BUG: Transaction cost set to zero regardless of transaction_cost_bps
        cost_t = 0.0

        gross_ret = float(np.sum(target_w * asset_returns[t]))
        net_ret = gross_ret - cost_t

        net_returns[idx] = net_ret
        turnover[idx] = turn_t

        drifted_w = target_w * (1.0 + asset_returns[t])
        drift_sum = np.sum(drifted_w)
        prev_w = drifted_w / drift_sum if drift_sum > 1e-12 else target_w

    equity_curve = np.cumprod(1.0 + net_returns)
    ann_ret = float(np.mean(net_returns) * 12.0)
    ann_vol = float(np.std(net_returns, ddof=1) * np.sqrt(12.0))
    sharpe = float(ann_ret / ann_vol) if ann_vol > 1e-8 else 0.0

    running_max = np.maximum.accumulate(equity_curve)
    drawdowns = (running_max - equity_curve) / running_max
    max_dd = float(np.max(drawdowns)) if len(drawdowns) > 0 else 0.0

    ann_turnover = float(np.mean(turnover) * 12.0)
    calmar = float(ann_ret / max_dd) if max_dd > 1e-6 else 0.0

    return {
        "net_returns": net_returns,
        "equity_curve": equity_curve,
        "annualized_return": ann_ret,
        "annualized_volatility": ann_vol,
        "sharpe_ratio": sharpe,
        "max_drawdown": max_dd,
        "annualized_turnover": ann_turnover,
        "calmar_ratio": calmar,
    }
