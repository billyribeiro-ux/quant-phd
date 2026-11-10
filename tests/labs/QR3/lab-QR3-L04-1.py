"""Lab QR3-L04-1: Decision Tree Recursive Partitioning and Depth-Induced Variance.

Demonstrates greedy split criterion optimization and how unconstrained
tree depth leads to severe variance explosion in low SNR return data.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class Node:
    feature: int = -1
    threshold: float = 0.0
    left: Node | None = None
    right: Node | None = None
    value: float = 0.0
    is_leaf: bool = True


def build_tree(x_mat: np.ndarray, y_vec: np.ndarray, max_depth: int, min_leaf: int, depth: int = 0) -> Node:
    """Builds a decision tree recursively via MSE reduction."""
    n_samples, n_features = x_mat.shape
    mean_val = float(np.mean(y_vec)) if n_samples > 0 else 0.0
    node = Node(value=mean_val, is_leaf=True)

    if depth >= max_depth or n_samples < 2 * min_leaf:
        return node

    best_gain = -1.0
    best_feat = -1
    best_thresh = 0.0
    curr_mse = float(np.var(y_vec)) * n_samples

    for f in range(n_features):
        vals = np.sort(np.unique(x_mat[:, f]))
        if len(vals) < 2:
            continue
        thresholds = (vals[:-1] + vals[1:]) / 2.0
        for th in thresholds:
            left_mask = x_mat[:, f] <= th
            n_l = int(np.sum(left_mask))
            n_r = n_samples - n_l
            if n_l < min_leaf or n_r < min_leaf:
                continue

            mse_l = float(np.var(y_vec[left_mask])) * n_l
            mse_r = float(np.var(y_vec[~left_mask])) * n_r
            gain = curr_mse - (mse_l + mse_r)
            if gain > best_gain:
                best_gain = gain
                best_feat = f
                best_thresh = float(th)

    if best_gain > 1e-8:
        left_mask = x_mat[:, best_feat] <= best_thresh
        node.is_leaf = False
        node.feature = best_feat
        node.threshold = best_thresh
        node.left = build_tree(x_mat[left_mask], y_vec[left_mask], max_depth, min_leaf, depth + 1)
        node.right = build_tree(x_mat[~left_mask], y_vec[~left_mask], max_depth, min_leaf, depth + 1)

    return node


def predict_tree(node: Node, x_row: np.ndarray) -> float:
    if node.is_leaf or node.left is None or node.right is None:
        return node.value
    if x_row[node.feature] <= node.threshold:
        return predict_tree(node.left, x_row)
    return predict_tree(node.right, x_row)


def main() -> None:
    rng = np.random.default_rng(42)
    n_train = 150
    n_test = 300
    n_features = 4

    x_train = rng.normal(0.0, 1.0, size=(n_train, n_features))
    # Nonlinear step function
    y_train = np.where((x_train[:, 0] > 0.0) & (x_train[:, 1] > 0.0), 1.0, -1.0).astype(float)
    y_train += rng.normal(0.0, 0.9, size=n_train)  # low SNR noise

    x_test = rng.normal(0.0, 1.0, size=(n_test, n_features))
    y_test = np.where((x_test[:, 0] > 0.0) & (x_test[:, 1] > 0.0), 1.0, -1.0).astype(float)
    y_test += rng.normal(0.0, 0.9, size=n_test)

    print("Evaluating Decision Tree Performance Across Depths:")
    for depth in [1, 2, 3, 5, 8]:
        tree = build_tree(x_train, y_train, max_depth=depth, min_leaf=5)
        tr_preds = np.array([predict_tree(tree, row) for row in x_train])
        te_preds = np.array([predict_tree(tree, row) for row in x_test])

        tr_mse = float(np.mean((y_train - tr_preds) ** 2))
        te_mse = float(np.mean((y_test - te_preds) ** 2))
        print(f"Depth {depth:d}: Train MSE = {tr_mse:.4f} | Test MSE = {te_mse:.4f}")

    print("Verification Invariant: Deep unpruned trees overfit training noise and degrade test MSE.")


main()
