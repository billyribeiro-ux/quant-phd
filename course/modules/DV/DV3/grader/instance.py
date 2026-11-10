"""Instance generator for DV3: Stochastic & Rough Volatility.

Generates deterministic market instances across seeds 0-49:
- Heston model parameters satisfying the Feller condition 2*kappa*theta > xi^2.
- SABR model parameters for forward volatility smile evaluation.
- Forward variance curve and 1-factor Bergomi model parameters.
- High-frequency realized log-volatility time series with fractional roughness H in (0.08, 0.18)
  simulated via exact Cholesky factorization of the fractional covariance matrix,
  plus calibrated microstructure measurement noise.
All simulated data is labeled SIMULATED.
All dictionary values are numeric primitives or lists of numeric primitives for deterministic reproducibility.
"""

from __future__ import annotations

import math
import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Return a deterministic market instance for the given integer seed."""
    rng = random.Random(seed)

    spot = round(95.0 + rng.random() * 20.0, 2)
    rate = round(0.02 + rng.random() * 0.025, 4)

    # 1. Heston Parameters satisfying Feller condition
    kappa = round(1.8 + rng.random() * 1.2, 4)
    theta = round(0.035 + rng.random() * 0.015, 4)
    v0 = round(0.030 + rng.random() * 0.020, 4)
    max_xi = math.sqrt(2.0 * kappa * theta * 0.70)
    xi = round(0.18 + rng.random() * (max_xi - 0.18), 4)
    rho_heston = round(-0.75 + rng.random() * 0.25, 4)

    strikes = [round(spot * factor, 2) for factor in [0.80, 0.90, 1.00, 1.10, 1.20]]
    maturities = [0.05, 0.25, 0.50, 1.00]

    # 2. SABR Parameters
    sabr_alpha = round(1.8 + rng.random() * 0.6, 4)
    sabr_beta = round(0.40 + rng.random() * 0.30, 4)
    sabr_rho = round(-0.45 + rng.random() * 0.25, 4)
    sabr_nu = round(0.30 + rng.random() * 0.20, 4)

    # 3. Forward Variance Curve & Bergomi Parameters
    fwd_tenors = [0.25, 0.50, 1.00, 2.00]
    fwd_variances = [
        round(0.038 + rng.random() * 0.006, 5),
        round(0.044 + rng.random() * 0.006, 5),
        round(0.050 + rng.random() * 0.006, 5),
        round(0.056 + rng.random() * 0.006, 5),
    ]
    fwd_curve = [(t, v) for t, v in zip(fwd_tenors, fwd_variances, strict=True)]
    bergomi_omega = round(1.8 + rng.random() * 0.6, 4)
    bergomi_kappa = round(3.0 + rng.random() * 2.0, 4)

    # 4. Rough Volatility Log-RV Time Series (SIMULATED) via Exact Cholesky fBm
    true_h = round(0.09 + rng.random() * 0.08, 4)
    n_days = 200
    dt = 1.0 / n_days

    cov: list[list[float]] = [[0.0] * n_days for _ in range(n_days)]
    for i in range(n_days):
        ti = (i + 1) * dt
        for j in range(i + 1):
            tj = (j + 1) * dt
            diff = abs(ti - tj)
            cov[i][j] = 0.5 * (ti ** (2.0 * true_h) + tj ** (2.0 * true_h) - diff ** (2.0 * true_h))
            cov[j][i] = cov[i][j]

    l_mat: list[list[float]] = [[0.0] * n_days for _ in range(n_days)]
    for i in range(n_days):
        for j in range(i + 1):
            s_sum = sum(l_mat[i][k] * l_mat[j][k] for k in range(j))
            if i == j:
                diag = cov[i][i] - s_sum
                l_mat[i][j] = math.sqrt(max(1e-12, diag))
            else:
                l_mat[i][j] = (cov[i][j] - s_sum) / l_mat[j][j]

    z = [rng.gauss(0.0, 1.0) for _ in range(n_days)]
    mu, nu_scale = -3.0, 0.60
    clean_log_rv: list[float] = []
    for i in range(n_days):
        fbm_val = sum(l_mat[i][j] * z[j] for j in range(i + 1))
        clean_log_rv.append(round(mu + nu_scale * fbm_val, 6))

    # Add microstructure measurement noise
    noise_sigma = round(0.035 + rng.random() * 0.020, 4)
    noisy_log_rv = [round(c + rng.gauss(0.0, noise_sigma), 6) for c in clean_log_rv]

    lags = [1, 2, 3, 4, 5, 6, 8, 10, 15, 20]

    return {
        "seed": seed,
        "label": "SIMULATED",
        "spot": spot,
        "rate": rate,
        "strikes": strikes,
        "maturities": maturities,
        "heston_v0": v0,
        "heston_kappa": kappa,
        "heston_theta": theta,
        "heston_xi": xi,
        "heston_rho": rho_heston,
        "sabr_alpha": sabr_alpha,
        "sabr_beta": sabr_beta,
        "sabr_rho": sabr_rho,
        "sabr_nu": sabr_nu,
        "forward_curve": fwd_curve,
        "bergomi_omega": bergomi_omega,
        "bergomi_kappa": bergomi_kappa,
        "true_h": true_h,
        "noise_sigma": noise_sigma,
        "clean_log_rv": clean_log_rv,
        "noisy_log_rv": noisy_log_rv,
        "lags": lags,
    }
