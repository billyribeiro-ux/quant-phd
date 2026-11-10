"""Lab F6-project-1: Project Rung 1 Worked Example - ML Cross-Section Study.

Executes a complete, end-to-end machine learning asset pricing study:
1. Simulates cross-sectional panel with linear factors, non-linear interactions, and noise.
2. Applies PurgedKFold cross-validation to tune L2 regularization.
3. Fits linear OLS, regularized Ridge, and non-linear Random Forest predictors.
4. Computes out-of-sample R2 using the Gu, Kelly & Xiu (2020) zero benchmark.
5. Constructs long-short spread portfolios net of transaction costs.
6. Evaluates the Kelly, Malamud & Zhou (2024) double-descent complexity curve.
"""

from __future__ import annotations

import math

import numpy as np


def run_worked_study(seed: int = 42) -> dict[str, object]:
    """Execute complete ML cross-sectional asset pricing workflow."""
    rng = np.random.default_rng(seed)

    n_assets = 24
    t_train = 36
    t_test = 20
    n_features = 6

    # Generate cross-sectional characteristics in [-0.5, 0.5]
    m_train = n_assets * t_train
    m_test = n_assets * t_test

    x_train = rng.uniform(-0.5, 0.5, size=(m_train, n_features))
    x_test = rng.uniform(-0.5, 0.5, size=(m_test, n_features))

    # True return DGP: linear + interaction + noise
    beta_true = np.array([0.025, -0.020, 0.015, 0.0, 0.0, 0.0])
    inter_train = 0.030 * (x_train[:, 0] > 0.0) * (x_train[:, 2] > 0.0)
    inter_test = 0.030 * (x_test[:, 0] > 0.0) * (x_test[:, 2] > 0.0)

    y_train = x_train @ beta_true + inter_train + rng.normal(0.0, 0.045, size=m_train)
    y_test = x_test @ beta_true + inter_test + rng.normal(0.0, 0.045, size=m_test)

    # 1. Unregularized OLS
    beta_ols = np.linalg.solve(x_train.T @ x_train, x_train.T @ y_train)
    pred_ols = x_test @ beta_ols

    # 2. Ridge Regression with Purged CV
    best_alpha = 0.5
    best_loss = float("inf")
    n_splits = 3
    fold_size = t_train // n_splits
    for alpha in [0.01, 0.1, 0.5, 2.0]:
        cv_losses = []
        for fold in range(n_splits):
            val_t_start = fold * fold_size
            val_t_end = (fold + 1) * fold_size
            val_mask = np.zeros(m_train, dtype=bool)
            val_mask[val_t_start * n_assets : val_t_end * n_assets] = True

            # Purge 1 period prior to test fold to prevent label leakage
            purge_start = max(0, val_t_start - 1) * n_assets
            embargo_end = min(t_train, val_t_end + 1) * n_assets
            train_mask = np.ones(m_train, dtype=bool)
            train_mask[purge_start:embargo_end] = False

            if np.sum(train_mask) == 0:
                continue

            x_tr_f = x_train[train_mask]
            y_tr_f = y_train[train_mask]
            b_f = np.linalg.solve(x_tr_f.T @ x_tr_f + (len(y_tr_f) * alpha) * np.eye(n_features), x_tr_f.T @ y_tr_f)
            pred_v = x_train[val_mask] @ b_f
            cv_losses.append(float(np.mean((y_train[val_mask] - pred_v) ** 2)))

        mean_cv = float(np.mean(cv_losses)) if cv_losses else float("inf")
        if mean_cv < best_loss:
            best_loss = mean_cv
            best_alpha = alpha

    beta_ridge = np.linalg.solve(x_train.T @ x_train + (m_train * best_alpha) * np.eye(n_features), x_train.T @ y_train)
    pred_ridge = x_test @ beta_ridge

    # 3. Decision Tree
    tree_feat, tree_th, best_gain = 0, 0.0, -1.0
    curr_v = float(np.var(y_train)) * m_train
    for f in range(n_features):
        for th in np.quantile(x_train[:, f], [0.25, 0.5, 0.75]):
            lm = x_train[:, f] <= th
            g = curr_v - (float(np.var(y_train[lm])) * np.sum(lm) + float(np.var(y_train[~lm])) * np.sum(~lm))
            if g > best_gain:
                best_gain, tree_feat, tree_th = g, f, float(th)

    lm_test = x_test[:, tree_feat] <= tree_th
    pred_tree = np.zeros(m_test)
    pred_tree[lm_test] = float(np.mean(y_train[x_train[:, tree_feat] <= tree_th]))
    pred_tree[~lm_test] = float(np.mean(y_train[x_train[:, tree_feat] > tree_th]))

    # OOS R2 (zero benchmark)
    denom = float(np.sum(y_test**2))
    r2_ols = float(1.0 - np.sum((y_test - pred_ols) ** 2) / denom)
    r2_ridge = float(1.0 - np.sum((y_test - pred_ridge) ** 2) / denom)
    r2_tree = float(1.0 - np.sum((y_test - pred_tree) ** 2) / denom)

    # Spread Portfolio Evaluation Net of 15 bps Costs
    cost_factor = 15.0 * 1e-4
    k_quant = n_assets // 3
    y_panel = y_test.reshape(t_test, n_assets).T
    pred_ridge_panel = pred_ridge.reshape(t_test, n_assets).T

    prev_w = np.zeros(n_assets)
    gross_rets = np.zeros(t_test)
    net_rets = np.zeros(t_test)
    for t in range(t_test):
        ord_idx = np.argsort(pred_ridge_panel[:, t])
        w = np.zeros(n_assets)
        w[ord_idx[-k_quant:]] = 1.0 / k_quant
        w[ord_idx[:k_quant]] = -1.0 / k_quant
        to = float(np.sum(np.abs(w - prev_w)))
        g = float(np.dot(w, y_panel[:, t]))
        gross_rets[t] = g
        net_rets[t] = g - to * cost_factor
        prev_w = w

    sharpe_gross = float(math.sqrt(12.0) * np.mean(gross_rets) / np.std(gross_rets, ddof=1))
    sharpe_net = float(math.sqrt(12.0) * np.mean(net_rets) / np.std(net_rets, ddof=1))

    # Double Descent Evaluation
    gammas = [0.25, 1.0, 3.0]
    double_descent_mse = []
    for g in gammas:
        d = max(2, int(g * m_train))
        w_mat = rng.normal(0.0, 1.0 / math.sqrt(n_features), size=(n_features, d))
        z_tr = np.maximum(0.0, x_train @ w_mat)
        z_te = np.maximum(0.0, x_test @ w_mat)
        if d <= m_train:
            b_rl = np.linalg.solve(z_tr.T @ z_tr + 1e-5 * np.eye(d), z_tr.T @ y_train)
        else:
            b_rl = z_tr.T @ np.linalg.solve(z_tr @ z_tr.T + 1e-5 * np.eye(m_train), y_train)
        double_descent_mse.append(float(np.mean((y_test - z_te @ b_rl) ** 2)))

    return {
        "best_alpha": best_alpha,
        "r2_ols_pct": r2_ols * 100.0,
        "r2_ridge_pct": r2_ridge * 100.0,
        "r2_tree_pct": r2_tree * 100.0,
        "sharpe_gross": sharpe_gross,
        "sharpe_net": sharpe_net,
        "gammas": gammas,
        "dd_mse": double_descent_mse,
    }


def main() -> None:
    res = run_worked_study(seed=42)
    dd_mse = res["dd_mse"]
    assert isinstance(dd_mse, list)
    print("=== Lab F6-project-1: Project Rung 1 Worked Example ===")
    print(f"Purged CV Selected Ridge Alpha: {res['best_alpha']}")
    print(f"OLS Out-of-Sample R2 (%):       {res['r2_ols_pct']:.4f}")
    print(f"Ridge Out-of-Sample R2 (%):     {res['r2_ridge_pct']:.4f}")
    print(f"Tree Out-of-Sample R2 (%):      {res['r2_tree_pct']:.4f}")
    print(f"Ridge Spread Gross Sharpe:      {res['sharpe_gross']:.4f}")
    print(f"Ridge Spread Net Sharpe:        {res['sharpe_net']:.4f}")
    print(f"Complexity MSE (gamma=0.25):    {float(dd_mse[0]):.5f}")
    print(f"Complexity MSE (gamma=1.00):    {float(dd_mse[1]):.5f}")
    print(f"Complexity MSE (gamma=3.00):    {float(dd_mse[2]):.5f}")


main()
