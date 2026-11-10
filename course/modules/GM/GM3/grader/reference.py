"""Reference solution for GM3 Project: Pre-FOMC Drift Out-of-Sample Check.

Provides complete econometric implementations for high-frequency FOMC event studies,
Kuttner Fed funds futures scaling, pre-FOMC announcement drift estimation,
non-parametric placebo permutation testing, and out-of-sample decay evaluation.
"""

from __future__ import annotations

import math

import numpy as np


def compute_kuttner_surprises(
    pre_rates: np.ndarray,
    post_rates: np.ndarray,
    days_in_month: np.ndarray,
    announcement_days: np.ndarray,
) -> np.ndarray:
    """Compute discrete target rate surprises from Fed funds futures price jumps.

    Applies the Kuttner (2001) month-scaling formula:
        Delta i_t^u = (M / (M - d)) * (f_{t, post} - f_{t, pre}) * 100 (in bps)
    For announcements occurring on or after day M - 1, the unscaled jump is used
    to avoid singularity/division-by-zero boundary effects.
    """
    if (
        len(pre_rates) != len(post_rates)
        or len(pre_rates) != len(days_in_month)
        or len(pre_rates) != len(announcement_days)
    ):
        raise ValueError("All input arrays must have identical length")
    if len(pre_rates) == 0:
        raise ValueError("Input arrays must not be empty")

    delta_f_percent = post_rates - pre_rates
    surprises = np.zeros(len(pre_rates), dtype=np.float64)

    for i in range(len(pre_rates)):
        m = float(days_in_month[i])
        d = float(announcement_days[i])
        if m <= 0 or d < 1:
            raise ValueError(f"Invalid calendar parameters at index {i}: M={m}, d={d}")

        scale_factor = 1.0 if d >= m - 1 else m / (m - d)
        surprises[i] = scale_factor * delta_f_percent[i] * 100.0

    return surprises


def regress_equity_response(
    surprises_bps: np.ndarray,
    equity_returns_bps: np.ndarray,
) -> dict[str, float]:
    """Estimate the Bernanke & Kuttner (2005) equity sensitivity regression.

    Model:
        R_t = alpha + beta * Delta i_t^u + epsilon_t
    """
    if len(surprises_bps) != len(equity_returns_bps):
        raise ValueError("Arrays must have identical length")
    n = len(surprises_bps)
    if n < 3:
        raise ValueError("Need at least 3 observations for regression")

    x = surprises_bps.astype(np.float64)
    y = equity_returns_bps.astype(np.float64)

    mean_x = float(np.mean(x))
    mean_y = float(np.mean(y))

    ss_xx = float(np.sum((x - mean_x) ** 2))
    if ss_xx <= 1e-12:
        raise ValueError("Zero variance in policy surprises")

    ss_xy = float(np.sum((x - mean_x) * (y - mean_y)))
    beta = ss_xy / ss_xx
    alpha = mean_y - beta * mean_x

    y_pred = alpha + beta * x
    residuals = y - y_pred
    ss_res = float(np.sum(residuals**2))
    ss_tot = float(np.sum((y - mean_y) ** 2))

    r_squared = 1.0 - (ss_res / ss_tot) if ss_tot > 1e-12 else 0.0
    r_squared = max(0.0, min(1.0, r_squared))

    df = n - 2
    residual_variance = ss_res / df
    se_beta = math.sqrt(residual_variance / ss_xx) if residual_variance > 0 else 1e-12
    t_stat_beta = beta / se_beta if se_beta > 0 else 0.0

    return {
        "alpha_bps": alpha,
        "beta": beta,
        "r_squared": r_squared,
        "t_stat_beta": t_stat_beta,
        "residual_std": math.sqrt(residual_variance),
    }


def compute_event_window_returns(
    daily_returns: np.ndarray,
    event_indices: np.ndarray,
    window_pre: int = 1,
    window_post: int = 0,
) -> np.ndarray:
    """Compute cumulative equity returns across specified event windows."""
    n_days = len(daily_returns)
    n_events = len(event_indices)
    if n_events == 0:
        raise ValueError("event_indices must not be empty")

    results = np.zeros(n_events, dtype=np.float64)
    for i, idx in enumerate(event_indices):
        start_idx = idx - window_pre
        end_idx = idx + window_post
        if start_idx < 0 or end_idx >= n_days:
            raise ValueError(f"Event index {idx} violates series boundaries [0, {n_days})")

        window_slice = daily_returns[start_idx : end_idx + 1]
        gross_return = float(np.prod(1.0 + window_slice)) - 1.0
        results[i] = gross_return * 10000.0

    return results


