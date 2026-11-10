"""Lab AP4-L07-1: Multi-model canonical horse-race synthesis and comparison.

Simulates Campbell-Cochrane, Bansal-Yaron, and Barro-Rietz on a standardized seed
and compares their performance on the equity premium, risk-free rate, and valuation volatility.
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
        if var <= 1e-12:
            return 0.0
        return float(np.mean(centered[1:] * centered[:-1]) / var)

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


def simulate_cc(t_len: int, seed: int) -> dict[str, np.ndarray]:
    g, sigma, phi, gamma, delta = 0.0189, 0.0150, 0.87, 2.0, 0.89
    b_s, pd_mean = 0.48, 3.38
    rng = np.random.default_rng(seed)

    s_bar_val = sigma * np.sqrt(gamma / (1.0 - phi))
    s_bar = float(np.log(s_bar_val))
    s_max = float(s_bar + 0.5 * (1.0 - s_bar_val**2))

    s = np.zeros(t_len, dtype=np.float64)
    dc = np.zeros(t_len, dtype=np.float64)
    s[0] = s_bar
    v = rng.normal(0.0, sigma, t_len)

    for t in range(t_len - 1):
        lam = (1.0 / s_bar_val) * np.sqrt(max(0.0, 1.0 - 2.0 * (s[t] - s_bar))) - 1.0 if s[t] <= s_max else 0.0
        s[t + 1] = (1.0 - phi) * s_bar + phi * s[t] + lam * v[t + 1]

    dc = g + v
    rf_const = -np.log(delta) + gamma * g - 0.5 * gamma * (1.0 - phi)
    rf = np.full(t_len, rf_const, dtype=np.float64)
    pd_log = pd_mean + b_s * (s - s_bar)

    re = np.zeros(t_len, dtype=np.float64)
    for t in range(t_len - 1):
        p_ratio = np.exp(pd_log[t + 1] - pd_log[t])
        re[t] = p_ratio * np.exp(dc[t + 1]) - np.exp(rf[t])
    re[-1] = re[-2]

    return {"consumption_growth": dc, "excess_return": re, "risk_free_rate": rf, "log_pd": pd_log}


def simulate_by(t_len: int, seed: int) -> dict[str, np.ndarray]:
    mu, rho, phi_e, sigma_bar, nu, sigma_w = 0.0180, 0.979, 0.044, 0.015, 0.987, 0.0000023
    mu_d, phi_d, phi_u, delta, gamma, psi, kappa1 = 0.0180, 3.0, 4.5, 0.99, 10.0, 1.5, 0.96
    a2_m, pd_mean = -15.0, 3.38
    rng = np.random.default_rng(seed)

    x = np.zeros(t_len, dtype=np.float64)
    sigma2 = np.full(t_len, sigma_bar**2, dtype=np.float64)
    eta = rng.normal(0.0, 1.0, t_len)
    e = rng.normal(0.0, 1.0, t_len)
    w = rng.normal(0.0, 1.0, t_len)
    u = rng.normal(0.0, 1.0, t_len)

    for t in range(t_len - 1):
        st = float(np.sqrt(max(1e-8, sigma2[t])))
        x[t + 1] = rho * x[t] + phi_e * st * e[t + 1]
        sigma2[t + 1] = max(1e-8, sigma_bar**2 + nu * (sigma2[t] - sigma_bar**2) + sigma_w * w[t + 1])

    st_arr = np.sqrt(np.maximum(1e-8, sigma2))
    dc = mu + x + st_arr * eta
    dd = mu_d + phi_d * x + phi_u * st_arr * u

    a1_m = (phi_d - 1.0 / psi) / (1.0 - kappa1 * rho)
    pd_log = pd_mean + a1_m * x + a2_m * (sigma2 - sigma_bar**2)

    rf0 = -np.log(delta) + mu / psi
    rf = rf0 + (1.0 / psi) * x - 0.5 * (gamma - 1.0 / psi) * (sigma2 - sigma_bar**2)

    re = np.zeros(t_len, dtype=np.float64)
    for t in range(t_len - 1):
        p_ratio = np.exp(pd_log[t + 1] - pd_log[t])
        ret = p_ratio * np.exp(dd[t + 1]) - np.exp(rf[t])
        re[t] = ret
    re[-1] = re[-2]

    return {"consumption_growth": dc, "excess_return": re, "risk_free_rate": rf, "log_pd": pd_log}


def simulate_br(t_len: int, seed: int) -> dict[str, np.ndarray]:
    g, sigma, sigma_d, p_disaster, b_mean, b_div_mult, delta, gamma = (
        0.025,
        0.020,
        0.050,
        0.017,
        0.29,
        1.5,
        0.97,
        4.0,
    )
    rng = np.random.default_rng(seed)

    eps_c = rng.normal(0.0, sigma, t_len)
    eps_d = rng.normal(0.0, sigma_d, t_len)
    jump = rng.binomial(1, p_disaster, t_len)

    b_div = min(0.99, b_mean * b_div_mult)
    dc = g + eps_c + np.log(1.0 - b_mean) * jump
    dd = g + eps_d + np.log(1.0 - b_div) * jump

    base_disc = delta * np.exp(-gamma * g + 0.5 * (gamma**2) * (sigma**2))
    prec_term = (1.0 - p_disaster) + p_disaster * ((1.0 - b_mean) ** (-gamma))
    em = base_disc * prec_term
    rf_val = float(-np.log(em))
    rf = np.full(t_len, rf_val, dtype=np.float64)

    base_eq = delta * np.exp((1.0 - gamma) * g + 0.5 * ((1.0 - gamma) ** 2) * (sigma**2))
    eq_jump = (1.0 - p_disaster) + p_disaster * ((1.0 - b_mean) ** (-gamma)) * (1.0 - b_div)
    alpha_d = float(base_eq * eq_jump)
    alpha_d = max(0.01, min(0.99, alpha_d))
    pd_const = float(alpha_d / (1.0 - alpha_d))
    pd_log = np.full(t_len, float(np.log(pd_const)), dtype=np.float64)

    re = np.zeros(t_len, dtype=np.float64)
    for t in range(t_len - 1):
        div_growth = np.exp(dd[t + 1])
        ret = ((pd_const + 1.0) / pd_const) * div_growth - np.exp(rf[t])
        re[t] = ret
    re[-1] = re[-2]

    return {"consumption_growth": dc, "excess_return": re, "risk_free_rate": rf, "log_pd": pd_log}


t_len = 500
data_cc = simulate_cc(t_len, seed=42)
data_by = simulate_by(t_len, seed=142)
data_br = simulate_br(t_len, seed=242)

m_cc = compute_twelve_moments(data_cc)
m_by = compute_twelve_moments(data_by)
m_br = compute_twelve_moments(data_br)

targets_map = {
    "mean_consumption_growth": 0.0189,
    "vol_consumption_growth": 0.0325,
    "ac1_consumption_growth": 0.4500,
    "mean_equity_premium": 0.0620,
    "vol_equity_return": 0.1940,
    "sharpe_ratio": 0.3200,
    "mean_risk_free_rate": 0.0080,
    "vol_risk_free_rate": 0.0540,
    "mean_log_pd": 3.3800,
    "vol_log_pd": 0.4000,
    "ac1_log_pd": 0.8700,
    "predictability_slope_1y": -0.1500,
}

print(f"{'Moment':<24} | {'Target':<7} | {'C-C (1999)':<10} | {'B-Y (2004)':<10} | {'B-R (2006)':<10}")
print("-" * 72)

key_moments = [
    ("mean_equity_premium", "Equity Premium"),
    ("vol_equity_return", "Equity Vol"),
    ("sharpe_ratio", "Sharpe Ratio"),
    ("mean_risk_free_rate", "Mean Rf"),
    ("vol_risk_free_rate", "Vol Rf"),
    ("mean_log_pd", "Mean log(P/D)"),
    ("vol_log_pd", "Vol log(P/D)"),
    ("predictability_slope_1y", "Predict Slope"),
]

for raw_k, label in key_moments:
    tgt = targets_map[raw_k]
    cc_val = m_cc[raw_k]
    by_val = m_by[raw_k]
    br_val = m_br[raw_k]
    print(f"{label:<24} | {tgt:7.4f} | {cc_val:10.4f} | {by_val:10.4f} | {br_val:10.4f}")
