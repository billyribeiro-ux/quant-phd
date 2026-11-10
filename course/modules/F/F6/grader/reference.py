"""Reference solution for F6: Machine Learning in Asset Pricing (ml_study.py).

Implements:
- compute_oos_r2: Out-of-sample R-squared with zero benchmark per Gu, Kelly & Xiu (2020).
- construct_spread_portfolio: Long-short spread quantile portfolio with linear transaction cost deduction.
- evaluate_complexity_curve: Overparameterized random features regression testing the Kelly et al. (2024)
  virtue-of-complexity / double-descent hypothesis.
- run_ml_study: Comprehensive cross-sectional asset pricing benchmark comparing linear,
  tree, and neural models with purged cross-validation.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
from atlas_ml import (
    NeuralNetworkRegressor,
    PurgedKFold,
    RandomForestRegressor,
    RidgeRegressor,
)

__all__ = [
    "compute_oos_r2",
    "construct_spread_portfolio",
    "evaluate_complexity_curve",
    "run_ml_study",
]


def compute_oos_r2(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute out-of-sample R-squared with zero return benchmark.

    Parameters
    ----------
    y_true : np.ndarray
        Realized excess returns of shape (N, T) or (M,).
    y_pred : np.ndarray
        Predicted excess returns of matching shape.

    Returns
    -------
    float
        R2_OOS = 1.0 - sum((y_true - y_pred)**2) / sum(y_true**2).
    """
    y_t = np.asarray(y_true, dtype=np.float64)
    y_p = np.asarray(y_pred, dtype=np.float64)

    if y_t.shape != y_p.shape:
        raise ValueError(f"Shape mismatch: y_true {y_t.shape} vs y_pred {y_p.shape}")
    if y_t.size == 0:
        raise ValueError("y_true and y_pred cannot be empty")

    denom = float(np.sum(y_t**2))
    if denom <= 1e-15:
        raise ValueError("Sum of squared true returns is near zero")

    num = float(np.sum((y_t - y_p) ** 2))
    return float(1.0 - (num / denom))