def estimate_drift_statistics(window_returns_bps: np.ndarray) -> dict[str, float]:
    """Estimate mean, standard deviation, t-statistic, Sharpe ratio, and win rate."""
    n = len(window_returns_bps)
    if n < 2:
        raise ValueError("Need at least 2 observations to compute drift statistics")

    arr = window_returns_bps.astype(np.float64)
    mean_bps = float(np.mean(arr))
    std_bps = float(np.std(arr, ddof=1))

    se = std_bps / math.sqrt(n) if std_bps > 0 else 1e-12
    t_stat = mean_bps / se

    x = abs(t_stat)
    p_norm = math.erfc(x / math.sqrt(2.0))
    p_value = min(1.0, max(0.0, p_norm))

    annualized_sharpe = (mean_bps / std_bps * math.sqrt(8.0)) if std_bps > 1e-12 else 0.0
    win_rate = float(np.mean(arr > 0.0))

    return {
        "mean_bps": mean_bps,
        "std_bps": std_bps,
        "t_stat": t_stat,
        "p_value": p_value,
        "annualized_sharpe": annualized_sharpe,
        "win_rate": win_rate,
    }


def placebo_permutation_test(
    daily_returns: np.ndarray,
    actual_event_indices: np.ndarray,
    n_sims: int = 1000,
    seed: int = 42,
) -> tuple[float, np.ndarray]:
    """Run non-parametric placebo permutation test for pre-announcement drift."""
    rng = np.random.default_rng(seed)
    n_days = len(daily_returns)
    n_events = len(actual_event_indices)

    actual_drift_returns = daily_returns[actual_event_indices - 1] * 10000.0
    actual_mean = float(np.mean(actual_drift_returns))

    excluded = set()
    for idx in actual_event_indices:
        for offset in range(-2, 3):
            excluded.add(idx + offset)

    valid_pool = np.array([t for t in range(2, n_days - 2) if t not in excluded], dtype=int)
    if len(valid_pool) < n_events * 2:
        raise ValueError("Insufficient valid non-event days for placebo testing")

    placebo_means = np.zeros(n_sims, dtype=np.float64)
    for s in range(n_sims):
        chosen_indices = rng.choice(valid_pool, size=n_events, replace=False)
        draw_returns = daily_returns[chosen_indices - 1] * 10000.0
        placebo_means[s] = float(np.mean(draw_returns))

    abs_actual = abs(actual_mean)
    count_extreme = int(np.sum(np.abs(placebo_means) >= abs_actual))
    empirical_p_value = float(count_extreme) / float(n_sims)

    return empirical_p_value, placebo_means


def evaluate_drift_decay(
    in_sample_returns_bps: np.ndarray,
    out_of_sample_returns_bps: np.ndarray,
) -> dict[str, float]:
    """Test for post-publication decay of the pre-FOMC announcement drift."""
    n1 = len(in_sample_returns_bps)
    n2 = len(out_of_sample_returns_bps)
    if n1 < 2 or n2 < 2:
        raise ValueError("Each sample must contain at least 2 observations")

    mu1 = float(np.mean(in_sample_returns_bps))
    mu2 = float(np.mean(out_of_sample_returns_bps))

    var1 = float(np.var(in_sample_returns_bps, ddof=1))
    var2 = float(np.var(out_of_sample_returns_bps, ddof=1))

    diff = mu2 - mu1
    decay_ratio = mu2 / mu1 if abs(mu1) > 1e-12 else 0.0

    se_welch = math.sqrt(var1 / n1 + var2 / n2) if (var1 / n1 + var2 / n2) > 0 else 1e-12
    welch_t = diff / se_welch

    numerator = (var1 / n1 + var2 / n2) ** 2
    denominator = ((var1 / n1) ** 2) / (n1 - 1) + ((var2 / n2) ** 2) / (n2 - 1)
    df_welch = numerator / denominator if denominator > 0 else 1.0

    welch_p = min(1.0, max(0.0, math.erfc(abs(welch_t) / math.sqrt(2.0))))

    oos_stats = estimate_drift_statistics(out_of_sample_returns_bps)
    survived = 1.0 if (oos_stats["mean_bps"] > 0 and oos_stats["p_value"] < 0.05) else 0.0

    return {
        "in_sample_mean_bps": mu1,
        "out_of_sample_mean_bps": mu2,
        "decay_ratio": decay_ratio,
        "difference_bps": diff,
        "welch_t_stat": welch_t,
        "welch_df": df_welch,
        "welch_p_value": welch_p,
        "survived": survived,
    }
