"""Lab GM1-L03-1: Ragged-Edge Kalman Filter Nowcasting.

Applies the Kalman filter with missing-observation selection matrices (Giannone,
Reichlin & Small 2008) to handle asynchronous macroeconomic release schedules.
Demonstrates the monotonic reduction in nowcast variance as incoming monthly data
fills the ragged edge of a current-quarter panel.
"""

from __future__ import annotations

import numpy as np


def run_ragged_kalman_filter(
    y_ragged: np.ndarray,
    mat_a: np.ndarray,
    loadings: np.ndarray,
    q_cov: np.ndarray,
    r_cov: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Run Kalman filter handling missing values (NaN) with row selection matrices."""
    t_len, _ = y_ragged.shape
    r_dim = mat_a.shape[0]

    state_mean = np.zeros(r_dim, dtype=np.float64)
    state_cov = np.eye(r_dim, dtype=np.float64)

    filtered_states = np.zeros((t_len, r_dim), dtype=np.float64)
    filtered_covs = np.zeros((t_len, r_dim, r_dim), dtype=np.float64)

    for t in range(t_len):
        # 1. Prediction step
        pred_mean = state_mean if t == 0 else mat_a @ state_mean
        pred_cov = state_cov if t == 0 else mat_a @ state_cov @ mat_a.T + q_cov

        # 2. Measurement update
        obs_mask = np.isfinite(y_ragged[t])
        n_obs = int(np.sum(obs_mask))

        if n_obs == 0:
            state_mean = pred_mean
            state_cov = pred_cov
        else:
            y_star = y_ragged[t, obs_mask]
            lambda_star = loadings[obs_mask, :]
            r_star = r_cov[obs_mask, :][:, obs_mask]

            innov = y_star - lambda_star @ pred_mean
            innov_cov = lambda_star @ pred_cov @ lambda_star.T + r_star

            kalman_gain = pred_cov @ lambda_star.T @ np.linalg.inv(innov_cov)
            state_mean = pred_mean + kalman_gain @ innov
            state_cov = (np.eye(r_dim) - kalman_gain @ lambda_star) @ pred_cov
            state_cov = 0.5 * (state_cov + state_cov.T)

        filtered_states[t] = state_mean
        filtered_covs[t] = state_cov

    return filtered_states, filtered_covs


def main() -> None:
    print("GM1 Lab L03-1: Ragged-Edge Kalman Nowcasting & Uncertainty [SIMULATED]")
    print("===================================================================")

    rng = np.random.default_rng(202)
    t_len = 12
    n_vars = 6  # 6 monthly indicators informing GDP growth
    r_dim = 1  # 1 common activity factor

    # State transition & measurement model
    mat_a = np.array([[0.80]], dtype=np.float64)
    q_cov = np.array([[0.36]], dtype=np.float64)
    loadings = np.array([[0.9], [0.85], [0.75], [0.70], [0.65], [0.60]], dtype=np.float64)
    r_diag = np.array([0.19, 0.28, 0.44, 0.51, 0.58, 0.64], dtype=np.float64)
    r_cov = np.diag(r_diag)

    # Generate synthetic observations
    factors = np.zeros((t_len, r_dim), dtype=np.float64)
    for t in range(1, t_len):
        factors[t] = mat_a @ factors[t - 1] + rng.normal(0, np.sqrt(q_cov[0, 0]))

    raw_y = factors @ loadings.T + rng.normal(0, np.sqrt(r_diag), size=(t_len, n_vars))

    # Evaluate nowcast variance at terminal quarter T-1 under 3 sequential information releases:
    # Release 1 (Month 1): Only fast indicators (financial / surveys, vars 0-1) available
    y_rel1 = raw_y.copy()
    y_rel1[-1, 2:] = np.nan

    # Release 2 (Month 2): Mid-quarter indicators (industrial production / retail sales, vars 2-3) arrive
    y_rel2 = raw_y.copy()
    y_rel2[-1, 4:] = np.nan

    # Release 3 (Month 3): Full quarter complete (all indicators 0-5 available)
    y_rel3 = raw_y.copy()

    _, covs1 = run_ragged_kalman_filter(y_rel1, mat_a, loadings, q_cov, r_cov)
    _, covs2 = run_ragged_kalman_filter(y_rel2, mat_a, loadings, q_cov, r_cov)
    _, covs3 = run_ragged_kalman_filter(y_rel3, mat_a, loadings, q_cov, r_cov)

    var1 = float(covs1[-1, 0, 0])
    var2 = float(covs2[-1, 0, 0])
    var3 = float(covs3[-1, 0, 0])

    # Pre-release prior uncertainty before any month-t observation
    prior_var = float(mat_a[0, 0] ** 2 * covs1[-2, 0, 0] + q_cov[0, 0])

    print("Nowcast Uncertainty Evolution Through Current Quarter:")
    print("-------------------------------------------------------------------")
    print(f"Prior Forecast Variance (T-1|T-2):           {prior_var:7.4f}")
    print(f"Vintage 1 (Month 1 Surveys, 2/6 vars):       {var1:7.4f}  (std: {np.sqrt(var1):.4f})")
    print(f"Vintage 2 (Month 2 Hard Data, 4/6 vars):     {var2:7.4f}  (std: {np.sqrt(var2):.4f})")
    print(f"Vintage 3 (Month 3 Complete Panel, 6/6 vars):{var3:7.4f}  (std: {np.sqrt(var3):.4f})")
    print("-------------------------------------------------------------------")

    variance_reduction = (1.0 - var3 / prior_var) * 100.0
    print(f"Total Uncertainty Reduction from Prior:      {variance_reduction:5.2f}%")

    # Verification: Monotonic decrease in posterior error variance
    assert prior_var > var1 > var2 > var3, "Nowcast variance must strictly decrease as data arrives"
    print("Monotonic reduction in nowcast uncertainty:   True")


main()
