"""Instance generator for FI2: Affine term-structure model calibration.

Generates a SIMULATED 3-factor Gaussian affine term-structure model dataset
including true factor parameters, state transition matrices, measurement noise,
latent factor trajectories, and observed yield curves over T periods.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a reproducible simulated 3-factor Gaussian ATSM curve instance.

    Parameters
    ----------
    seed : int
        Pseudorandom seed for reproducible instance generation.

    Returns
    -------
    dict[str, Any]
        Dictionary containing observation dimensions, maturities, true parameters,
        simulated latent factors, and observed yield matrix.
    """
    rng = np.random.default_rng(seed)

    # Observation dimensions
    n_periods = 60  # 60 monthly periods (5 years)
    tau = np.array([0.25, 0.5, 1.0, 2.0, 5.0, 10.0], dtype=np.float64)  # 6 tenors in years
    n_maturities = len(tau)

    # Risk-neutral parameters (Q-measure)
    # delta0: baseline instantaneous short rate intercept (around 2% to 4%)
    delta0 = float(0.025 + 0.01 * (rng.uniform(-0.5, 0.5)))

    # kappa: mean reversion speeds (strictly ordered: level < slope < curvature)
    kappa1 = float(0.06 + 0.02 * rng.uniform(-0.5, 0.5))
    kappa2 = float(0.28 + 0.05 * rng.uniform(-0.5, 0.5))
    kappa3 = float(0.85 + 0.10 * rng.uniform(-0.5, 0.5))
    kappa = np.array([kappa1, kappa2, kappa3], dtype=np.float64)

    # sigma: factor volatilities
    sigma1 = float(0.010 + 0.002 * rng.uniform(-0.5, 0.5))
    sigma2 = float(0.014 + 0.002 * rng.uniform(-0.5, 0.5))
    sigma3 = float(0.018 + 0.003 * rng.uniform(-0.5, 0.5))
    sigma = np.array([sigma1, sigma2, sigma3], dtype=np.float64)

    # Physical parameters (P-measure discrete-time VAR(1))
    # X_{t+1} = c + Phi * X_t + eta_{t+1}, eta ~ N(0, Q)
    c_vec = np.array([0.0001, -0.0002, 0.0001], dtype=np.float64)
    phi_diag = np.array(
        [
            0.98 + 0.01 * rng.uniform(-0.5, 0.5),
            0.92 + 0.02 * rng.uniform(-0.5, 0.5),
            0.80 + 0.03 * rng.uniform(-0.5, 0.5),
        ],
        dtype=np.float64,
    )
    phi_mat = np.diag(phi_diag)

    # Transition covariance Q (monthly dt = 1/12)
    dt = 1.0 / 12.0
    q_diag = sigma**2 * dt
    q_mat = np.diag(q_diag)

    # Measurement noise: 5 bps standard deviation
    meas_std = 0.0005  # 5 bps
    r_diag = np.full(n_maturities, meas_std**2, dtype=np.float64)

    # Solve Riccati ODEs to obtain yield loadings: y(t, tau) = a(tau) + H(tau) * X_t
    b_mat = np.zeros((n_maturities, 3), dtype=np.float64)
    a_vec = np.zeros(n_maturities, dtype=np.float64)
    for m in range(n_maturities):
        tm = tau[m]
        for i in range(3):
            ki = kappa[i]
            si = sigma[i]
            b_mat[m, i] = -(1.0 - np.exp(-ki * tm)) / ki
            # Analytical integral of B_i(s)^2 from 0 to tm
            int_b2 = (1.0 / (ki**2)) * (
                tm - 2.0 * (1.0 - np.exp(-ki * tm)) / ki + (1.0 - np.exp(-2.0 * ki * tm)) / (2.0 * ki)
            )
            a_vec[m] += 0.5 * (si**2) * int_b2
        a_vec[m] -= delta0 * tm

    a_yield = -a_vec / tau
    h_yield = -b_mat / tau[:, np.newaxis]

    # Compute unconditional state distribution for initialization
    # V0 = Phi V0 Phi^T + Q -> vec(V0) = (I - Phi (x) Phi)^(-1) vec(Q)
    i_kron = np.eye(9) - np.kron(phi_mat, phi_mat)
    v0_mat = np.linalg.solve(i_kron, q_mat.flatten()).reshape((3, 3))
    # Symmetrize V0
    v0_mat = 0.5 * (v0_mat + v0_mat.T)
    mean_x0 = np.linalg.solve(np.eye(3) - phi_mat, c_vec)

    # Simulate latent state trajectory X_t
    x_states = np.zeros((n_periods, 3), dtype=np.float64)
    # Initial state from stationary distribution
    x_states[0] = rng.multivariate_normal(mean_x0, v0_mat)
    for t in range(1, n_periods):
        eta = rng.multivariate_normal(np.zeros(3), q_mat)
        x_states[t] = c_vec + phi_mat @ x_states[t - 1] + eta

    # Simulate observed yields: y_t = a + H * X_t + v_t
    v_noise = rng.normal(0.0, meas_std, size=(n_periods, n_maturities))
    yields = np.zeros((n_periods, n_maturities), dtype=np.float64)
    for t in range(n_periods):
        yields[t] = a_yield + h_yield @ x_states[t] + v_noise[t]

    return {
        "seed": seed,
        "T": n_periods,
        "M": n_maturities,
        "tau": tau.tolist(),
        "delta0": delta0,
        "kappa": kappa.tolist(),
        "sigma": sigma.tolist(),
        "c": c_vec.tolist(),
        "phi": phi_mat.tolist(),
        "Q": q_mat.tolist(),
        "R_diag": r_diag.tolist(),
        "a_yield": a_yield.tolist(),
        "H_yield": h_yield.tolist(),
        "true_states": x_states.tolist(),
        "yields": yields.tolist(),
    }
