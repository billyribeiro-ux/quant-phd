"""Instance generator for the AP5 present value & return predictability autograder.

SIMULATED: generates synthetic asset return panels, valuation ratios, and
predictive regression series for testing Campbell-Shiller variance decompositions.
Labelled SIMULATED per BLUEPRINT §5.3.

Deterministic per seed; valid by construction.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic test instance for a given integer seed."""
    rng = np.random.default_rng(seed)

    # 1. Sample dimensions and parameters
    n_obs = 150  # 150 annual observations
    rho = float(0.95 + 0.02 * rng.uniform(-1.0, 1.0))  # discount parameter in [0.93, 0.97]

    # 2. Calibrated 2-variable VAR(1) parameters: z_t = [r_t, dp_t]^T
    # Persistent valuation ratio with return predictability (Cochrane 2011 calibration)
    phi_01 = float(0.12 + 0.02 * rng.uniform(-1.0, 1.0))  # return slope
    phi_11 = float(0.93 + 0.02 * rng.uniform(-1.0, 1.0))  # dp persistence
    phi_00 = float(0.01 * rng.uniform(-1.0, 1.0))
    phi_10 = float(-0.01 * rng.uniform(0.0, 1.0))
    phi_mat = np.array([[phi_00, phi_01], [phi_10, phi_11]], dtype=np.float64)

    # Stationary intercepts
    dp_bar = -3.20 + 0.20 * rng.uniform(-1.0, 1.0)
    r_bar = 0.08 + 0.02 * rng.uniform(-1.0, 1.0)
    c_vec = (np.eye(2) - phi_mat) @ np.array([r_bar, dp_bar], dtype=np.float64)

    # Innovation covariance
    sigma_u = float(0.18 + 0.03 * rng.uniform(-1.0, 1.0))
    sigma_v = float(0.14 + 0.03 * rng.uniform(-1.0, 1.0))
    rho_uv = float(-0.75 + 0.10 * rng.uniform(-1.0, 1.0))
    cov_uv = rho_uv * sigma_u * sigma_v
    cov_mat = np.array([[sigma_u**2, cov_uv], [cov_uv, sigma_v**2]], dtype=np.float64)

    # Simulate VAR path
    eps = rng.multivariate_normal(mean=[0.0, 0.0], cov=cov_mat, size=n_obs + 1)
    z = np.zeros((n_obs + 1, 2), dtype=np.float64)
    z[0] = np.array([r_bar, dp_bar], dtype=np.float64)
    for t in range(n_obs):
        z[t + 1] = c_vec + phi_mat @ z[t] + eps[t + 1]

    # 3. Dedicated predictive regression series under known parameters
    pred_t = 180
    pred_phi = float(0.94 + 0.02 * rng.uniform(-1.0, 1.0))
    pred_beta = float(0.05 + 0.03 * rng.uniform(-1.0, 1.0))
    pred_noise = rng.multivariate_normal(
        mean=[0.0, 0.0],
        cov=[[0.0324, -0.018], [-0.018, 0.0196]],
        size=pred_t + 1,
    )
    pred_x = np.zeros(pred_t + 1, dtype=np.float64)
    pred_x[0] = -3.0
    for t in range(pred_t):
        pred_x[t + 1] = -3.0 * (1.0 - pred_phi) + pred_phi * pred_x[t] + pred_noise[t + 1, 1]
    pred_y = 0.02 + pred_beta * pred_x[:-1] + pred_noise[1:, 0]

    # 4. Out-of-sample validation series
    oos_t = 160
    oos_x = pred_x[:oos_t]
    oos_y = pred_y[:oos_t]

    return {
        "seed": seed,
        "n_obs": n_obs,
        "rho": rho,
        "var_data": z.tolist(),
        "phi_true": phi_mat.tolist(),
        "cov_true": cov_mat.tolist(),
        "predictive_x": pred_x[:-1].tolist(),
        "predictive_y": pred_y.tolist(),
        "oos_x": oos_x.tolist(),
        "oos_y": oos_y.tolist(),
        "oos_burn_in": 50,
    }
