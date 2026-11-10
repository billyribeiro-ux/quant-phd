"""Atlas A17: Machine Learning Pipeline (atlas.ml) support module for F6.

Provides point-in-time statistical learning estimators and purged cross-validation
conforming to atlas/A17.contract.md:
- PurgedKFold: temporal cross-validation with label lookahead purging and post-test embargo.
- RidgeRegressor: L2 penalized normal equations.
- LassoRegressor: L1 penalized coordinate descent.
- DecisionTreeRegressor: recursive MSE binary partitioning.
- RandomForestRegressor: bootstrap aggregation with randomized feature subsampling.
- NeuralNetworkRegressor: analytical backpropagation MLP with momentum and weight decay.
"""

from __future__ import annotations

import math
import sys
import types

import numpy as np

__all__ = [
    "DecisionTreeRegressor",
    "LassoRegressor",
    "NeuralNetworkRegressor",
    "PurgedKFold",
    "RandomForestRegressor",
    "RidgeRegressor",
]


class PurgedKFold:
    """K-fold cross-validation with label overlap purging and post-test embargo."""

    def __init__(
        self,
        n_splits: int = 5,
        label_lookahead: int = 1,
        embargo_pct: float = 0.01,
    ) -> None:
        if n_splits < 2:
            raise ValueError(f"n_splits must be at least 2, got {n_splits}")
        if label_lookahead < 1:
            raise ValueError(f"label_lookahead must be >= 1, got {label_lookahead}")
        if not (0.0 <= embargo_pct < 1.0):
            raise ValueError(f"embargo_pct must be in [0.0, 1.0), got {embargo_pct}")

        self.n_splits = n_splits
        self.label_lookahead = label_lookahead
        self.embargo_pct = embargo_pct

    def split(self, n_samples: int) -> list[tuple[np.ndarray, np.ndarray]]:
        """Generate (train_indices, test_indices) splits."""
        if n_samples < self.n_splits:
            raise ValueError(f"n_samples ({n_samples}) must be >= n_splits ({self.n_splits})")

        indices = np.arange(n_samples)
        fold_sizes = np.full(self.n_splits, n_samples // self.n_splits, dtype=int)
        fold_sizes[: n_samples % self.n_splits] += 1
        current = 0
        splits: list[tuple[np.ndarray, np.ndarray]] = []
        h_embargo = math.ceil(self.embargo_pct * n_samples)

        for f_size in fold_sizes:
            test_start = current
            test_end = current + f_size - 1
            current += f_size

            test_idx = indices[test_start : test_end + 1]

            purge_start = max(0, test_start - self.label_lookahead + 1)
            embargo_end = min(n_samples - 1, test_end + h_embargo)

            train_mask = np.ones(n_samples, dtype=bool)
            train_mask[purge_start : embargo_end + 1] = False
            train_idx = indices[train_mask]

            splits.append((train_idx, test_idx))

        return splits


class RidgeRegressor:
    """Ridge regression with L2 shrinkage."""

    def __init__(self, alpha: float = 1.0, fit_intercept: bool = True) -> None:
        if alpha < 0.0:
            raise ValueError(f"alpha must be non-negative, got {alpha}")
        self.alpha = float(alpha)
        self.fit_intercept = fit_intercept
        self.coef_: np.ndarray | None = None
        self.intercept_: float = 0.0

    def fit(self, x_mat: np.ndarray, y_vec: np.ndarray) -> RidgeRegressor:
        """Fit Ridge coefficients via normal equations."""
        x_data = np.asarray(x_mat, dtype=np.float64)
        y_data = np.asarray(y_vec, dtype=np.float64)
        if x_data.ndim != 2:
            raise ValueError("x_mat must be 2-dimensional")
        if y_data.ndim != 1:
            raise ValueError("y_vec must be 1-dimensional")
        if x_data.shape[0] != y_data.shape[0]:
            raise ValueError("Sample counts of x_mat and y_vec must match")

        n_samples, n_features = x_data.shape
        if self.fit_intercept:
            x_mean = np.mean(x_data, axis=0)
            y_mean = float(np.mean(y_data))
            x_c = x_data - x_mean
            y_c = y_data - y_mean
        else:
            x_mean = np.zeros(n_features)
            y_mean = 0.0
            x_c = x_data
            y_c = y_data

        a_mat = x_c.T @ x_c + (n_samples * self.alpha) * np.eye(n_features)
        b_vec = x_c.T @ y_c
        self.coef_ = np.linalg.solve(a_mat, b_vec)

        if self.fit_intercept:
            self.intercept_ = y_mean - float(x_mean @ self.coef_)
        else:
            self.intercept_ = 0.0
        return self

    def predict(self, x_mat: np.ndarray) -> np.ndarray:
        """Predict target values."""
        if self.coef_ is None:
            raise ValueError("Model is not fitted")
        x_data = np.asarray(x_mat, dtype=np.float64)
        return np.asarray(x_data @ self.coef_ + self.intercept_, dtype=np.float64)


class LassoRegressor:
    """Lasso regression with L1 regularization via cyclical coordinate descent."""

    def __init__(
        self,
        alpha: float = 0.1,
        fit_intercept: bool = True,
        max_iter: int = 1000,
        tol: float = 1e-4,
    ) -> None:
        if alpha < 0.0:
            raise ValueError(f"alpha must be non-negative, got {alpha}")
        self.alpha = float(alpha)
        self.fit_intercept = fit_intercept
        self.max_iter = max_iter
        self.tol = tol
        self.coef_: np.ndarray | None = None
        self.intercept_: float = 0.0

    def fit(self, x_mat: np.ndarray, y_vec: np.ndarray) -> LassoRegressor:
        """Fit Lasso coefficients via coordinate descent."""
        x_data = np.asarray(x_mat, dtype=np.float64)
        y_data = np.asarray(y_vec, dtype=np.float64)
        if x_data.ndim != 2 or y_data.ndim != 1 or x_data.shape[0] != y_data.shape[0]:
            raise ValueError("Invalid shapes for x_mat and y_vec")

        n_samples, n_features = x_data.shape
        if self.fit_intercept:
            x_mean = np.mean(x_data, axis=0)
            y_mean = float(np.mean(y_data))
            x_c = x_data - x_mean
            y_c = y_data - y_mean
        else:
            x_mean = np.zeros(n_features)
            y_mean = 0.0
            x_c = x_data
            y_c = y_data

        norm_sq = np.sum(x_c**2, axis=0) / n_samples
        norm_sq = np.where(norm_sq == 0, 1.0, norm_sq)

        beta = np.zeros(n_features, dtype=np.float64)
        residuals = y_c.copy()

        for _ in range(self.max_iter):
            max_change = 0.0
            for j in range(n_features):
                old_val = beta[j]
                residuals += x_c[:, j] * old_val
                rho = float(np.dot(x_c[:, j], residuals)) / n_samples

                if rho > self.alpha:
                    new_val = (rho - self.alpha) / norm_sq[j]
                elif rho < -self.alpha:
                    new_val = (rho + self.alpha) / norm_sq[j]
                else:
                    new_val = 0.0

                beta[j] = new_val
                residuals -= x_c[:, j] * new_val
                max_change = max(max_change, abs(new_val - old_val))

            if max_change < self.tol:
                break

        self.coef_ = beta
        if self.fit_intercept:
            self.intercept_ = y_mean - float(x_mean @ self.coef_)
        else:
            self.intercept_ = 0.0
        return self

    def predict(self, x_mat: np.ndarray) -> np.ndarray:
        """Predict target values."""
        if self.coef_ is None:
            raise ValueError("Model is not fitted")
        x_data = np.asarray(x_mat, dtype=np.float64)
        return np.asarray(x_data @ self.coef_ + self.intercept_, dtype=np.float64)


class _TreeNode:
    def __init__(
        self,
        value: float = 0.0,
        feature: int = -1,
        threshold: float = 0.0,
        left: _TreeNode | None = None,
        right: _TreeNode | None = None,
        n_samples: int = 0,
        is_leaf: bool = True,
    ) -> None:
        self.value = value
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.n_samples = n_samples
        self.is_leaf = is_leaf


class DecisionTreeRegressor:
    """Decision tree regressor using recursive binary partitioning on MSE."""

    def __init__(self, max_depth: int = 3, min_samples_leaf: int = 5) -> None:
        if max_depth < 1:
            raise ValueError("max_depth must be >= 1")
        if min_samples_leaf < 1:
            raise ValueError("min_samples_leaf must be >= 1")

        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.root: _TreeNode | None = None
        self.n_features_: int = 0

    def fit(self, x_mat: np.ndarray, y_vec: np.ndarray) -> DecisionTreeRegressor:
        """Grow decision tree recursively."""
        x_data = np.asarray(x_mat, dtype=np.float64)
        y_data = np.asarray(y_vec, dtype=np.float64)
        if x_data.ndim != 2 or y_data.ndim != 1 or x_data.shape[0] != y_data.shape[0]:
            raise ValueError("Invalid shapes for x_mat and y_vec")

        self.n_features_ = x_data.shape[1]
        self.root = self._build_tree(x_data, y_data, depth=0)
        return self

    def _build_tree(self, x_subset: np.ndarray, y_subset: np.ndarray, depth: int) -> _TreeNode:
        n_samples = len(y_subset)
        node_value = float(np.mean(y_subset)) if n_samples > 0 else 0.0
        node = _TreeNode(value=node_value, n_samples=n_samples, is_leaf=True)

        if depth >= self.max_depth or n_samples < 2 * self.min_samples_leaf:
            return node

        best_feat = -1
        best_thresh = 0.0
        best_mse_gain = -1.0
        curr_mse = float(np.var(y_subset)) * n_samples

        for f in range(self.n_features_):
            vals = np.sort(np.unique(x_subset[:, f]))
            if len(vals) < 2:
                continue
            thresholds = (vals[:-1] + vals[1:]) / 2.0
            if len(thresholds) > 20:
                thresholds = np.quantile(thresholds, np.linspace(0.05, 0.95, 20))

            for th in thresholds:
                left_mask = x_subset[:, f] <= th
                n_l = int(np.sum(left_mask))
                n_r = n_samples - n_l
                if n_l < self.min_samples_leaf or n_r < self.min_samples_leaf:
                    continue

                mse_l = float(np.var(y_subset[left_mask])) * n_l
                mse_r = float(np.var(y_subset[~left_mask])) * n_r
                gain = curr_mse - (mse_l + mse_r)
                if gain > best_mse_gain:
                    best_mse_gain = gain
                    best_feat = f
                    best_thresh = float(th)

        if best_mse_gain > 1e-12:
            left_mask = x_subset[:, best_feat] <= best_thresh
            node.is_leaf = False
            node.feature = best_feat
            node.threshold = best_thresh
            node.left = self._build_tree(x_subset[left_mask], y_subset[left_mask], depth + 1)
            node.right = self._build_tree(x_subset[~left_mask], y_subset[~left_mask], depth + 1)

        return node

    def predict(self, x_mat: np.ndarray) -> np.ndarray:
        """Predict target values."""
        if self.root is None:
            raise ValueError("Model is not fitted")
        x_data = np.asarray(x_mat, dtype=np.float64)
        return np.array([self._predict_single(self.root, row) for row in x_data], dtype=np.float64)

    def _predict_single(self, node: _TreeNode, x_row: np.ndarray) -> float:
        if node.is_leaf or node.left is None or node.right is None:
            return node.value
        if x_row[node.feature] <= node.threshold:
            return self._predict_single(node.left, x_row)
        return self._predict_single(node.right, x_row)


class RandomForestRegressor:
    """Random forest ensemble with bootstrap aggregation and feature subsampling."""

    def __init__(
        self,
        n_estimators: int = 10,
        max_depth: int = 3,
        min_samples_leaf: int = 5,
        max_features: str | float = "sqrt",
        seed: int = 42,
    ) -> None:
        if n_estimators < 1:
            raise ValueError("n_estimators must be >= 1")
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.seed = seed
        self.trees: list[tuple[DecisionTreeRegressor, np.ndarray]] = []

    def fit(self, x_mat: np.ndarray, y_vec: np.ndarray) -> RandomForestRegressor:
        """Fit ensemble of bagged trees."""
        x_data = np.asarray(x_mat, dtype=np.float64)
        y_data = np.asarray(y_vec, dtype=np.float64)
        n_samples, n_features = x_data.shape
        rng = np.random.default_rng(self.seed)

        if isinstance(self.max_features, str) and self.max_features == "sqrt":
            k_feats = max(1, int(math.sqrt(n_features)))
        elif isinstance(self.max_features, float):
            k_feats = max(1, int(self.max_features * n_features))
        else:
            k_feats = n_features

        self.trees = []
        for _ in range(self.n_estimators):
            boot_idx = rng.choice(n_samples, size=n_samples, replace=True)
            feat_idx = np.sort(rng.choice(n_features, size=k_feats, replace=False))
            tree = DecisionTreeRegressor(
                max_depth=self.max_depth,
                min_samples_leaf=self.min_samples_leaf,
            )
            tree.fit(x_data[boot_idx][:, feat_idx], y_data[boot_idx])
            self.trees.append((tree, feat_idx))
        return self

    def predict(self, x_mat: np.ndarray) -> np.ndarray:
        """Predict target values averaging across trees."""
        if not self.trees:
            raise ValueError("Model is not fitted")
        x_data = np.asarray(x_mat, dtype=np.float64)
        preds = np.zeros(len(x_data), dtype=np.float64)
        for tree, feat_idx in self.trees:
            preds += tree.predict(x_data[:, feat_idx])
        return preds / len(self.trees)


class NeuralNetworkRegressor:
    """Multi-layer feedforward neural network with analytical backpropagation and L2 regularization."""

    def __init__(
        self,
        hidden_layers: list[int] | None = None,
        learning_rate: float = 0.01,
        l2_reg: float = 1e-3,
        epochs: int = 50,
        batch_size: int = 32,
        seed: int = 42,
    ) -> None:
        self.hidden_layers = hidden_layers if hidden_layers is not None else [16, 8]
        self.learning_rate = learning_rate
        self.l2_reg = l2_reg
        self.epochs = epochs
        self.batch_size = batch_size
        self.seed = seed
        self.weights: list[np.ndarray] = []
        self.biases: list[np.ndarray] = []

    def fit(self, x_mat: np.ndarray, y_vec: np.ndarray) -> NeuralNetworkRegressor:
        """Fit neural network weights via mini-batch SGD with momentum."""
        x_data = np.asarray(x_mat, dtype=np.float64)
        y_data = np.asarray(y_vec, dtype=np.float64).reshape(-1, 1)
        n_samples, n_in = x_data.shape

        rng = np.random.default_rng(self.seed)
        layer_sizes = [n_in, *self.hidden_layers, 1]

        self.weights = []
        self.biases = []
        v_w: list[np.ndarray] = []
        v_b: list[np.ndarray] = []
        for i in range(len(layer_sizes) - 1):
            w = rng.normal(0.0, math.sqrt(2.0 / layer_sizes[i]), size=(layer_sizes[i], layer_sizes[i + 1]))
            b = np.zeros((1, layer_sizes[i + 1]), dtype=np.float64)
            self.weights.append(w)
            self.biases.append(b)
            v_w.append(np.zeros_like(w))
            v_b.append(np.zeros_like(b))

        momentum = 0.9
        for _ in range(self.epochs):
            perm = rng.permutation(n_samples)
            for s in range(0, n_samples, self.batch_size):
                b_idx = perm[s : s + self.batch_size]
                x_b = x_data[b_idx]
                y_b = y_data[b_idx]
                m_b = len(b_idx)

                activations = [x_b]
                zs = []
                for i in range(len(self.weights)):
                    z = activations[-1] @ self.weights[i] + self.biases[i]
                    zs.append(z)
                    a = np.maximum(0.0, z) if i < len(self.weights) - 1 else z
                    activations.append(a)

                delta = (activations[-1] - y_b) / m_b
                for i in reversed(range(len(self.weights))):
                    d_w = activations[i].T @ delta + self.l2_reg * self.weights[i]
                    d_b = np.sum(delta, axis=0, keepdims=True)

                    v_w[i] = momentum * v_w[i] - self.learning_rate * d_w
                    v_b[i] = momentum * v_b[i] - self.learning_rate * d_b
                    self.weights[i] += v_w[i]
                    self.biases[i] += v_b[i]

                    if i > 0:
                        delta = (delta @ self.weights[i].T) * (zs[i - 1] > 0.0)

        return self

    def predict(self, x_mat: np.ndarray) -> np.ndarray:
        """Predict target values via forward propagation."""
        if not self.weights:
            raise ValueError("Model is not fitted")
        x_data = np.asarray(x_mat, dtype=np.float64)
        a = x_data
        for i in range(len(self.weights)):
            z = a @ self.weights[i] + self.biases[i]
            a = np.maximum(0.0, z) if i < len(self.weights) - 1 else z
        return np.asarray(a.flatten(), dtype=np.float64)


# Ensure atlas.ml alias is registered in sys.modules
if "atlas" not in sys.modules:
    atlas_pkg = types.ModuleType("atlas")
    sys.modules["atlas"] = atlas_pkg
sys.modules["atlas.ml"] = sys.modules[__name__]
setattr(sys.modules["atlas"], "ml", sys.modules[__name__])  # noqa: B010
