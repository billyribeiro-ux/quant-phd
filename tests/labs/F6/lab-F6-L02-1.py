"""Lab F6-L02-1: Non-Linear Interaction Harvesting via Tree Ensembles.

Demonstrates that tree-based architectures capture non-linear characteristic interactions
(e.g., momentum conditional on size or volatility) that linear models miss.
Evaluates out-of-sample R2 and calculates feature attribution.
"""

from __future__ import annotations

import numpy as np


class RegressionTreeNode:
    """Node in a greedy binary regression tree."""

    def __init__(
        self,
        value: float = 0.0,
        feature: int = -1,
        threshold: float = 0.0,
        left: RegressionTreeNode | None = None,
        right: RegressionTreeNode | None = None,
        is_leaf: bool = True,
    ) -> None:
        self.value = value
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.is_leaf = is_leaf


class ShallowRegressionTree:
    """Shallow regression tree for low S/N financial panels."""

    def __init__(self, max_depth: int = 3, min_samples_leaf: int = 10) -> None:
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.root: RegressionTreeNode | None = None

    def fit(self, x_mat: np.ndarray, y_vec: np.ndarray) -> ShallowRegressionTree:
        """Fit decision tree via greedy MSE reduction."""
        self.root = self._build(x_mat, y_vec, depth=0)
        return self

    def _build(self, x_sub: np.ndarray, y_sub: np.ndarray, depth: int) -> RegressionTreeNode:
        n_samples = len(y_sub)
        val = float(np.mean(y_sub)) if n_samples > 0 else 0.0
        if depth >= self.max_depth or n_samples < 2 * self.min_samples_leaf:
            return RegressionTreeNode(value=val, is_leaf=True)

        best_feat = -1
        best_th = 0.0
        best_gain = -1.0
        curr_var = float(np.var(y_sub)) * n_samples

        for f in range(x_sub.shape[1]):
            thresholds = np.quantile(x_sub[:, f], np.linspace(0.1, 0.9, 9))
            for th in thresholds:
                left_mask = x_sub[:, f] <= th
                n_l = int(np.sum(left_mask))
                n_r = n_samples - n_l
                if n_l < self.min_samples_leaf or n_r < self.min_samples_leaf:
                    continue

                gain = curr_var - (float(np.var(y_sub[left_mask])) * n_l + float(np.var(y_sub[~left_mask])) * n_r)
                if gain > best_gain:
                    best_gain = gain
                    best_feat = f
                    best_th = float(th)

        if best_gain <= 1e-8:
            return RegressionTreeNode(value=val, is_leaf=True)

        left_mask = x_sub[:, best_feat] <= best_th
        left_node = self._build(x_sub[left_mask], y_sub[left_mask], depth + 1)
        right_node = self._build(x_sub[~left_mask], y_sub[~left_mask], depth + 1)
        return RegressionTreeNode(
            value=val,
            feature=best_feat,
            threshold=best_th,
            left=left_node,
            right=right_node,
            is_leaf=False,
        )

    def predict(self, x_mat: np.ndarray) -> np.ndarray:
        """Predict returns."""
        if self.root is None:
            raise ValueError("Tree not fitted")
        return np.array([self._predict_row(self.root, row) for row in x_mat], dtype=np.float64)

    def _predict_row(self, node: RegressionTreeNode, row: np.ndarray) -> float:
        if node.is_leaf or node.left is None or node.right is None:
            return node.value
        if row[node.feature] <= node.threshold:
            return self._predict_row(node.left, row)
        return self._predict_row(node.right, row)


def run_lab(seed: int = 42) -> dict[str, float]:
    """Execute non-linear interaction comparison."""
    rng = np.random.default_rng(seed)

    n_samples = 1200
    n_features = 6

    # Normalized characteristic panel in [-0.5, 0.5]
    x_data = rng.uniform(-0.5, 0.5, size=(n_samples, n_features))

    # True return contains a sharp non-linear interaction:
    # Feature 0 (e.g. Momentum) is profitable ONLY when Feature 1 (e.g. Size/Vol) is in the upper regime
    signal_interaction = 0.040 * (x_data[:, 0] > 0.0) * (x_data[:, 1] > 0.0)
    signal_linear = -0.015 * x_data[:, 2]
    noise = rng.normal(0.0, 0.035, size=n_samples)

    y_data = signal_interaction + signal_linear + noise

    n_train = 800
    x_train, y_train = x_data[:n_train], y_data[:n_train]
    x_test, y_test = x_data[n_train:], y_data[n_train:]

    # 1. Linear Model (Ridge)
    ridge_beta = np.linalg.solve(x_train.T @ x_train + 10.0 * np.eye(n_features), x_train.T @ y_train)
    pred_linear = x_test @ ridge_beta

    # 2. Shallow Decision Tree
    tree = ShallowRegressionTree(max_depth=3, min_samples_leaf=15)
    tree.fit(x_train, y_train)
    pred_tree = tree.predict(x_test)

    # Out-of-sample R2 (zero benchmark)
    denom = float(np.sum(y_test**2))
    r2_linear = float(1.0 - np.sum((y_test - pred_linear) ** 2) / denom)
    r2_tree = float(1.0 - np.sum((y_test - pred_tree) ** 2) / denom)

    # Compute root split feature and threshold
    root_feat = tree.root.feature if tree.root else -1
    root_th = tree.root.threshold if tree.root else 0.0

    return {
        "r2_linear_pct": r2_linear * 100.0,
        "r2_tree_pct": r2_tree * 100.0,
        "root_split_feature": float(root_feat),
        "root_split_threshold": float(root_th),
    }


def main() -> None:
    res = run_lab(seed=42)
    print("=== Lab F6-L02-1: Tree Ensembles & Non-Linear Interactions ===")
    print(f"Linear Out-of-Sample R2 (%): {res['r2_linear_pct']:.4f}")
    print(f"Tree Out-of-Sample R2 (%):   {res['r2_tree_pct']:.4f}")
    print(f"Root Split Feature Index:    {int(res['root_split_feature'])}")
    print(f"Root Split Threshold:        {res['root_split_threshold']:.4f}")


main()
