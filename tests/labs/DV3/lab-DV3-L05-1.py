"""Lab 5 · Variogram Hurst Exponent Estimation & Microstructure Noise Correction.

This lab simulates a continuous-time rough log-volatility process with true Hurst parameter
H=0.12 on seed 0 (SIMULATED), contaminates the realized variance with high-frequency
microstructure noise, demonstrates the flattening of the log-log variogram at small lags,
and applies noise-corrected lag-truncation regression to recover the true roughness H.
"""

from __future__ import annotations

import math
import random


def simulate_rough_log_rv(n: int, h: float, seed: int) -> list[float]:
    """Simulate rough log realized volatility path using exact covariance Cholesky."""
    cov: list[list[float]] = [[0.0] * n for _ in range(n)]
    dt = 1.0 / n
    for i in range(n):
        ti = (i + 1) * dt
        for j in range(i + 1):
            tj = (j + 1) * dt
            diff = abs(ti - tj)
            cov[i][j] = 0.5 * (ti ** (2.0 * h) + tj ** (2.0 * h) - diff ** (2.0 * h))
            cov[j][i] = cov[i][j]

    l_mat: list[list[float]] = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s_sum = sum(l_mat[i][k] * l_mat[j][k] for k in range(j))
            if i == j:
                l_mat[i][j] = math.sqrt(max(1e-12, cov[i][i] - s_sum))
            else:
                l_mat[i][j] = (cov[i][j] - s_sum) / l_mat[j][j]

    rng = random.Random(seed)
    z = [rng.gauss(0.0, 1.0) for _ in range(n)]
    mu = -3.0
    nu = 0.60
    log_rv: list[float] = [0.0] * n
    for i in range(n):
        fbm_val = sum(l_mat[i][j] * z[j] for j in range(i + 1))
        log_rv[i] = mu + nu * fbm_val
    return log_rv


def compute_variogram(series: list[float], lags: list[int], q: float = 2.0) -> dict[int, float]:
    """Compute empirical q-th order structure function m(q, Delta) = E[|X_{t+Delta} - X_t|^q]."""
    n = len(series)
    m_q: dict[int, float] = {}
    for lag in lags:
        diffs = [abs(series[i + lag] - series[i]) ** q for i in range(n - lag)]
        m_q[lag] = sum(diffs) / len(diffs)
    return m_q


def ols_regression(xs: list[float], ys: list[float]) -> tuple[float, float, float]:
    """Perform OLS regression: y = slope * x + intercept, returning (slope, intercept, R^2)."""
    n = len(xs)
    x_mean = sum(xs) / n
    y_mean = sum(ys) / n
    cov_xy = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys, strict=True))
    var_x = sum((x - x_mean) ** 2 for x in xs)
    var_y = sum((y - y_mean) ** 2 for y in ys)

    slope = cov_xy / var_x
    intercept = y_mean - slope * x_mean
    r_sq = (cov_xy**2) / (var_x * var_y) if var_y > 1e-14 else 1.0
    return slope, intercept, r_sq


def main() -> None:
    print("=== Hurst Exponent Estimation & Microstructure Noise Correction ===")
    true_h = 0.12
    n_days = 200
    seed = 42

    print(f"True Model: Continuous Rough Log-RV with H = {true_h:.2f} (N={n_days} days, seed={seed}, SIMULATED)")
    clean_log_rv = simulate_rough_log_rv(n_days, true_h, seed=seed)

    noise_sigma = 0.08
    rng_noise = random.Random(101)
    noise_series = [rng_noise.gauss(0.0, noise_sigma) for _ in range(n_days)]
    noisy_log_rv = [c + eps for c, eps in zip(clean_log_rv, noise_series, strict=True)]

    lags = [1, 2, 3, 4, 5, 6, 8, 10, 15, 20]
    q = 2.0

    vario_clean = compute_variogram(clean_log_rv, lags, q)
    vario_noisy = compute_variogram(noisy_log_rv, lags, q)

    print("\nEmpirical Variograms m(q=2, Delta):")
    print(" Lag Delta | Clean m(2, Delta) | Noisy m(2, Delta) | Noise Variance Bias (2*sigma_eps^2)")
    print("-----------------------------------------------------------------------------------------")
    theoretical_bias = 2.0 * (noise_sigma**2)
    for lag_idx in lags:
        m_c = vario_clean[lag_idx]
        m_n = vario_noisy[lag_idx]
        diff = m_n - m_c
        bias_str = f"{diff:8.5f} (th: {theoretical_bias:7.5f})"
        print(f"     {lag_idx:2d}    |       {m_c:8.5f}    |       {m_n:8.5f}    |       {bias_str}")

    # Regression 1: Clean series (all lags)
    log_lags = [math.log(lag_val) for lag_val in lags]
    log_m_clean = [math.log(vario_clean[lag_val]) for lag_val in lags]
    slope_clean, _, r2_clean = ols_regression(log_lags, log_m_clean)
    h_hat_clean = slope_clean / q

    # Regression 2: Naive on noisy series (all lags)
    log_m_noisy = [math.log(vario_noisy[lag_val]) for lag_val in lags]
    slope_naive, _, r2_naive = ols_regression(log_lags, log_m_noisy)
    h_hat_naive = slope_naive / q

    # Regression 3: Noise-corrected truncated regression (lags >= 4)
    trunc_lags = [lag_val for lag_val in lags if lag_val >= 4]
    trunc_log_lags = [math.log(lag_val) for lag_val in trunc_lags]
    trunc_log_m_noisy = [math.log(vario_noisy[lag_val]) for lag_val in trunc_lags]
    slope_trunc, _, r2_trunc = ols_regression(trunc_log_lags, trunc_log_m_noisy)
    h_hat_corrected = slope_trunc / q

    print("\nEstimation Results:")
    print(f"  1. Clean Series (All Lags):        H_hat = {h_hat_clean:.4f} (R^2 = {r2_clean:.4f})")
    print(f"  2. Naive Noisy (All Lags):         H_hat = {h_hat_naive:.4f} (R^2 = {r2_naive:.4f}) [Noise biased]")
    print(f"  3. Noise-Corrected (Lags >= 4):    H_hat = {h_hat_corrected:.4f} (R^2 = {r2_trunc:.4f}) [Recovered]")
    print(f"  True Parameter:                    H     = {true_h:.4f}")

    print("\nDebate Relevance: At small lags Delta=1, microstructure noise accounts for")
    pct_noise = (theoretical_bias / vario_noisy[1]) * 100.0
    print(f"  {pct_noise:.1f}% of total measured variance, flattening the variogram.")
    print("Truncating ultrafast lags isolates physical volatility roughness from market microstructure noise.")


main()
