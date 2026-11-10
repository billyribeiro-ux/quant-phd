"""Lab S2-L12-1: Monte Carlo simulation of Stambaugh bias in predictive regressions.

Evaluates finite-sample upward bias in predictive OLS regressions where the
predictive regressor is persistent (rho = 0.95) and its innovations are negatively
correlated with return shocks (corr = -0.80), comparing empirical bias against
the theoretical Stambaugh (1999) formula and Kendall (1954) AR(1) bias.

Standard library only.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    rng = random.Random(42)
    sample_size = 120  # 10 years of monthly data
    replications = 3000
    rho_true = 0.95
    beta_true = 0.00  # Null hypothesis: no return predictability
    corr_uv = -0.80
    var_v = 1.00
    cov_uv = corr_uv * var_v

    beta_estimates: list[float] = []
    rho_estimates: list[float] = []
    rej_onesided = 0
    rej_twosided = 0

    for _ in range(replications):
        # Burn-in to reach stationary distribution
        x_cur = 0.0
        for _ in range(50):
            v_burn = rng.gauss(0.0, 1.0)
            x_cur = rho_true * x_cur + v_burn

        x: list[float] = [0.0] * sample_size
        y: list[float] = [0.0] * sample_size

        for t in range(sample_size):
            # Bivariate Gaussian innovations with correlation corr_uv
            z1 = rng.gauss(0.0, 1.0)
            z2 = rng.gauss(0.0, 1.0)
            v = z1
            u = corr_uv * z1 + math.sqrt(1.0 - corr_uv**2) * z2

            x[t] = x_cur
            y[t] = beta_true * x_cur + u
            x_cur = rho_true * x_cur + v

        # OLS estimation of y on x
        x_bar = sum(x) / sample_size
        y_bar = sum(y) / sample_size
        sxx = sum((xt - x_bar) ** 2 for xt in x)
        sxy = sum((xt - x_bar) * (yt - y_bar) for xt, yt in zip(x, y, strict=True))
        b_hat = sxy / sxx
        beta_estimates.append(b_hat)

        # OLS estimation of AR(1) persistence rho
        x_lag = x[:-1]
        x_lead = x[1:]
        n_ar = sample_size - 1
        x_lag_bar = sum(x_lag) / n_ar
        x_lead_bar = sum(x_lead) / n_ar
        s_lag_lag = sum((xt - x_lag_bar) ** 2 for xt in x_lag)
        s_lag_lead = sum((xt - x_lag_bar) * (yt - x_lead_bar) for xt, yt in zip(x_lag, x_lead, strict=True))
        r_hat = s_lag_lead / s_lag_lag
        rho_estimates.append(r_hat)

        # Hypothesis testing
        resids = [yt - (y_bar + b_hat * (xt - x_bar)) for xt, yt in zip(x, y, strict=True)]
        s2 = sum(r**2 for r in resids) / (sample_size - 2)
        se_b = math.sqrt(s2 / sxx)
        t_stat = b_hat / se_b

        if t_stat > 1.645:
            rej_onesided += 1
        if abs(t_stat) > 1.96:
            rej_twosided += 1

    emp_mean_rho = sum(rho_estimates) / replications
    emp_bias_rho = emp_mean_rho - rho_true
    kendall_theory = -(1.0 + 3.0 * rho_true) / sample_size

    emp_mean_beta = sum(beta_estimates) / replications
    stambaugh_theory = (cov_uv / var_v) * emp_bias_rho

    rate_onesided = rej_onesided / replications
    rate_twosided = rej_twosided / replications

    print("Metric                 | Theoretical | Empirical Simulation")
    print("-" * 55)
    print(f"AR(1) Persistence Bias |     {kendall_theory:+.4f} |              {emp_bias_rho:+.4f}")
    print(f"Predictive Slope Bias  |     {stambaugh_theory:+.4f} |              {emp_mean_beta:+.4f}")
    print(f"One-sided Rej (alpha=0.05) |      0.0500 |              {rate_onesided:.4f}")
    print(f"Two-sided Rej (alpha=0.05) |      0.0500 |              {rate_twosided:.4f}")


main()
