"""Lab AP2-L06-1: Jensen's alpha, beta, and time-series inference.

SIMULATED panel of T = 120 monthly observations (seed 42).
Computes OLS estimates for alpha and beta, residual variance with T-2 degrees of freedom,
standard error of alpha, and the t-statistic testing the null hypothesis alpha = 0.
Compares closed forms against normal equations.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    rng = random.Random(42)
    t_obs = 120

    # True data-generating process: alpha = 0.001 (10 bps/month), beta = 1.15
    true_alpha = 0.001
    true_beta = 1.15
    true_sigma_e = 0.025  # 2.5% monthly idiosyncratic volatility

    # Market excess return: mean 0.0065, std 0.045
    r_m = [rng.gauss(0.0065, 0.045) for _ in range(t_obs)]
    r_i = [true_alpha + true_beta * r_m[t] + rng.gauss(0.0, true_sigma_e) for t in range(t_obs)]

    # Closed-form OLS formulas
    mean_m = sum(r_m) / float(t_obs)
    mean_i = sum(r_i) / float(t_obs)
    s_mm = sum((m - mean_m) ** 2 for m in r_m)
    s_im = sum((r_m[t] - mean_m) * (r_i[t] - mean_i) for t in range(t_obs))

    beta_hat = s_im / s_mm
    alpha_hat = mean_i - beta_hat * mean_m

    residuals = [r_i[t] - (alpha_hat + beta_hat * r_m[t]) for t in range(t_obs)]
    sse = sum(e * e for e in residuals)
    df = t_obs - 2
    s2 = sse / float(df)
    var_alpha = s2 * (1.0 / float(t_obs) + (mean_m * mean_m) / s_mm)
    se_alpha = math.sqrt(var_alpha)
    t_stat = alpha_hat / se_alpha

    # Normal equations check:
    # [ T       sum(r_m)   ] [ alpha ] = [ sum(r_i)     ]
    # [ sum(r_m) sum(r_m^2) ] [ beta  ]   [ sum(r_i*r_m) ]
    sum_m = sum(r_m)
    sum_m2 = sum(m * m for m in r_m)
    sum_i = sum(r_i)
    sum_im = sum(r_i[t] * r_m[t] for t in range(t_obs))
    det = float(t_obs) * sum_m2 - sum_m * sum_m
    norm_alpha = (sum_m2 * sum_i - sum_m * sum_im) / det
    norm_beta = (float(t_obs) * sum_im - sum_m * sum_i) / det

    print("--- SIMULATED Jensen Regression (T = 120) ---")
    print(f"Sample length T:             {t_obs}")
    print(f"Sample mean excess market:   {mean_m:.6f}")
    print(f"Sample mean excess asset:    {mean_i:.6f}")
    print(f"Estimated beta (closed):     {beta_hat:.6f}")
    print(f"Estimated beta (normal eq):  {norm_beta:.6f}")
    print(f"Estimated alpha (closed):    {alpha_hat:.6f}")
    print(f"Estimated alpha (normal eq): {norm_alpha:.6f}")
    print(f"Residual variance s^2:       {s2:.8f}")
    print(f"Residual std s:              {math.sqrt(s2):.6f}")
    print(f"Standard error se(alpha):    {se_alpha:.6f}")
    print(f"t-statistic (H0: alpha = 0): {t_stat:.4f}")
    print(f"Agreement within 1e-12:      {abs(alpha_hat - norm_alpha) < 1e-12 and abs(beta_hat - norm_beta) < 1e-12}")


main()
