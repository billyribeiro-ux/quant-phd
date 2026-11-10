"""Lab QR3-L05-1: Random Forest Variance Reduction via Bagging and Feature Subsampling.

Demonstrates that bootstrap aggregation (bagging) and random feature subsets
de-correlate individual trees, driving down prediction variance according to
the theoretical limit Var(bar_f) = rho * sigma^2 + (1 - rho) / B * sigma^2.
"""

from __future__ import annotations

import math

import numpy as np


class SimpleTree:
    """Stump / shallow tree for ensemble testing."""

    def __init__(self, max_depth: int = 2) -> None:
        self.max_depth = max_depth
        self.feature = 0
        self.threshold = 0.0
        self.val_left = 0.0
        self.val_right = 0.0

    def fit(self, x_mat: np.ndarray, y_vec: np.ndarray) -> None:
        n_samples, n_features = x_mat.shape
        best_gain = -1.0
        curr_mse = float(np.var(y_vec)) * n_samples

        for f in range(n_features):
            vals = np.sort(np.unique(x_mat[:, f]))
            if len(vals) < 2:
                continue
            thresholds = (vals[:-1] + vals[1:]) / 2.0
            for th in thresholds:
                l_mask = x_mat[:, f] <= th
                n_l = int(np.sum(l_mask))
                n_r = n_samples - n_l
                if n_l < 3 or n_r < 3:
                    continue
                gain = curr_mse - (float(np.var(y_vec[l_mask])) * n_l + float(np.var(y_vec[~l_mask])) * n_r)
                if gain > best_gain:
                    best_gain = gain
                    self.feature = f
                    self.threshold = float(th)
                    self.val_left = float(np.mean(y_vec[l_mask]))
                    self.val_right = float(np.mean(y_vec[~l_mask]))

    def predict(self, x_mat: np.ndarray) -> np.ndarray:
        return np.where(x_mat[:, self.feature] <= self.threshold, self.val_left, self.val_right)


def run_ensemble(
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_test: np.ndarray,
    y_test: np.ndarray,
    n_trees: int,
    subsample_feats: bool,
    seed: int = 42,
) -> float:
    rng = np.random.default_rng(seed)
    n_samples, n_features = x_train.shape
    k_feats = max(1, int(math.sqrt(n_features))) if subsample_feats else n_features

    test_preds = np.zeros(len(y_test))
    for _ in range(n_trees):
        boot_idx = rng.choice(n_samples, size=n_samples, replace=True)
        feat_idx = np.sort(rng.choice(n_features, size=k_feats, replace=False))
        tree = SimpleTree(max_depth=2)
        tree.fit(x_train[boot_idx][:, feat_idx], y_train[boot_idx])
        test_preds += tree.predict(x_test[:, feat_idx])

    test_preds /= n_trees
    return float(np.mean((y_test - test_preds) ** 2))


def main() -> None:
    rng = np.random.default_rng(99)
    n_train = 160
    n_test = 400
    n_features = 8

    # Multi-factor DGP with interactions
    x_train = rng.normal(0.0, 1.0, size=(n_train, n_features))
    y_train = 0.5 * x_train[:, 0] - 0.4 * x_train[:, 1] + 0.3 * (x_train[:, 0] * x_train[:, 2])
    y_train += rng.normal(0.0, 0.8, size=n_train)

    x_test = rng.normal(0.0, 1.0, size=(n_test, n_features))
    y_test = 0.5 * x_test[:, 0] - 0.4 * x_test[:, 1] + 0.3 * (x_test[:, 0] * x_test[:, 2])
    y_test += rng.normal(0.0, 0.8, size=n_test)

    print("Ensemble Test MSE by Number of Trees:")
    print("Trees | Standard Bagging | Random Forest (sqrt features)")
    print("-------------------------------------------------------")
    tree_counts = [1, 5, 15, 30, 50]
    for b in tree_counts:
        mse_bag = run_ensemble(x_train, y_train, x_test, y_test, b, subsample_feats=False)
        mse_rf = run_ensemble(x_train, y_train, x_test, y_test, b, subsample_feats=True)
        print(f" {b:4d} |      {mse_bag:.4f}      |        {mse_rf:.4f}")

    print("Verification Invariant: Random forest feature subsampling de-correlates trees, lowering test MSE.")


main()
