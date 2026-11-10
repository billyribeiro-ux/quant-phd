"""Lab SR3-L01-1: CoVaR and Delta-CoVaR Estimation via Quantile Regression.

SIMULATED: generates synthetic financial institution and systemic equity returns
to estimate conditional Value-at-Risk (CoVaR) and marginal systemic contribution
(Delta-CoVaR) following Adrian and Brunnermeier (2016).
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import linprog


def fit_quantile_regression(y: np.ndarray, x: np.ndarray, q: float) -> np.ndarray:
    """Solve linear quantile regression via linear programming."""
    t_obs, k_vars = x.shape
    c = np.concatenate([np.zeros(k_vars), q * np.ones(t_obs), (1.0 - q) * np.ones(t_obs)])
    eye_t = np.eye(t_obs)
    a_eq = np.hstack([x, eye_t, -eye_t])
    bounds = [(None, None)] * k_vars + [(0.0, None)] * (2 * t_obs)
    res = linprog(c, A_eq=a_eq, b_eq=y, bounds=bounds, method="highs")
    if not res.success:
        raise ValueError(f"Quantile optimization failed: {res.message}")
    return np.asarray(res.x[:k_vars], dtype=np.float64)


def main() -> None:
    # Deterministic synthetic sample calibration (T=500 daily observations)
    rng = np.random.default_rng(101)
    t_obs = 500

    # Macro state variable: market volatility index proxy (mean zero, AR(1))
    vol_state = np.zeros(t_obs)
    for t in range(1, t_obs):
        vol_state[t] = 0.65 * vol_state[t - 1] + rng.normal(0.0, 0.01)

    # Institution returns R_i (high beta financial institution)
    # R_i,t = alpha_i + gamma_i * M_t-1 + eps_i,t
    eps_i = rng.standard_t(df=4, size=t_obs) * 0.015
    r_inst = 0.0004 - 0.25 * vol_state + eps_i

    # System returns R_sys (financial sector aggregate)
    # R_sys,t = alpha_s + beta_s * R_i,t + gamma_s * M_t-1 + eps_s,t
    eps_s = rng.standard_t(df=4, size=t_obs) * 0.010
    r_sys = 0.0002 + 0.60 * r_inst - 0.15 * vol_state + eps_s

    # Design matrices
    ones = np.ones((t_obs, 1))
    x_inst = np.column_stack([ones, vol_state])
    x_sys = np.column_stack([ones, r_inst, vol_state])

    # 1. Institution VaR at q = 0.05 (crisis) and q = 0.50 (median)
    beta_inst_05 = fit_quantile_regression(r_inst, x_inst, q=0.05)
    beta_inst_50 = fit_quantile_regression(r_inst, x_inst, q=0.50)

    # Evaluate at sample average volatility (vol_mean = 0)
    eval_state = np.array([1.0, float(np.mean(vol_state))])
    var_inst_05 = float(np.dot(beta_inst_05, eval_state))
    var_inst_50 = float(np.dot(beta_inst_50, eval_state))

    # 2. System CoVaR quantile regression at q = 0.05
    beta_sys_05 = fit_quantile_regression(r_sys, x_sys, q=0.05)
    alpha_sys = beta_sys_05[0]
    beta_sys = beta_sys_05[1]
    gamma_sys = beta_sys_05[2]

    # CoVaR conditional on institution at 5% VaR vs median VaR
    covar_05 = float(alpha_sys + beta_sys * var_inst_05 + gamma_sys * eval_state[1])
    covar_50 = float(alpha_sys + beta_sys * var_inst_50 + gamma_sys * eval_state[1])
    delta_covar = covar_05 - covar_50

    # 3. OLS Benchmark for comparison
    ols_sys = np.linalg.lstsq(x_sys, r_sys, rcond=None)[0]

    print("=== CoVaR and Delta-CoVaR Estimation (Adrian & Brunnermeier 2016) ===")
    print(f"Observations (T): {t_obs}")
    print(f"Institution VaR(0.05): {var_inst_05:.4f} (-{abs(var_inst_05) * 100:.2f}%)")
    print(f"Institution VaR(0.50): {var_inst_50:.4f} (+{var_inst_50 * 100:.2f}%)")
    print(f"Quantile Regression beta(0.05): {beta_sys:.4f}")
    print(f"OLS Regression beta: {ols_sys[1]:.4f}")
    print(f"System CoVaR(0.05 | Inst VaR 0.05): {covar_05:.4f}")
    print(f"System CoVaR(0.05 | Inst Median):   {covar_50:.4f}")
    print(f"Delta-CoVaR(0.05):                  {delta_covar:.4f} ({delta_covar * 10000:.1f} bps)")


main()