def construct_spread_portfolio(
    predictions: np.ndarray,
    returns: np.ndarray,
    cost_bps: float = 15.0,
) -> dict[str, float]:
    """Construct top-bottom quantile long-short spread portfolio net of costs.

    Parameters
    ----------
    predictions : np.ndarray
        Model return predictions of shape (N, T).
    returns : np.ndarray
        Realized excess returns of shape (N, T).
    cost_bps : float, default=15.0
        Round-trip transaction cost in basis points.

    Returns
    -------
    dict[str, float]
        Dictionary of portfolio performance metrics.
    """
    preds = np.asarray(predictions, dtype=np.float64)
    rets = np.asarray(returns, dtype=np.float64)

    if preds.shape != rets.shape:
        raise ValueError(f"Shape mismatch: predictions {preds.shape} vs returns {rets.shape}")
    if preds.ndim != 2:
        raise ValueError(f"Expected 2-dimensional arrays (N, T), got {preds.ndim} dimensions")
    if cost_bps < 0.0:
        raise ValueError(f"cost_bps must be non-negative, got {cost_bps}")

    n_assets, n_periods = preds.shape
    if n_assets < 2:
        raise ValueError("n_assets must be at least 2")
    if n_periods < 2:
        raise ValueError("n_periods must be at least 2")

    k_quant = max(1, n_assets // 3)
    gross_returns = np.zeros(n_periods, dtype=np.float64)
    net_returns = np.zeros(n_periods, dtype=np.float64)
    turnovers = np.zeros(n_periods, dtype=np.float64)

    cost_factor = cost_bps * 1e-4
    prev_weights = np.zeros(n_assets, dtype=np.float64)

    for t in range(n_periods):
        scores = preds[:, t]
        order = np.argsort(scores)

        weights = np.zeros(n_assets, dtype=np.float64)
        short_idx = order[:k_quant]
        long_idx = order[-k_quant:]

        weights[long_idx] = 1.0 / k_quant
        weights[short_idx] = -1.0 / k_quant

        turnover = float(np.sum(np.abs(weights - prev_weights)))
        cost = turnover * cost_factor

        r_gross = float(np.dot(weights, rets[:, t]))
        r_net = r_gross - cost

        gross_returns[t] = r_gross
        net_returns[t] = r_net
        turnovers[t] = turnover
        prev_weights = weights

    gross_mean = float(np.mean(gross_returns))
    gross_vol = float(np.std(gross_returns, ddof=1))
    gross_sharpe = float(math.sqrt(12.0) * (gross_mean / gross_vol)) if gross_vol > 1e-8 else 0.0

    net_mean = float(np.mean(net_returns))
    net_vol = float(np.std(net_returns, ddof=1))
    net_sharpe = float(math.sqrt(12.0) * (net_mean / net_vol)) if net_vol > 1e-8 else 0.0

    return {
        "gross_mean": gross_mean,
        "gross_vol": gross_vol,
        "gross_sharpe": gross_sharpe,
        "net_mean": net_mean,
        "net_vol": net_vol,
        "net_sharpe": net_sharpe,
        "mean_turnover": float(np.mean(turnovers)),
    }


def evaluate_complexity_curve(
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_test: np.ndarray,
    y_test: np.ndarray,
    gammas: list[float],
    seed: int = 42,
) -> dict[str, list[float]]:
    """Evaluate overparameterized random feature regression across complexity ratios.

    Implements the Kelly, Malamud & Zhou (2024) / Hastie et al. double-descent framework.

    Parameters
    ----------
    x_train : np.ndarray
        Training features of shape (N, T_train, P) or (M_train, P).
    y_train : np.ndarray
        Training returns of shape (N, T_train) or (M_train,).
    x_test : np.ndarray
        Testing features of shape (N, T_test, P) or (M_test, P).
    y_test : np.ndarray
        Testing returns of shape (N, T_test) or (M_test,).
    gammas : list[float]
        List of complexity parameter ratios P_dim / M_samples.
    seed : int, default=42
        RNG seed for random feature projections.

    Returns
    -------
    dict[str, list[float]]
        Dictionary containing 'gammas', 'ridgeless_mse', 'ridgeless_r2',
        'regularized_mse', and 'regularized_r2'.
    """
    x_tr = np.asarray(x_train, dtype=np.float64)
    y_tr = np.asarray(y_train, dtype=np.float64)
    x_te = np.asarray(x_test, dtype=np.float64)
    y_te = np.asarray(y_test, dtype=np.float64)

    if x_tr.ndim == 3:
        n_a, t_tr, n_f = x_tr.shape
        x_tr = x_tr.transpose(1, 0, 2).reshape(t_tr * n_a, n_f)
        y_tr = y_tr.T.reshape(t_tr * n_a)
    elif x_tr.ndim == 2:
        n_f = x_tr.shape[1]
        y_tr = y_tr.flatten()
    else:
        raise ValueError("X_train must be 2D or 3D")

    if x_te.ndim == 3:
        n_a, t_te, _ = x_te.shape
        x_te = x_te.transpose(1, 0, 2).reshape(t_te * n_a, n_f)
        y_te = y_te.T.reshape(t_te * n_a)
    elif x_te.ndim == 2:
        y_te = y_te.flatten()
    else:
        raise ValueError("X_test must be 2D or 3D")

    m_samples = len(y_tr)
    rng = np.random.default_rng(seed)

    res_gammas: list[float] = []
    ridgeless_mse: list[float] = []
    ridgeless_r2: list[float] = []
    regularized_mse: list[float] = []
    regularized_r2: list[float] = []

    for g in gammas:
        gamma_val = float(g)
        d_feats = max(2, int(gamma_val * m_samples))

        # Random feature projection matrix
        w_proj = rng.normal(0.0, 1.0 / math.sqrt(n_f), size=(n_f, d_feats))
        z_tr = np.maximum(0.0, x_tr @ w_proj)  # ReLU non-linearity
        z_te = np.maximum(0.0, x_te @ w_proj)

        # 1. Ridgeless minimum-norm interpolator
        if d_feats <= m_samples:
            # Underparameterized: (Z^T Z + eps I)^-1 Z^T y
            gram = z_tr.T @ z_tr + 1e-5 * np.eye(d_feats)
            beta_rl = np.linalg.solve(gram, z_tr.T @ y_tr)
        else:
            # Overparameterized: Z^T (Z Z^T + eps I)^-1 y (minimum L2-norm solution)
            dual_gram = z_tr @ z_tr.T + 1e-5 * np.eye(m_samples)
            alpha_dual = np.linalg.solve(dual_gram, y_tr)
            beta_rl = z_tr.T @ alpha_dual

        pred_rl = z_te @ beta_rl
        mse_rl = float(np.mean((y_te - pred_rl) ** 2))
        r2_rl = compute_oos_r2(y_te, pred_rl)

        # 2. Properly regularized ridge estimator (optimal / calibrated shrinkage)
        reg_penalty = 0.05 * m_samples
        gram_reg = z_tr.T @ z_tr + reg_penalty * np.eye(d_feats)
        beta_reg = np.linalg.solve(gram_reg, z_tr.T @ y_tr)
        pred_reg = z_te @ beta_reg
        mse_reg = float(np.mean((y_te - pred_reg) ** 2))
        r2_reg = compute_oos_r2(y_te, pred_reg)

        res_gammas.append(gamma_val)
        ridgeless_mse.append(mse_rl)
        ridgeless_r2.append(r2_rl)
        regularized_mse.append(mse_reg)
        regularized_r2.append(r2_reg)

    return {
        "gammas": res_gammas,
        "ridgeless_mse": ridgeless_mse,
        "ridgeless_r2": ridgeless_r2,
        "regularized_mse": regularized_mse,
        "regularized_r2": regularized_r2,
    }


def run_ml_study(instance: dict[str, Any]) -> dict[str, Any]:
    """Execute complete cross-sectional ML asset pricing study.

    Trains OLS, regularized Ridge, Random Forest, and Neural Network predictors
    using purged cross-validation, reports out-of-sample R2, long-short portfolio
    Sharpe ratios net of transaction costs, and tests the complexity curve.

    Parameters
    ----------
    instance : dict[str, Any]
        Panel instance dictionary from make_instance.

    Returns
    -------
    dict[str, Any]
        Complete results dictionary.
    """
    x_train_3d = np.asarray(instance["X_train"], dtype=np.float64)
    y_train_2d = np.asarray(instance["y_train"], dtype=np.float64)
    x_test_3d = np.asarray(instance["X_test"], dtype=np.float64)
    y_test_2d = np.asarray(instance["y_test"], dtype=np.float64)
    cost_bps = float(instance.get("cost_bps", 15.0))
    gammas = list(instance.get("gammas", [0.25, 0.5, 0.9, 1.0, 1.5, 2.5, 4.0]))

    n_assets, t_train, n_feats = x_train_3d.shape
    _, t_test, _ = x_test_3d.shape

    # Reshape time-first for panel modeling
    x_tr = x_train_3d.transpose(1, 0, 2).reshape(t_train * n_assets, n_feats)
    y_tr = y_train_2d.T.reshape(t_train * n_assets)
    x_te = x_test_3d.transpose(1, 0, 2).reshape(t_test * n_assets, n_feats)

    # 1. Linear OLS (unregularized)
    ols = RidgeRegressor(alpha=0.0, fit_intercept=True)
    ols.fit(x_tr, y_tr)
    pred_ols_flat = ols.predict(x_te)
    pred_ols_2d = pred_ols_flat.reshape(t_test, n_assets).T

    # 2. Ridge with Purged Cross-Validation
    pkf = PurgedKFold(n_splits=3, label_lookahead=1, embargo_pct=0.02)
    candidate_alphas = [0.01, 0.1, 1.0, 10.0]
    best_alpha = 1.0
    best_cv_loss = float("inf")

    for alpha in candidate_alphas:
        fold_losses = []
        for tr_t, val_t in pkf.split(t_train):
            tr_idx = np.concatenate([np.arange(t * n_assets, (t + 1) * n_assets) for t in tr_t])
            val_idx = np.concatenate([np.arange(t * n_assets, (t + 1) * n_assets) for t in val_t])

            m = RidgeRegressor(alpha=alpha, fit_intercept=True)
            m.fit(x_tr[tr_idx], y_tr[tr_idx])
            pred_val = m.predict(x_tr[val_idx])
            fold_losses.append(float(np.mean((y_tr[val_idx] - pred_val) ** 2)))
        mean_loss = float(np.mean(fold_losses))
        if mean_loss < best_cv_loss:
            best_cv_loss = mean_loss
            best_alpha = alpha

    ridge = RidgeRegressor(alpha=best_alpha, fit_intercept=True)
    ridge.fit(x_tr, y_tr)
    pred_ridge_flat = ridge.predict(x_te)
    pred_ridge_2d = pred_ridge_flat.reshape(t_test, n_assets).T

    # 3. Random Forest Regressor
    rf = RandomForestRegressor(n_estimators=10, max_depth=3, min_samples_leaf=10, seed=42)
    rf.fit(x_tr, y_tr)
    pred_rf_flat = rf.predict(x_te)
    pred_rf_2d = pred_rf_flat.reshape(t_test, n_assets).T

    # 4. Neural Network Regressor
    nn = NeuralNetworkRegressor(
        hidden_layers=[16, 8],
        learning_rate=0.01,
        l2_reg=1e-3,
        epochs=30,
        batch_size=32,
        seed=42,
    )
    nn.fit(x_tr, y_tr)
    pred_nn_flat = nn.predict(x_te)
    pred_nn_2d = pred_nn_flat.reshape(t_test, n_assets).T

    # Compute OOS R2
    r2_ols = compute_oos_r2(y_test_2d, pred_ols_2d)
    r2_ridge = compute_oos_r2(y_test_2d, pred_ridge_2d)
    r2_rf = compute_oos_r2(y_test_2d, pred_rf_2d)
    r2_nn = compute_oos_r2(y_test_2d, pred_nn_2d)

    # Compute portfolio performance
    perf_ols = construct_spread_portfolio(pred_ols_2d, y_test_2d, cost_bps)
    perf_ridge = construct_spread_portfolio(pred_ridge_2d, y_test_2d, cost_bps)
    perf_rf = construct_spread_portfolio(pred_rf_2d, y_test_2d, cost_bps)
    perf_nn = construct_spread_portfolio(pred_nn_2d, y_test_2d, cost_bps)

    # Evaluate complexity curve
    complexity_res = evaluate_complexity_curve(x_train_3d, y_train_2d, x_test_3d, y_test_2d, gammas, seed=42)

    return {
        "best_alpha": best_alpha,
        "oos_r2": {
            "ols": r2_ols,
            "ridge": r2_ridge,
            "rf": r2_rf,
            "nn": r2_nn,
        },
        "portfolio_performance": {
            "ols": perf_ols,
            "ridge": perf_ridge,
            "rf": perf_rf,
            "nn": perf_nn,
        },
        "complexity_results": complexity_res,
    }
