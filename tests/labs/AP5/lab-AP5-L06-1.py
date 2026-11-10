"""Lab AP5-L06-1: Out-of-Sample Return Predictability and Economic Restrictions.

SIMULATED: replicates the Welch-Goyal (2008) vs Campbell-Thompson (2008) out-of-sample
predictability horse race with recursive expanding estimation and sign restrictions.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    rng = np.random.default_rng(999)
    n_obs = 240  # 240 months (20 years)
    n_init = 60  # initial burn-in window of 5 years (60 months)

    # Predictor x_t: persistent valuation ratio (AR(1) phi = 0.96)
    # Return r_{t+1} = alpha + beta * x_t + u_{t+1}
    # Mild predictability with true R^2 approx 1.5%
    phi = 0.96
    sigma_v = 0.05
    sigma_u = 0.16
    cov_uv = -0.70 * sigma_u * sigma_v
    cov_matrix = np.array([[sigma_u**2, cov_uv], [cov_uv, sigma_v**2]])

    noise = rng.multivariate_normal(mean=[0.0, 0.0], cov=cov_matrix, size=n_obs + 1)
    u = noise[:, 0]
    v = noise[:, 1]

    x = np.zeros(n_obs + 1)
    for t in range(n_obs):
        x[t + 1] = phi * x[t] + v[t + 1]

    # True return: beta = 0.06
    beta_true = 0.06
    r = 0.005 + beta_true * x[:-1] + u[1:]
    x_pred = x[:-1]

    # Recursive out-of-sample forecasting loop
    actuals = []
    bench_forecasts = []
    ols_forecasts = []
    ct_forecasts = []

    for t in range(n_init, n_obs):
        # Data available at time t: returns r[0:t] and predictors x_pred[0:t]
        y_hist = r[:t]
        x_hist = x_pred[:t]

        # 1. Historical prevailing mean benchmark
        r_bar = float(np.mean(y_hist))
        bench_forecasts.append(r_bar)

        # 2. Unconstrained OLS: r_{s+1} = a + b * x_s
        x_m = float(np.mean(x_hist))
        y_m = float(np.mean(y_hist))
        sxx = float(np.sum((x_hist - x_m) ** 2))
        sxy = float(np.sum((x_hist - x_m) * (y_hist - y_m)))
        b_hat = sxy / sxx if sxx > 1e-12 else 0.0
        a_hat = y_m - b_hat * x_m

        # Predict period t+1 return given x_pred[t]
        r_pred_ols = a_hat + b_hat * x_pred[t]
        ols_forecasts.append(r_pred_ols)

        # 3. Campbell & Thompson (2008) economically constrained forecast:
        # Constraint 1: b_hat >= 0 (positive risk premium slope)
        b_ct = max(0.0, b_hat)
        a_ct = y_m - b_ct * x_m
        r_pred_ct_raw = a_ct + b_ct * x_pred[t]
        # Constraint 2: predicted excess return >= 0
        r_pred_ct = max(0.0, r_pred_ct_raw)
        ct_forecasts.append(r_pred_ct)

        actuals.append(r[t])

    y_true = np.array(actuals)
    f_bench = np.array(bench_forecasts)
    f_ols = np.array(ols_forecasts)
    f_ct = np.array(ct_forecasts)

    # Compute Mean Squared Errors
    mse_bench = float(np.mean((y_true - f_bench) ** 2))
    mse_ols = float(np.mean((y_true - f_ols) ** 2))
    mse_ct = float(np.mean((y_true - f_ct) ** 2))

    # Out-of-sample R^2 = 1 - MSE / MSE_bench
    r2_oos_ols = 1.0 - (mse_ols / mse_bench)
    r2_oos_ct = 1.0 - (mse_ct / mse_bench)

    # Annualized mean-variance utility gain (gamma = 3)
    gamma = 3.0
    sharpe_hist = float(np.mean(y_true) / np.std(y_true, ddof=1))
    delta_u_ct = (r2_oos_ct + sharpe_hist**2) / (2.0 * gamma * (1.0 - r2_oos_ct)) * 12.0

    print("Welch & Goyal (2008) vs Campbell & Thompson (2008) OOS Test")
    print(f"Total evaluation periods:    {len(y_true)} months")
    print(f"Historical mean MSE:         {mse_bench:.6f}")
    print(f"Unconstrained OLS MSE:       {mse_ols:.6f}")
    print(f"Constrained CT MSE:          {mse_ct:.6f}")
    print(f"Unconstrained OOS R^2:       {r2_oos_ols * 100:.3f}%")
    print(f"Constrained OOS R^2:         {r2_oos_ct * 100:.3f}%")
    print(f"Annualized utility gain:     {delta_u_ct * 100:.2f}% per year")


main()
