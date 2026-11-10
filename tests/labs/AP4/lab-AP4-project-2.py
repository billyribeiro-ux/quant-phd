"""Lab AP4-project-2: Project Rung 2 Completion Problem — 12-Moment Scorecard Implementation.

Validates the complete moment extractor and weighted loss evaluation function against test fixtures.
"""

from __future__ import annotations

import numpy as np


def compute_twelve_moments(data: dict[str, np.ndarray]) -> dict[str, float]:
    dc = np.asarray(data["consumption_growth"], dtype=np.float64)
    re = np.asarray(data["excess_return"], dtype=np.float64)
    rf = np.asarray(data["risk_free_rate"], dtype=np.float64)
    pd_log = np.asarray(data["log_pd"], dtype=np.float64)

    def autocorr_lag1(series: np.ndarray) -> float:
        if len(series) < 2:
            return 0.0
        centered = series - np.mean(series)
        var = np.mean(centered**2)
        return float(np.mean(centered[1:] * centered[:-1]) / var) if var > 1e-12 else 0.0

    if len(re) > 1 and len(pd_log) > 1:
        x_pred = pd_log[:-1] - np.mean(pd_log[:-1])
        y_pred = re[1:]
        var_x = np.mean(x_pred**2)
        pred_slope = float(np.mean(x_pred * y_pred) / var_x) if var_x > 1e-12 else 0.0
    else:
        pred_slope = 0.0

    mean_re = float(np.mean(re))
    vol_re = float(np.std(re, ddof=1)) if len(re) > 1 else 0.0
    sharpe = float(mean_re / vol_re) if vol_re > 1e-8 else 0.0

    return {
        "mean_consumption_growth": float(np.mean(dc)),
        "vol_consumption_growth": float(np.std(dc, ddof=1)) if len(dc) > 1 else 0.0,
        "ac1_consumption_growth": autocorr_lag1(dc),
        "mean_equity_premium": mean_re,
        "vol_equity_return": vol_re,
        "sharpe_ratio": sharpe,
        "mean_risk_free_rate": float(np.mean(rf)),
        "vol_risk_free_rate": float(np.std(rf, ddof=1)) if len(rf) > 1 else 0.0,
        "mean_log_pd": float(np.mean(pd_log)),
        "vol_log_pd": float(np.std(pd_log, ddof=1)) if len(pd_log) > 1 else 0.0,
        "ac1_log_pd": autocorr_lag1(pd_log),
        "predictability_slope_1y": pred_slope,
    }


def evaluate_model_scorecard(moments: dict[str, float], targets: np.ndarray, weights: np.ndarray) -> dict[str, float]:
    moment_keys = [
        "mean_consumption_growth",
        "vol_consumption_growth",
        "ac1_consumption_growth",
        "mean_equity_premium",
        "vol_equity_return",
        "sharpe_ratio",
        "mean_risk_free_rate",
        "vol_risk_free_rate",
        "mean_log_pd",
        "vol_log_pd",
        "ac1_log_pd",
        "predictability_slope_1y",
    ]
    rel_errors = []
    weighted_err_sq = 0.0
    for i, k in enumerate(moment_keys):
        tgt = float(targets[i])
        w = float(weights[i])
        val = moments.get(k, 0.0)
        scale = abs(tgt) if abs(tgt) > 1e-4 else 1e-4
        rel_err = abs(val - tgt) / scale
        rel_errors.append(rel_err)
        weighted_err_sq += w * (rel_err**2)

    mape = float(np.mean(rel_errors))
    matched = sum(1 for e in rel_errors if e <= 0.50)
    return {
        "weighted_loss": float(weighted_err_sq),
        "mean_absolute_percentage_error": mape,
        "moments_matched": float(matched),
        "total_moments": 12.0,
    }


def simulate_cc(p: list[float], t_len: int, seed: int) -> dict[str, np.ndarray]:
    g, sigma, phi, gamma, delta, b_s, pd_mean = p
    rng = np.random.default_rng(seed)
    s_bar_val = sigma * np.sqrt(gamma / (1.0 - phi))
    s_bar = float(np.log(s_bar_val))
    s_max = float(s_bar + 0.5 * (1.0 - s_bar_val**2))
    s = np.zeros(t_len, dtype=np.float64)
    dc = np.zeros(t_len, dtype=np.float64)
    s[0] = s_bar
    v = rng.normal(0.0, sigma, t_len)
    for t in range(t_len - 1):
        if s[t] <= s_max:
            val_inside = max(0.0, 1.0 - 2.0 * (s[t] - s_bar))
            lam = (1.0 / s_bar_val) * np.sqrt(val_inside) - 1.0
        else:
            lam = 0.0
        dc[t + 1] = g + v[t + 1]
        s[t + 1] = (1.0 - phi) * s_bar + phi * s[t] + lam * v[t + 1]
    rf_log = -np.log(delta) + gamma * g - 0.5 * gamma * (1.0 - phi)
    rf_net = float(np.exp(rf_log) - 1.0)
    rf_series = np.full(t_len - 1, rf_net, dtype=np.float64)
    log_pd = pd_mean + b_s * (s - s_bar)
    pd_ratio = np.exp(log_pd)
    re = np.zeros(t_len - 1, dtype=np.float64)
    for t in range(t_len - 1):
        gross_return = ((pd_ratio[t + 1] + 1.0) / pd_ratio[t]) * np.exp(dc[t + 1])
        re[t] = (gross_return - 1.0) - rf_net
    return {"consumption_growth": dc[1:], "excess_return": re, "risk_free_rate": rf_series, "log_pd": log_pd[1:]}


# Setup parameters and simulation
cc_params = [0.01917396, 0.0149511, 0.87573757, 2.0, 0.89157894, 0.46376709, 3.38]
targets = np.array([0.0189, 0.0325, 0.45, 0.062, 0.194, 0.32, 0.008, 0.054, 3.38, 0.4, 0.87, -0.15])
weights = np.array([0.08, 0.08, 0.08, 0.12, 0.1, 0.1, 0.1, 0.08, 0.08, 0.06, 0.06, 0.06])

sim_data = simulate_cc(cc_params, t_len=500, seed=42)

# Extract moments and evaluate scorecard
moments = compute_twelve_moments(sim_data)
scorecard = evaluate_model_scorecard(moments, targets, weights)

print("Rung 2 Completion Verification:")
print(f"Extracted {len(moments)} moments successfully.")
print(f"Mean Absolute Percentage Error: {scorecard['mean_absolute_percentage_error'] * 100:.2f}%")
print(f"Total Weighted Loss: {scorecard['weighted_loss']:.4f}")
print(f"Moments matched within 50% tolerance: {int(scorecard['moments_matched'])}/{int(scorecard['total_moments'])}")
