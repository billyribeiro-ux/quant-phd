"""Student error: Omits intertemporal hedging demand, treating return predictability purely through single-period myopic demand.
"""

from __future__ import annotations

import math
from typing import Any
import numpy as np

from integrity import validate_lifecycle_params, validate_simulation_outputs


def compute_human_capital(wages: np.ndarray, r_discount: float) -> np.ndarray:
    n = len(wages)
    hc = np.zeros(n)
    for t in range(n):
        discounts = (1.0 + r_discount) ** (-np.arange(n - t))
        hc[t] = float(np.sum(wages[t:] * discounts))
    return hc


def compute_certainty_equivalent(wealth: np.ndarray, gamma: float) -> float:
    safe_w = np.maximum(wealth, 1.0)
    if abs(gamma - 1.0) < 1e-6:
        return float(math.exp(float(np.mean(np.log(safe_w)))))
    u_mean = float(np.mean((safe_w ** (1.0 - gamma)) / (1.0 - gamma)))
    return float(((1.0 - gamma) * u_mean) ** (1.0 / (1.0 - gamma)))


def compute_optimal_policy(
    t: int,
    total_years: int,
    wealth: float | np.ndarray,
    x_state: float | np.ndarray,
    hc_val: float,
    params: dict[str, Any],
) -> float | np.ndarray:
    gamma = float(params["gamma"])
    equity_vol = float(params["equity_vol"])
    equity_premium = float(params["equity_premium"])
    beta_pred = float(params["beta_pred"])
    wage_beta = float(params.get("wage_beta", 0.0))

    # Myopic allocation only
    myopic = (equity_premium + beta_pred * x_state) / (gamma * equity_vol**2)

    # MUTANT ERROR: Sets hedging demand to identically zero, ignoring Campbell-Viceira predictability effect
    hedging = 0.0

    alpha_tot = myopic + hedging
    is_scalar = np.isscalar(wealth)
    w_arr = np.maximum(np.asarray(wealth, dtype=float), 1000.0)
    hc_ratio = hc_val / w_arr
    alpha_f = alpha_tot + (alpha_tot - wage_beta) * hc_ratio

    clipped = np.clip(alpha_f, 0.0, 1.0)
    return float(clipped) if is_scalar else clipped


