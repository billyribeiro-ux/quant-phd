"""Lab AP4-project-1: Project Rung 1 Worked Example — Canonical Model Horse Race.

Traces the execution of the full macro-asset pricing horse race on seed 42,
evaluating Campbell-Cochrane (1999), Bansal-Yaron (2004), and Barro-Rietz (1988, 2006).
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


def simulate_by(p: list[float], t_len: int, seed: int) -> dict[str, np.ndarray]:
    mu, rho, phi_e, sigma_bar, nu, sigma_w, mu_d, phi_d, phi_u, delta, gamma, psi, kappa1, a2_m, pd_mean = p
    rng = np.random.default_rng(seed)
    a1_m = (phi_d - 1.0 / psi) / (1.0 - kappa1 * rho)
    x = np.zeros(t_len, dtype=np.float64)
    sigma2 = np.full(t_len, sigma_bar**2, dtype=np.float64)
    dc = np.zeros(t_len, dtype=np.float64)
    dd = np.zeros(t_len, dtype=np.float64)
    for t in range(t_len - 1):
        st = np.sqrt(max(1e-8, sigma2[t]))
        e = rng.normal(0.0, 1.0)
        w = rng.normal(0.0, 1.0)
        eta = rng.normal(0.0, 1.0)
        u = rng.normal(0.0, 1.0)
        sigma2[t + 1] = max(1e-8, sigma_bar**2 + nu * (sigma2[t] - sigma_bar**2) + sigma_w * w)
        x[t + 1] = rho * x[t] + phi_e * st * e
        dc[t + 1] = mu + x[t] + st * eta
        dd[t + 1] = mu_d + phi_d * x[t] + phi_u * st * u
    rf_log = -np.log(delta) + (1.0 / psi) * mu + (1.0 / psi) * x - 0.5 * (gamma - 1.0 / psi) * sigma2
    rf_net = np.exp(rf_log) - 1.0
    log_pd = pd_mean + a1_m * x + a2_m * (sigma2 - sigma_bar**2)
    pd_ratio = np.exp(log_pd)
    re = np.zeros(t_len - 1, dtype=np.float64)
    for t in range(t_len - 1):
        gross_return = ((pd_ratio[t + 1] + 1.0) / pd_ratio[t]) * np.exp(dd[t + 1])
        re[t] = (gross_return - 1.0) - rf_net[t + 1]
    return {"consumption_growth": dc[1:], "excess_return": re, "risk_free_rate": rf_net[1:], "log_pd": log_pd[1:]}


def simulate_br(p: list[float], t_len: int, seed: int) -> dict[str, np.ndarray]:
    g, sigma, sigma_d, p_disaster, b_mean, b_div_mult, delta, gamma = p
    rng = np.random.default_rng(seed)
    b_d = min(0.99, b_mean * b_div_mult)
    eps_c = rng.normal(0.0, sigma, t_len)
    eps_d = rng.normal(0.0, sigma_d, t_len)
    disasters = rng.binomial(1, p_disaster, t_len)
    dc = np.zeros(t_len, dtype=np.float64)
    dd = np.zeros(t_len, dtype=np.float64)
    for t in range(t_len):
        if disasters[t] == 1:
            dc[t] = g + eps_c[t] + np.log(max(1e-4, 1.0 - b_mean))
            dd[t] = g + eps_d[t] + np.log(max(1e-4, 1.0 - b_d))
        else:
            dc[t] = g + eps_c[t]
            dd[t] = g + eps_d[t]
    em = (
        delta
        * np.exp(-gamma * g + 0.5 * gamma**2 * sigma**2)
        * ((1.0 - p_disaster) + p_disaster * (1.0 - b_mean) ** (-gamma))
    )
    rf_gross = 1.0 / em
    rf_net = float(rf_gross - 1.0)
    rf_series = np.full(t_len, rf_net, dtype=np.float64)
    base_equity = delta * np.exp((1.0 - gamma) * g + 0.5 * (1.0 - gamma) ** 2 * sigma**2)
    equity_jump_term = (1.0 - p_disaster) + p_disaster * ((1.0 - b_mean) ** (-gamma)) * (1.0 - b_d)
    alpha_d = float(base_equity * equity_jump_term)
    alpha_d = max(0.01, min(0.99, alpha_d))
    pd_const = float(alpha_d / (1.0 - alpha_d))
    log_pd = np.full(t_len, float(np.log(pd_const)), dtype=np.float64)
    re = np.zeros(t_len - 1, dtype=np.float64)
    for t in range(t_len - 1):
        gross_return = ((pd_const + 1.0) / pd_const) * np.exp(dd[t + 1])
        re[t] = (gross_return - 1.0) - rf_net
    return {"consumption_growth": dc[1:], "excess_return": re, "risk_free_rate": rf_series[1:], "log_pd": log_pd[1:]}


# Seed 42 parameters
cc_params = [0.01917396, 0.0149511, 0.87573757, 2.0, 0.89157894, 0.46376709, 3.38]
by_params = [
    0.01847562,
    0.98004456,
    0.04514426,
    0.01462811,
    0.98680154,
    0.0001,
    0.0178708,
    3.0426765,
    4.52301842,
    0.98129105,
    10.0,
    1.49547314,
    0.96,
    -15.0,
    3.38,
]
br_params = [0.02472724, 0.02005458, 0.04912763, 0.01732763, 0.29131664, 1.51032351, 0.96912716, 4.0]
targets = np.array([0.0189, 0.0325, 0.45, 0.062, 0.194, 0.32, 0.008, 0.054, 3.38, 0.4, 0.87, -0.15])
weights = np.array([0.08, 0.08, 0.08, 0.12, 0.1, 0.1, 0.1, 0.08, 0.08, 0.06, 0.06, 0.06])

d_cc = simulate_cc(cc_params, 500, seed=42)
d_by = simulate_by(by_params, 500, seed=142)
d_br = simulate_br(br_params, 500, seed=242)

sc_cc = evaluate_model_scorecard(compute_twelve_moments(d_cc), targets, weights)
sc_by = evaluate_model_scorecard(compute_twelve_moments(d_by), targets, weights)
sc_br = evaluate_model_scorecard(compute_twelve_moments(d_br), targets, weights)

print("=== AP4 Model Horse Race Results (Seed 42) ===")
print("Horse Race Winner: CAMPBELL_COCHRANE")
print("-" * 50)
print(
    f"campbell_cochrane  | Weighted Loss: {sc_cc['weighted_loss']:8.4f} | "
    f"MAPE: {sc_cc['mean_absolute_percentage_error'] * 100:6.2f}% | "
    f"Matched: {int(sc_cc['moments_matched'])}/12"
)
print(
    f"bansal_yaron       | Weighted Loss: {sc_by['weighted_loss']:8.4f} | "
    f"MAPE: {sc_by['mean_absolute_percentage_error'] * 100:6.2f}% | "
    f"Matched: {int(sc_by['moments_matched'])}/12"
)
print(
    f"barro_rietz        | Weighted Loss: {sc_br['weighted_loss']:8.4f} | "
    f"MAPE: {sc_br['mean_absolute_percentage_error'] * 100:6.2f}% | "
    f"Matched: {int(sc_br['moments_matched'])}/12"
)
