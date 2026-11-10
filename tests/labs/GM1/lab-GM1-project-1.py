"""GM1 project lab 1 (rung 2 completion): Full Dynamic Factor Nowcasting Pipeline.

Fits a Stock-Watson dynamic factor model on balanced historical macro data,
filters an asynchronous ragged-edge current-quarter panel using the Kalman filter,
and generates the target GDP growth nowcast and posterior uncertainty.
"""

from __future__ import annotations

import numpy as np


class DynamicFactorNowcaster:
    """Dynamic Factor Model with ragged-edge Kalman filtering."""

    def __init__(self, n_factors: int = 2) -> None:
        self.n_factors = n_factors
        self.mean_: np.ndarray | None = None
        self.std_: np.ndarray | None = None
        self.loadings_: np.ndarray | None = None
        self.trans_a_: np.ndarray | None = None
        self.trans_q_: np.ndarray | None = None
        self.meas_r_: np.ndarray | None = None
        self.beta_: np.ndarray | None = None

    def fit(self, x_balanced: np.ndarray, y_target: np.ndarray) -> DynamicFactorNowcaster:
        """Fit factor loadings, VAR(1) transition, and target regression."""
        t_obs, _ = x_balanced.shape
        self.mean_ = np.mean(x_balanced, axis=0)
        self.std_ = np.std(x_balanced, axis=0, ddof=1)
        x_std = (x_balanced - self.mean_) / self.std_

        cov = (x_std.T @ x_std) / float(t_obs)
        eigvals, eigvecs = np.linalg.eigh(cov)
        idx = np.argsort(eigvals)[::-1]
        top_eigvecs = eigvecs[:, idx[: self.n_factors]]
        self.loadings_ = top_eigvecs.copy()

        factors = x_std @ top_eigvecs
        f_curr = factors[1:]
        f_prev = factors[:-1]
        trans_a, _, _, _ = np.linalg.lstsq(f_prev, f_curr, rcond=None)
        self.trans_a_ = trans_a.T

        resids = f_curr - f_prev @ trans_a
        q_cov = (resids.T @ resids) / float(len(resids) - 1)
        self.trans_q_ = 0.5 * (q_cov + q_cov.T) + 1e-6 * np.eye(self.n_factors)

        e_resid = x_std - factors @ top_eigvecs.T
        r_diag = np.maximum(np.var(e_resid, axis=0, ddof=1), 1e-4)
        self.meas_r_ = np.diag(r_diag)

        beta, _, _, _ = np.linalg.lstsq(factors, y_target, rcond=None)
        self.beta_ = beta
        return self

    def filter_ragged(self, x_ragged: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Kalman filter on ragged-edge data with missing values."""
        assert self.mean_ is not None and self.std_ is not None
        assert self.loadings_ is not None and self.trans_a_ is not None
        assert self.trans_q_ is not None and self.meas_r_ is not None

        t_len, _ = x_ragged.shape
        r_dim = self.n_factors
        x_std = np.full_like(x_ragged, np.nan, dtype=np.float64)
        valid = np.isfinite(x_ragged)
        mean_tile = np.tile(self.mean_, (t_len, 1))
        std_tile = np.tile(self.std_, (t_len, 1))
        x_std[valid] = (x_ragged[valid] - mean_tile[valid]) / std_tile[valid]

        filtered_factors = np.zeros((t_len, r_dim), dtype=np.float64)
        filtered_covs = np.zeros((t_len, r_dim, r_dim), dtype=np.float64)
        state_mean = np.zeros(r_dim, dtype=np.float64)
        state_cov = np.eye(r_dim, dtype=np.float64)

        for t in range(t_len):
            pred_mean = state_mean if t == 0 else self.trans_a_ @ state_mean
            pred_cov = state_cov if t == 0 else self.trans_a_ @ state_cov @ self.trans_a_.T + self.trans_q_

            obs_mask = np.isfinite(x_std[t])
            if np.any(obs_mask):
                y_star = x_std[t, obs_mask]
                lambda_star = self.loadings_[obs_mask, :]
                r_star = self.meas_r_[obs_mask, :][:, obs_mask]
                innov = y_star - lambda_star @ pred_mean
                innov_cov = lambda_star @ pred_cov @ lambda_star.T + r_star
                kalman_gain = pred_cov @ lambda_star.T @ np.linalg.inv(innov_cov)
                state_mean = pred_mean + kalman_gain @ innov
                state_cov = (np.eye(r_dim) - kalman_gain @ lambda_star) @ pred_cov
                state_cov = 0.5 * (state_cov + state_cov.T)
            else:
                state_mean, state_cov = pred_mean, pred_cov

            filtered_factors[t] = state_mean
            filtered_covs[t] = state_cov

        return filtered_factors, filtered_covs

    def nowcast(self, x_ragged: np.ndarray) -> tuple[float, float]:
        """Return point nowcast and posterior standard deviation."""
        assert self.beta_ is not None
        factors, covs = self.filter_ragged(x_ragged)
        term_factor = factors[-1]
        term_cov = covs[-1]
        point_est = float(np.dot(self.beta_, term_factor))
        post_var = float(self.beta_ @ term_cov @ self.beta_)
        return point_est, float(np.sqrt(post_var))


def main() -> None:
    print("GM1 Project Lab 1: End-to-End Nowcasting Pipeline [SIMULATED]")
    print("=============================================================")

    rng = np.random.default_rng(404)
    t_hist = 120
    t_rag = 12
    n_vars = 8
    n_factors = 2

    # Simulate balanced history
    true_factors = np.zeros((t_hist, n_factors), dtype=np.float64)
    mat_a = np.array([[0.75, 0.05], [-0.05, 0.65]], dtype=np.float64)
    for t in range(1, t_hist):
        true_factors[t] = mat_a @ true_factors[t - 1] + rng.normal(0, 0.5, size=n_factors)

    loadings = rng.uniform(0.5, 0.9, size=(n_vars, n_factors))
    hist_x = true_factors @ loadings.T + rng.normal(0, 0.3, size=(t_hist, n_vars))
    target_y = 1.4 * true_factors[:, 0] - 0.5 * true_factors[:, 1] + rng.normal(0, 0.2, size=t_hist)

    # Ragged-edge panel
    ragged_factors = np.zeros((t_rag, n_factors), dtype=np.float64)
    for t in range(1, t_rag):
        ragged_factors[t] = mat_a @ ragged_factors[t - 1] + rng.normal(0, 0.5, size=n_factors)
    ragged_x = ragged_factors @ loadings.T + rng.normal(0, 0.3, size=(t_rag, n_vars))

    # Introduce asynchronous publication delays (ragged edge at terminal rows)
    ragged_x[-2, [3, 5, 7]] = np.nan
    ragged_x[-1, [0, 2, 3, 5, 6, 7]] = np.nan

    model = DynamicFactorNowcaster(n_factors=n_factors)
    model.fit(hist_x, target_y)
    point_est, post_se = model.nowcast(ragged_x)

    print(f"Balanced History Sample:     T = {t_hist}, N = {n_vars}")
    print(f"Ragged-Edge Panel Sample:    T = {t_rag}, N = {n_vars}")
    print("Terminal Month Missing:      6 of 8 indicators unreleased")
    print("-------------------------------------------------------------")
    print(f"Target GDP Growth Nowcast:   {point_est:6.3f}%")
    print(f"Posterior Standard Error:    {post_se:6.3f}%")
    print(f"95% Confidence Interval:     [{point_est - 1.96 * post_se:6.3f}%, {point_est + 1.96 * post_se:6.3f}%]")
    print("-------------------------------------------------------------")
    print("Nowcast pipeline execution:  True")


main()
