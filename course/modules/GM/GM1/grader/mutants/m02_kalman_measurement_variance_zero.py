"""Mutant 2: sets measurement error variance R to zero instead of estimated idiosyncratic variances."""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Any

import numpy as np


class DynamicFactorNowcaster:
    """Dynamic Factor Model with ragged-edge Kalman filtering (Stock & Watson 2002, Giannone et al. 2008)."""

    def __init__(self, n_factors: int = 2) -> None:
        if n_factors <= 0:
            raise ValueError(f"n_factors must be positive, got {n_factors}")
        self.n_factors: int = n_factors
        self.mean_: np.ndarray | None = None
        self.std_: np.ndarray | None = None
        self.loadings_: np.ndarray | None = None
        self.trans_a_: np.ndarray | None = None
        self.trans_q_: np.ndarray | None = None
        self.meas_r_: np.ndarray | None = None
        self.beta_: np.ndarray | None = None

    def fit(self, x_balanced: np.ndarray, y_target: np.ndarray | None = None) -> DynamicFactorNowcaster:
        if not isinstance(x_balanced, np.ndarray):
            raise ValueError("X_balanced must be a numpy ndarray")
        if x_balanced.ndim != 2:
            raise ValueError(f"X_balanced must be 2-dimensional, got ndim={x_balanced.ndim}")
        if not np.all(np.isfinite(x_balanced)):
            raise ValueError("X_balanced must not contain NaN or Inf values")

        t_obs, n_series = x_balanced.shape
        if self.n_factors >= n_series:
            raise ValueError(f"n_factors ({self.n_factors}) must be strictly less than n_series ({n_series})")
        if t_obs <= n_series:
            raise ValueError(f"Sample length T ({t_obs}) must be greater than number of series N ({n_series})")

        mean = np.mean(x_balanced, axis=0)
        std = np.std(x_balanced, axis=0, ddof=1)
        x_std = (x_balanced - mean) / std

        self.mean_ = mean
        self.std_ = std

        cov = (x_std.T @ x_std) / float(t_obs)
        eigvals, eigvecs = np.linalg.eigh(cov)
        idx = np.argsort(eigvals)[::-1]
        eigvecs = eigvecs[:, idx]

        top_eigvecs = eigvecs[:, : self.n_factors]
        self.loadings_ = top_eigvecs.copy()
        factors = x_std @ top_eigvecs

        f_curr = factors[1:]
        f_prev = factors[:-1]
        trans_a, _, _, _ = np.linalg.lstsq(f_prev, f_curr, rcond=None)
        self.trans_a_ = trans_a.T

        resids = f_curr - f_prev @ trans_a
        q_cov = (resids.T @ resids) / float(len(resids) - 1)
        self.trans_q_ = 0.5 * (q_cov + q_cov.T) + 1e-6 * np.eye(self.n_factors)

        # MUTATION: Sets measurement variance to zero
        self.meas_r_ = np.zeros((n_series, n_series), dtype=np.float64)

        if y_target is not None:
            beta, _, _, _ = np.linalg.lstsq(factors, y_target, rcond=None)
            self.beta_ = beta
        else:
            default_beta = np.zeros(self.n_factors, dtype=np.float64)
            default_beta[0] = 1.0
            self.beta_ = default_beta

        return self

    def filter_ragged(self, x_ragged: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        if self.mean_ is None or self.std_ is None or self.loadings_ is None or self.trans_a_ is None:
            raise ValueError("Model must be fitted before running filter_ragged")
        t_len, _ = x_ragged.shape
        r_factors = self.n_factors
        std_safe = np.where(self.std_ > 1e-12, self.std_, 1.0)
        x_std = np.full_like(x_ragged, np.nan, dtype=np.float64)
        valid_mask = np.isfinite(x_ragged)
        x_std[valid_mask] = (x_ragged[valid_mask] - np.tile(self.mean_, (t_len, 1))[valid_mask]) / np.tile(
            std_safe, (t_len, 1)
        )[valid_mask]

        filtered_factors = np.zeros((t_len, r_factors), dtype=np.float64)
        filtered_covs = np.zeros((t_len, r_factors, r_factors), dtype=np.float64)
        state_mean = np.zeros(r_factors, dtype=np.float64)
        state_cov = np.eye(r_factors, dtype=np.float64)

        mat_a = self.trans_a_
        mat_q = self.trans_q_
        loadings = self.loadings_
        meas_r = self.meas_r_
        assert mat_a is not None and mat_q is not None and loadings is not None and meas_r is not None

        for t in range(t_len):
            pred_mean = state_mean if t == 0 else mat_a @ state_mean
            pred_cov = state_cov if t == 0 else mat_a @ state_cov @ mat_a.T + mat_q

            obs_mask = np.isfinite(x_std[t])
            n_obs = int(np.sum(obs_mask))
            if n_obs == 0:
                state_mean, state_cov = pred_mean, pred_cov
            else:
                y_star = x_std[t, obs_mask]
                lambda_star = loadings[obs_mask, :]
                r_star = meas_r[obs_mask, :][:, obs_mask]
                innov = y_star - lambda_star @ pred_mean
                innov_cov = lambda_star @ pred_cov @ lambda_star.T + r_star
                kalman_gain = pred_cov @ lambda_star.T @ np.linalg.pinv(innov_cov)
                state_mean = pred_mean + kalman_gain @ innov
                state_cov = (np.eye(r_factors) - kalman_gain @ lambda_star) @ pred_cov
                state_cov = 0.5 * (state_cov + state_cov.T)

            filtered_factors[t] = state_mean
            filtered_covs[t] = state_cov
        return filtered_factors, filtered_covs

    def nowcast(self, x_ragged: np.ndarray) -> float:
        if self.beta_ is None:
            raise ValueError("Model must be fitted before running nowcast")
        factors, _ = self.filter_ragged(x_ragged)
        return float(np.dot(self.beta_, factors[-1]))


def decompose_news(nowcaster: DynamicFactorNowcaster, x_old: np.ndarray, x_new: np.ndarray) -> dict[str, Any]:
    old_nowcast = nowcaster.nowcast(x_old)
    new_nowcast = nowcaster.nowcast(x_new)
    total_revision = new_nowcast - old_nowcast
    n_series = x_old.shape[1]
    innovations = np.zeros(n_series, dtype=np.float64)
    factors_old, _ = nowcaster.filter_ragged(x_old)
    terminal_old_factor = factors_old[-1]
    assert nowcaster.mean_ is not None and nowcaster.std_ is not None and nowcaster.loadings_ is not None

    for i in range(n_series):
        val_old = x_old[-1, i]
        val_new = x_new[-1, i]
        if np.isnan(val_old) and not np.isnan(val_new):
            pred_std = float(np.dot(nowcaster.loadings_[i, :], terminal_old_factor))
            new_std = (val_new - nowcaster.mean_[i]) / nowcaster.std_[i]
            innovations[i] = new_std - pred_std
        elif not np.isnan(val_old) and not np.isnan(val_new) and abs(val_new - val_old) > 1e-12:
            innovations[i] = (val_new - val_old) / nowcaster.std_[i]

    diffs = np.zeros(n_series, dtype=np.float64)
    for i in range(n_series):
        if abs(innovations[i]) > 1e-12 or (np.isnan(x_old[-1, i]) != np.isnan(x_new[-1, i])):
            x_step = x_old.copy()
            x_step[-1, i] = x_new[-1, i]
            diffs[i] = nowcaster.nowcast(x_step) - old_nowcast

    sum_diffs = float(np.sum(diffs))
    contributions = diffs * (total_revision / sum_diffs) if abs(sum_diffs) > 1e-12 else diffs
    weights = np.zeros(n_series, dtype=np.float64)
    for i in range(n_series):
        weights[i] = contributions[i] / innovations[i] if abs(innovations[i]) > 1e-12 else 0.0

    return {
        "old_nowcast": old_nowcast,
        "new_nowcast": new_nowcast,
        "total_revision": total_revision,
        "innovations": innovations,
        "weights": weights,
        "contributions": contributions,
    }


def calculate_surprises(actuals: np.ndarray, consensus: np.ndarray, historical_std: np.ndarray) -> np.ndarray:
    diff = actuals - consensus
    return np.asarray(diff / historical_std, dtype=np.float64)


def build_surprise_index(
    surprises: np.ndarray, weights: np.ndarray, half_life: float = 30.0, normalize: bool = True
) -> np.ndarray:
    norm_weights = weights / float(np.sum(weights))
    decay = math.exp(-math.log(2.0) / half_life)
    t_len = surprises.shape[0]
    esi = np.zeros(t_len, dtype=np.float64)
    running_state = 0.0
    for t in range(t_len):
        period_surprise = float(np.dot(surprises[t], norm_weights))
        running_state = running_state * decay + period_surprise
        esi[t] = running_state
    if normalize:
        mean_esi = float(np.mean(esi))
        std_esi = float(np.std(esi, ddof=1)) if t_len > 1 else 1.0
        if std_esi > 1e-12:
            esi = (esi - mean_esi) / std_esi
    return esi


def classify_growth_inflation_regime(
    growth_signal: float | np.ndarray,
    inflation_signal: float | np.ndarray,
    growth_threshold: float = 0.0,
    inflation_threshold: float = 0.0,
) -> str | np.ndarray:
    if isinstance(growth_signal, (int, float)) and isinstance(inflation_signal, (int, float)):
        g, inf = float(growth_signal), float(inflation_signal)
        if g >= growth_threshold:
            return "Goldilocks" if inf < inflation_threshold else "Reflation"
        else:
            return "Stagflation" if inf >= inflation_threshold else "Deflation"

    g_arr = np.asarray(growth_signal, dtype=np.float64)
    inf_arr = np.asarray(inflation_signal, dtype=np.float64)
    res = np.empty(g_arr.shape, dtype=object)
    for idx in np.ndindex(g_arr.shape):
        val_g, val_inf = float(g_arr[idx]), float(inf_arr[idx])
        if val_g >= growth_threshold:
            res[idx] = "Goldilocks" if val_inf < inflation_threshold else "Reflation"
        else:
            res[idx] = "Stagflation" if val_inf >= inflation_threshold else "Deflation"
    return res


def compute_regime_probabilities(
    growth_series: np.ndarray,
    inflation_series: np.ndarray,
    growth_threshold: float = 0.0,
    inflation_threshold: float = 0.0,
    bandwidth: float = 1.0,
) -> np.ndarray:
    t_len = len(growth_series)
    probs = np.zeros((t_len, 4), dtype=np.float64)
    p_high_g = 1.0 / (1.0 + np.exp(-(growth_series - growth_threshold) / bandwidth))
    p_high_inf = 1.0 / (1.0 + np.exp(-(inflation_series - inflation_threshold) / bandwidth))
    probs[:, 0] = p_high_g * (1.0 - p_high_inf)
    probs[:, 1] = p_high_g * p_high_inf
    probs[:, 2] = (1.0 - p_high_g) * p_high_inf
    probs[:, 3] = (1.0 - p_high_g) * (1.0 - p_high_inf)
    probs /= np.sum(probs, axis=1, keepdims=True)
    return probs


def cross_asset_macro_sensitivity(
    asset_returns: np.ndarray, macro_signals: np.ndarray, regime_labels: Sequence[str] | np.ndarray
) -> dict[str, Any]:
    t_len, n_assets = asset_returns.shape
    x_mat = np.column_stack([np.ones(t_len, dtype=np.float64), macro_signals])
    beta_coeffs, _, _, _ = np.linalg.lstsq(x_mat, asset_returns, rcond=None)
    betas = beta_coeffs[1:, :].T
    regimes = ["Goldilocks", "Reflation", "Stagflation", "Deflation"]
    labels_arr = np.asarray(regime_labels)
    regime_mean_returns: dict[str, np.ndarray] = {}
    regime_sharpe: dict[str, np.ndarray] = {}
    for reg in regimes:
        mask = labels_arr == reg
        if np.sum(mask) > 1:
            sub_rets = asset_returns[mask]
            m_ret = np.mean(sub_rets, axis=0)
            s_ret = np.std(sub_rets, axis=0, ddof=1)
            regime_mean_returns[reg] = m_ret
            regime_sharpe[reg] = np.where(s_ret > 1e-12, (m_ret / s_ret) * math.sqrt(252.0), 0.0)
        else:
            regime_mean_returns[reg] = np.zeros(n_assets, dtype=np.float64)
            regime_sharpe[reg] = np.zeros(n_assets, dtype=np.float64)
    return {"betas": betas, "regime_mean_returns": regime_mean_returns, "regime_sharpe": regime_sharpe}