def simulate_lifecycle(
    params: dict[str, Any],
    policy: str = "dynamic",
    custom_glide_path: np.ndarray | None = None,
    n_paths: int = 3000,
    seed: int = 42,
) -> dict[str, Any]:
    params = validate_lifecycle_params(params)
    rng = np.random.default_rng(seed)

    initial_age = int(params["initial_age"])
    retire_age = int(params["retire_age"])
    years = retire_age - initial_age
    initial_wealth = float(params["initial_wealth"])
    initial_wage = float(params["initial_wage"])
    wage_growth = float(params["wage_growth"])
    savings_rate = float(params["savings_rate"])
    r_free = float(params["r_free"])
    equity_premium = float(params["equity_premium"])
    equity_vol = float(params["equity_vol"])
    phi = float(params["phi"])
    sigma_eta = float(params["sigma_eta"])
    rho = float(params["rho"])
    beta_pred = float(params["beta_pred"])
    gamma = float(params["gamma"])

    wages = np.zeros(years + 1)
    for t in range(years + 1):
        wages[t] = initial_wage * math.exp(wage_growth * t - 0.0003 * t**2)

    hc = compute_human_capital(wages, r_discount=r_free)
    cov_eps_eta = rho * equity_vol * sigma_eta
    cov_mat = np.array([[equity_vol**2, cov_eps_eta], [cov_eps_eta, sigma_eta**2]])
    chol = np.linalg.cholesky(cov_mat)

    z = rng.standard_normal((n_paths, years, 2))
    shocks = np.einsum("ij,nyj->nyi", chol, z)
    eps = shocks[:, :, 0]
    eta = shocks[:, :, 1]

    x = np.zeros((n_paths, years + 1))
    r_equity = np.zeros((n_paths, years))

    for t in range(years):
        r_equity[:, t] = r_free + equity_premium + beta_pred * x[:, t] + eps[:, t]
        x[:, t + 1] = phi * x[:, t] + eta[:, t]

    wealth = np.zeros((n_paths, years + 1))
    wealth[:, 0] = initial_wealth
    avg_weights = np.zeros(years)

    ages = np.arange(initial_age, retire_age)
    if policy == "to_retirement":
        det_alpha = np.zeros(years)
        for i, age in enumerate(ages):
            det_alpha[i] = 0.90 if age <= 40 else 0.90 - (0.90 - 0.30) * ((age - 40) / (retire_age - 40))
    elif policy == "through_retirement":
        det_alpha = np.zeros(years)
        for i, age in enumerate(ages):
            det_alpha[i] = 0.90 if age <= 40 else 0.90 - (0.50) * ((age - 40) / (retire_age - 40))
    elif policy == "static_60_40":
        det_alpha = np.full(years, 0.60)
    elif policy == "custom" and custom_glide_path is not None:
        det_alpha = np.asarray(custom_glide_path, dtype=float)
    else:
        det_alpha = None

    for t in range(years):
        if det_alpha is not None:
            alpha_t = det_alpha[t]
            avg_weights[t] = float(alpha_t)
            port_ret = (1.0 - alpha_t) * r_free + alpha_t * r_equity[:, t]
        else:
            alpha_t_arr = compute_optimal_policy(
                t=t,
                total_years=years,
                wealth=wealth[:, t],
                x_state=x[:, t],
                hc_val=hc[t],
                params=params,
            )
            avg_weights[t] = float(np.mean(alpha_t_arr))
            port_ret = (1.0 - alpha_t_arr) * r_free + alpha_t_arr * r_equity[:, t]

        savings = savings_rate * wages[t]
        wealth[:, t + 1] = wealth[:, t] * (1.0 + port_ret) + savings

    terminal_w = wealth[:, -1]
    mean_w = float(np.mean(terminal_w))
    median_w = float(np.median(terminal_w))
    std_w = float(np.std(terminal_w))
    p5_w = float(np.percentile(terminal_w, 5))
    ce_w = compute_certainty_equivalent(terminal_w, gamma=gamma)

    last_window = wealth[:, max(0, years - 5) :]
    peaks = np.maximum.accumulate(last_window, axis=1)
    dd = (peaks - last_window) / peaks
    p95_late_dd = float(np.percentile(np.max(dd, axis=1), 95))

    out = {
        "mean_terminal_wealth": mean_w,
        "median_terminal_wealth": median_w,
        "std_terminal_wealth": std_w,
        "p5_terminal_wealth": p5_w,
        "certainty_equivalent": ce_w,
        "max_late_drawdown_p95": p95_late_dd,
        "equity_weights": avg_weights,
    }
    validate_simulation_outputs(out)
    return out


def evaluate_tdf_comparison(
    params: dict[str, Any],
    n_paths: int = 3000,
    seed: int = 42,
) -> dict[str, Any]:
    dynamic_res = simulate_lifecycle(params, policy="dynamic", n_paths=n_paths, seed=seed)
    to_ret_res = simulate_lifecycle(params, policy="to_retirement", n_paths=n_paths, seed=seed)
    through_ret_res = simulate_lifecycle(params, policy="through_retirement", n_paths=n_paths, seed=seed)
    static_res = simulate_lifecycle(params, policy="static_60_40", n_paths=n_paths, seed=seed)

    ce_dyn = dynamic_res["certainty_equivalent"]

    return {
        "dynamic": dynamic_res,
        "to_retirement": to_ret_res,
        "through_retirement": through_ret_res,
        "static_60_40": static_res,
        "welfare_loss_to_retirement": float((to_ret_res["certainty_equivalent"] / ce_dyn - 1.0) * 100.0),
        "welfare_loss_static": float((static_res["certainty_equivalent"] / ce_dyn - 1.0) * 100.0),
    }
