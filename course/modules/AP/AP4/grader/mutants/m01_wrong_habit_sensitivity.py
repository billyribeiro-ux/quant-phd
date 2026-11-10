"""Mutant: introduces time-varying risk-free rate into Campbell-Cochrane, violating constant risk-free rate."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import numpy as np

CC_PARAM_NAMES = ("g", "sigma", "phi", "gamma", "delta", "b_s", "pd_mean")

BY_PARAM_NAMES = (
    "mu",
    "rho",
    "phi_e",
    "sigma_bar",
    "nu",
    "sigma_w",
    "mu_d",
    "phi_d",
    "phi_u",
    "delta",
    "gamma",
    "psi",
    "kappa1",
    "a2_m",
    "pd_mean",
)

BR_PARAM_NAMES = ("g", "sigma", "sigma_d", "p_disaster", "b_mean", "b_div_mult", "delta", "gamma")

MOMENT_NAMES = (
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
)


def _to_dict(params: Any, keys: tuple[str, ...]) -> dict[str, float]:
    """Helper to convert array or dict to standardized dict."""
    if isinstance(params, Mapping):
        return {k: float(params[k]) for k in keys if k in params}
    arr = np.asarray(params, dtype=np.float64).ravel()
    return {k: float(arr[i]) for i, k in enumerate(keys) if i < len(arr)}


def compute_twelve_moments(data: dict[str, np.ndarray]) -> dict[str, float]:
    """Compute the 12 canonical macro-finance data moments from simulation time series."""
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

    # 1-year predictive regression slope: excess return re[t+1] on log(P/D)[t]
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


def simulate_campbell_cochrane(params: Any, t_len: int, seed: int) -> dict[str, np.ndarray]:
    """Simulate the Campbell-Cochrane (1999) external habit model."""
    p = _to_dict(params, CC_PARAM_NAMES)
    rng = np.random.default_rng(seed)

    g = p["g"]
    sigma = p["sigma"]
    phi = p["phi"]
    gamma = p["gamma"]
    delta = p["delta"]
    b_s = p.get("b_s", 0.48)
    pd_mean = p.get("pd_mean", 3.38)

    # Steady state surplus consumption ratio
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

    # By construction of lambda(s), the real risk-free rate is constant:
    rf_log = -np.log(delta) + gamma * g - 0.5 * gamma * (1.0 - phi)
    rf_net = float(np.exp(rf_log) - 1.0)
    rf_series = np.full(t_len - 1, rf_net, dtype=np.float64) + 0.05 * v[1:]

    # Log price-dividend ratio increases with the surplus consumption ratio
    log_pd = pd_mean + b_s * (s - s_bar)
    pd_ratio = np.exp(log_pd)

    # Gross equity returns and excess returns
    re = np.zeros(t_len - 1, dtype=np.float64)
    for t in range(t_len - 1):
        gross_return = ((pd_ratio[t + 1] + 1.0) / pd_ratio[t]) * np.exp(dc[t + 1])
        re[t] = (gross_return - 1.0) - rf_net

    return {
        "consumption_growth": dc[1:],
        "excess_return": re,
        "risk_free_rate": rf_series,
        "log_pd": log_pd[1:],
    }


def simulate_bansal_yaron(params: Any, t_len: int, seed: int) -> dict[str, np.ndarray]:
    """Simulate the Bansal-Yaron (2004) long-run risks model."""
    p = _to_dict(params, BY_PARAM_NAMES)
    rng = np.random.default_rng(seed)

    mu = p["mu"]
    rho = p["rho"]
    phi_e = p["phi_e"]
    sigma_bar = p["sigma_bar"]
    nu = p["nu"]
    sigma_w = p.get("sigma_w", 0.0001)
    mu_d = p.get("mu_d", 0.0180)
    phi_d = p["phi_d"]
    phi_u = p["phi_u"]
    delta = p["delta"]
    gamma = p["gamma"]
    psi = p["psi"]
    kappa1 = p.get("kappa1", 0.96)
    a2_m = p.get("a2_m", -15.0)
    pd_mean = p.get("pd_mean", 3.38)

    # Analytical sensitivity coefficient of valuation to long-run expected growth
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

    # Time-varying risk-free rate
    rf_log = -np.log(delta) + (1.0 / psi) * mu + (1.0 / psi) * x - 0.5 * (gamma - 1.0 / psi) * sigma2
    rf_net = np.exp(rf_log) - 1.0

    # Log price-dividend ratio
    log_pd = pd_mean + a1_m * x + a2_m * (sigma2 - sigma_bar**2)
    pd_ratio = np.exp(log_pd)

    # Gross equity returns and excess returns
    re = np.zeros(t_len - 1, dtype=np.float64)
    for t in range(t_len - 1):
        gross_return = ((pd_ratio[t + 1] + 1.0) / pd_ratio[t]) * np.exp(dd[t + 1])
        re[t] = (gross_return - 1.0) - rf_net[t + 1]

    return {
        "consumption_growth": dc[1:],
        "excess_return": re,
        "risk_free_rate": rf_net[1:],
        "log_pd": log_pd[1:],
    }


def simulate_barro_rietz(params: Any, t_len: int, seed: int) -> dict[str, np.ndarray]:
    """Simulate the Barro-Rietz (1988, 2006) rare disasters model."""
    p = _to_dict(params, BR_PARAM_NAMES)
    rng = np.random.default_rng(seed)

    g = p["g"]
    sigma = p["sigma"]
    sigma_d = p.get("sigma_d", 0.050)
    p_disaster = p["p_disaster"]
    b_mean = p["b_mean"]
    b_div_mult = p.get("b_div_mult", 1.5)
    delta = p["delta"]
    gamma = p["gamma"]

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

    # Precautionary pricing kernel expectation for risk-free bond
    em = (
        delta
        * np.exp(-gamma * g + 0.5 * gamma**2 * sigma**2)
        * ((1.0 - p_disaster) + p_disaster * (1.0 - b_mean) ** (-gamma))
    )
    rf_gross = 1.0 / max(1e-8, em)
    rf_net = float(rf_gross - 1.0)
    rf_series = np.full(t_len - 1, rf_net, dtype=np.float64)

    # Equilibrium price-dividend ratio
    alpha_d = (
        delta
        * np.exp((1.0 - gamma) * g + 0.5 * (1.0 - gamma) ** 2 * sigma**2)
        * ((1.0 - p_disaster) + p_disaster * ((1.0 - b_mean) ** (-gamma)) * (1.0 - b_d))
    )
    alpha_d = min(0.999, max(1e-4, alpha_d))
    pd_val = alpha_d / (1.0 - alpha_d)
    log_pd = np.full(t_len - 1, np.log(pd_val), dtype=np.float64)

    # Gross equity returns and excess returns
    re = np.zeros(t_len - 1, dtype=np.float64)
    for t in range(t_len - 1):
        gross_return = ((pd_val + 1.0) / pd_val) * np.exp(dd[t + 1])
        re[t] = (gross_return - 1.0) - rf_net

    return {
        "consumption_growth": dc[1:],
        "excess_return": re,
        "risk_free_rate": rf_series,
        "log_pd": log_pd,
    }


def evaluate_model_scorecard(
    sim_moments: Any,
    target_moments: Any,
    weights: Any = None,
) -> dict[str, Any]:
    """Evaluate simulated moments against empirical target moments, computing scorecard metrics."""
    sim_dict = _to_dict(sim_moments, MOMENT_NAMES)
    tgt_dict = _to_dict(target_moments, MOMENT_NAMES)
    w_dict = _to_dict(weights, MOMENT_NAMES) if weights is not None else {}

    abs_errors: dict[str, float] = {}
    rel_errors: dict[str, float] = {}
    total_weighted_loss = 0.0

    for key, target in tgt_dict.items():
        sim_val = sim_dict.get(key, 0.0)
        diff = abs(sim_val - target)
        abs_errors[key] = float(diff)
        denom = abs(target) if abs(target) > 1e-4 else 1e-4
        rel = float(diff / denom)
        rel_errors[key] = rel

        w = w_dict.get(key, 1.0 / len(tgt_dict))
        total_weighted_loss += w * (rel**2)

    mape = float(np.mean(list(rel_errors.values()))) if rel_errors else 0.0
    passed_count = sum(1 for r in rel_errors.values() if r <= 0.50)

    return {
        "sim_moments": sim_dict,
        "absolute_errors": abs_errors,
        "relative_errors": rel_errors,
        "mean_absolute_percentage_error": mape,
        "weighted_loss": float(total_weighted_loss),
        "moments_matched": passed_count,
        "total_moments": len(tgt_dict),
    }


def run_horse_race(instance: dict[str, Any]) -> dict[str, Any]:
    """Run full horse race comparing Campbell-Cochrane, Bansal-Yaron, and Barro-Rietz on 12 moments."""
    t_len = int(instance["t_len"])
    seed = int(instance["seed"])
    targets = instance["targets"]
    weights = instance.get("weights")

    data_cc = simulate_campbell_cochrane(instance["cc_params"], t_len, seed)
    data_by = simulate_bansal_yaron(instance["by_params"], t_len, seed + 100)
    data_br = simulate_barro_rietz(instance["br_params"], t_len, seed + 200)

    moments_cc = compute_twelve_moments(data_cc)
    moments_by = compute_twelve_moments(data_by)
    moments_br = compute_twelve_moments(data_br)

    scorecard_cc = evaluate_model_scorecard(moments_cc, targets, weights)
    scorecard_by = evaluate_model_scorecard(moments_by, targets, weights)
    scorecard_br = evaluate_model_scorecard(moments_br, targets, weights)

    models_scores: dict[str, float] = {
        "campbell_cochrane": scorecard_cc["weighted_loss"],
        "bansal_yaron": scorecard_by["weighted_loss"],
        "barro_rietz": scorecard_br["weighted_loss"],
    }

    winner = min(models_scores, key=models_scores.get)  # type: ignore[arg-type]

    return {
        "scorecards": {
            "campbell_cochrane": scorecard_cc,
            "bansal_yaron": scorecard_by,
            "barro_rietz": scorecard_br,
        },
        "winner": winner,
        "models_scores": models_scores,
    }
