"""Mutant 3: FeatureStore allows future feature observations to be retrieved in as-of queries, introducing lookahead bias."""


from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

import numpy as np

try:
    from atlas.integrity import IntegrityReport, TrialSet, integrity_report
except ImportError:
    from integrity import IntegrityReport, TrialSet, integrity_report

__all__ = [
    "CombinatorialPurgedCV",
    "DecisionTreeRegressor",
    "FeatureStore",
    "GradientBoostingRegressor",
    "IntegrityReport",
    "LassoRegressor",
    "ModelLifecycleState",
    "ModelRegistry",
    "NeuralNetworkRegressor",
    "PurgedKFold",
    "RandomForestRegressor",
    "RidgeRegressor",
    "TreeSHAPExplainer",
    "TrialSet",
    "evaluate_ml_strategy",
    "integrity_report",
]


# ---------------------------------------------------------------------------
# 1. Feature Store & As-Of Point-in-Time Joins
# ---------------------------------------------------------------------------


class FeatureStore:
    """Point-in-time feature store enforcing strict temporal causality."""

    def __init__(self) -> None:
        self._store: dict[str, dict[str, list[tuple[float, float]]]] = {}

    def register_entity(self, entity_id: str) -> None:
        """Register a valid entity identifier."""
        if not entity_id or not isinstance(entity_id, str):
            raise ValueError("Entity ID must be a non-empty string")
        if entity_id not in self._store:
            self._store[entity_id] = {}

    def add_feature_record(
        self,
        entity_id: str,
        timestamp: int | float,
        feature_name: str,
        value: float,
    ) -> None:
        """Store an observed feature value with availability timestamp."""
        if entity_id not in self._store:
            self.register_entity(entity_id)
        if not feature_name or not isinstance(feature_name, str):
            raise ValueError("Feature name must be a non-empty string")
        if not math.isfinite(float(value)):
            raise ValueError(f"Feature value must be finite, got {value}")
        t = float(timestamp)
        if not math.isfinite(t):
            raise ValueError("Timestamp must be finite")

        feat_dict = self._store[entity_id]
        if feature_name not in feat_dict:
            feat_dict[feature_name] = []

        feat_dict[feature_name].append((t, float(value)))
        feat_dict[feature_name].sort(key=lambda x: x[0])

    def get_point_in_time(
        self,
        entity_id: str,
        query_timestamp: int | float,
        feature_names: list[str] | None = None,
    ) -> dict[str, float]:
        """Query feature values known strictly as-of query_timestamp."""
        if entity_id not in self._store:
            raise ValueError(f"Entity '{entity_id}' is not registered in feature store")
        q_t = float(query_timestamp)
        if not math.isfinite(q_t):
            raise ValueError("Query timestamp must be finite")

        entity_data = self._store[entity_id]
        target_features = feature_names if feature_names is not None else list(entity_data.keys())

        result: dict[str, float] = {}
        for feat in target_features:
            records = entity_data.get(feat, [])
            val = np.nan
            if records:
                val = records[-1][1]  # BUG: returns latest record regardless of query timestamp
            result[feat] = val
        return result

    def as_of_join(
        self,
        query_keys: list[tuple[str, int | float]],
        feature_names: list[str],
    ) -> np.ndarray:
        """Construct feature matrix for a sequence of (entity_id, query_timestamp) keys."""
        if not query_keys:
            return np.empty((0, len(feature_names)), dtype=np.float64)
        if not feature_names:
            raise ValueError("feature_names cannot be empty")

        matrix = np.full((len(query_keys), len(feature_names)), np.nan, dtype=np.float64)
        for i, (ent, q_t) in enumerate(query_keys):
            feat_vals = self.get_point_in_time(ent, q_t, feature_names)
            for j, f in enumerate(feature_names):
                matrix[i, j] = feat_vals[f]
        return matrix


# ---------------------------------------------------------------------------
# 2. Purged and Embargoed Cross-Validation
# ---------------------------------------------------------------------------


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

            # Purge any training index i where label [i, i + h - 1] overlaps [test_start, test_end]
            purge_start = max(0, test_start - self.label_lookahead + 1)
            embargo_end = min(n_samples - 1, test_end + h_embargo)

            train_mask = np.ones(n_samples, dtype=bool)
            train_mask[purge_start : embargo_end + 1] = False
            train_idx = indices[train_mask]

            splits.append((train_idx, test_idx))

        return splits


class CombinatorialPurgedCV:
    """Combinatorial Purged Cross-Validation (CPCV)."""

    def __init__(
        self,
        n_groups: int = 6,
        k_test_groups: int = 2,
        label_lookahead: int = 1,
        embargo_pct: float = 0.01,
    ) -> None:
        if n_groups < 2:
            raise ValueError(f"n_groups must be >= 2, got {n_groups}")
        if not (1 <= k_test_groups < n_groups):
            raise ValueError(f"k_test_groups must be in [1, n_groups-1], got {k_test_groups}")
        if label_lookahead < 1:
            raise ValueError(f"label_lookahead must be >= 1, got {label_lookahead}")
        if not (0.0 <= embargo_pct < 1.0):
            raise ValueError(f"embargo_pct must be in [0.0, 1.0), got {embargo_pct}")

        self.n_groups = n_groups
        self.k_test_groups = k_test_groups
        self.label_lookahead = label_lookahead
        self.embargo_pct = embargo_pct

    def split(self, n_samples: int) -> list[tuple[np.ndarray, np.ndarray]]:
        """Generate combinatorial splits."""
        if n_samples < self.n_groups:
            raise ValueError(f"n_samples ({n_samples}) must be >= n_groups ({self.n_groups})")

        indices = np.arange(n_samples)
        group_sizes = np.full(self.n_groups, n_samples // self.n_groups, dtype=int)
        group_sizes[: n_samples % self.n_groups] += 1

        group_bounds: list[tuple[int, int]] = []
        curr = 0
        for g_size in group_sizes:
            group_bounds.append((curr, curr + g_size - 1))
            curr += g_size

        h_embargo = math.ceil(self.embargo_pct * n_samples)
        splits: list[tuple[np.ndarray, np.ndarray]] = []

        for test_comb in itertools.combinations(range(self.n_groups), self.k_test_groups):
            test_mask = np.zeros(n_samples, dtype=bool)
            train_mask = np.ones(n_samples, dtype=bool)

            for g in test_comb:
                g_start, g_end = group_bounds[g]
                test_mask[g_start : g_end + 1] = True

                p_start = max(0, g_start - self.label_lookahead + 1)
                e_end = min(n_samples - 1, g_end + h_embargo)
                train_mask[p_start : e_end + 1] = False

            splits.append((indices[train_mask], indices[test_mask]))

        return splits


# ---------------------------------------------------------------------------
# 3. Statistical Learning Estimators
# ---------------------------------------------------------------------------


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
        if max_iter < 1:
            raise ValueError("max_iter must be >= 1")
        if tol <= 0.0:
            raise ValueError("tol must be positive")

        self.alpha = float(alpha)
        self.fit_intercept = fit_intercept
        self.max_iter = max_iter
        self.tol = tol
        self.coef_: np.ndarray | None = None
        self.intercept_: float = 0.0

    @staticmethod
    def _soft_threshold(z: float, gamma: float) -> float:
        if z > gamma:
            return z - gamma
        elif z < -gamma:
            return z + gamma
        return 0.0

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

        col_norms = np.sum(x_c**2, axis=0)
        col_norms[col_norms < 1e-12] = 1e-12

        beta = np.zeros(n_features, dtype=np.float64)
        residuals = y_c - x_c @ beta

        for _ in range(self.max_iter):
            max_change = 0.0
            for j in range(n_features):
                old_beta_j = beta[j]
                r_j = residuals + x_c[:, j] * old_beta_j
                rho_j = float(x_c[:, j] @ r_j) / n_samples
                new_beta_j = self._soft_threshold(rho_j, self.alpha) / (col_norms[j] / n_samples)

                diff = new_beta_j - old_beta_j
                if diff != 0.0:
                    beta[j] = new_beta_j
                    residuals -= x_c[:, j] * diff
                    max_change = max(max_change, abs(diff))

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


@dataclass
class _TreeNode:
    feature: int = -1
    threshold: float = 0.0
    left: _TreeNode | None = None
    right: _TreeNode | None = None
    value: float = 0.0
    n_samples: int = 0
    is_leaf: bool = True


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
        """Ensemble average predictions."""
        if not self.trees:
            raise ValueError("Model is not fitted")
        x_data = np.asarray(x_mat, dtype=np.float64)
        preds = np.zeros(x_data.shape[0], dtype=np.float64)
        for tree, feat_idx in self.trees:
            preds += tree.predict(x_data[:, feat_idx])
        return preds / len(self.trees)


class GradientBoostingRegressor:
    """Gradient boosted decision trees with shrinkage learning rate."""

    def __init__(
        self,
        n_estimators: int = 20,
        learning_rate: float = 0.1,
        max_depth: int = 2,
        min_samples_leaf: int = 5,
    ) -> None:
        if n_estimators < 1:
            raise ValueError("n_estimators must be >= 1")
        if learning_rate <= 0.0 or learning_rate > 1.0:
            raise ValueError("learning_rate must be in (0, 1]")

        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.trees: list[DecisionTreeRegressor] = []
        self.initial_value_: float = 0.0

    def fit(self, x_mat: np.ndarray, y_vec: np.ndarray) -> GradientBoostingRegressor:
        """Sequential boosting on negative gradients (residuals)."""
        x_data = np.asarray(x_mat, dtype=np.float64)
        y_data = np.asarray(y_vec, dtype=np.float64)

        self.initial_value_ = float(np.mean(y_data))
        f_m = np.full_like(y_data, self.initial_value_)
        self.trees = []

        for _ in range(self.n_estimators):
            residuals = y_data - f_m
            tree = DecisionTreeRegressor(
                max_depth=self.max_depth,
                min_samples_leaf=self.min_samples_leaf,
            )
            tree.fit(x_data, residuals)
            step_pred = tree.predict(x_data)
            f_m += self.learning_rate * step_pred
            self.trees.append(tree)

        return self

    def predict(self, x_mat: np.ndarray) -> np.ndarray:
        """Additive stage predictions."""
        if not self.trees:
            raise ValueError("Model is not fitted")
        x_data = np.asarray(x_mat, dtype=np.float64)
        preds = np.full(x_data.shape[0], self.initial_value_, dtype=np.float64)
        for tree in self.trees:
            preds += self.learning_rate * tree.predict(x_data)
        return preds


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
        v_w = []
        v_b = []
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
        """Predict target values."""
        if not self.weights:
            raise ValueError("Model is not fitted")
        a = np.asarray(x_mat, dtype=np.float64)
        for i in range(len(self.weights)):
            z = a @ self.weights[i] + self.biases[i]
            a = np.maximum(0.0, z) if i < len(self.weights) - 1 else z
        return a.ravel()


# ---------------------------------------------------------------------------
# 4. Interpretability via TreeSHAP
# ---------------------------------------------------------------------------


class TreeSHAPExplainer:
    """Computes exact Shapley values for DecisionTreeRegressor satisfying local additivity."""

    def __init__(self, model: DecisionTreeRegressor) -> None:
        if model.root is None:
            raise ValueError("Model must be fitted before explaining")
        self.model = model
        self.root = model.root
        self._expected_val = self.root.value

    @property
    def expected_value(self) -> float:
        """Return base value E[f(x)]."""
        return self._expected_val

    def explain(self, x_vec: np.ndarray) -> np.ndarray:
        """Compute exact Shapley attribution vector phi such that sum(phi) + E[f(x)] == f(x)."""
        x_data = np.asarray(x_vec, dtype=np.float64)
        if x_data.ndim != 1 or len(x_data) != self.model.n_features_:
            raise ValueError(f"Input x_vec must have shape ({self.model.n_features_},)")

        phi = np.zeros(self.model.n_features_, dtype=np.float64)
        pred = float(self.model.predict(x_data.reshape(1, -1))[0])

        curr = self.root
        while curr is not None and not curr.is_leaf and curr.left is not None and curr.right is not None:
            feat = curr.feature
            next_node = curr.left if x_data[feat] <= curr.threshold else curr.right
            step_delta = next_node.value - curr.value
            phi[feat] += step_delta
            curr = next_node

        total_attributed = float(np.sum(phi))
        residual = (pred - self.expected_value) - total_attributed
        if abs(residual) > 1e-12:
            active_feats = np.where(phi != 0.0)[0]
            if len(active_feats) > 0:
                phi[active_feats[0]] += residual

        return phi


# ---------------------------------------------------------------------------
# 5. Model Registry & Lifecycle Management
# ---------------------------------------------------------------------------


class ModelLifecycleState(StrEnum):
    DRAFT = "DRAFT"
    VALIDATED = "VALIDATED"
    DEPLOYED = "DEPLOYED"
    RETIRED = "RETIRED"


class ModelRegistry:
    """Model governance tracking states, metrics, and deployment lifecycle."""

    def __init__(self) -> None:
        self._registry: dict[str, dict[str, Any]] = {}

    def register_model(self, model_id: str, model: Any, metadata: dict[str, Any]) -> None:
        """Register a new candidate model in DRAFT state."""
        if not model_id or not isinstance(model_id, str):
            raise ValueError("model_id must be a non-empty string")
        if model_id in self._registry:
            raise ValueError(f"Model ID '{model_id}' is already registered")
        self._registry[model_id] = {
            "model": model,
            "metadata": dict(metadata),
            "state": ModelLifecycleState.DRAFT,
        }

    def transition_state(self, model_id: str, new_state: ModelLifecycleState | str) -> None:
        """Enforce valid lifecycle transitions."""
        if model_id not in self._registry:
            raise ValueError(f"Model '{model_id}' not found in registry")
        curr_state = self._registry[model_id]["state"]
        target = ModelLifecycleState(new_state)

        valid_transitions = {
            (ModelLifecycleState.DRAFT, ModelLifecycleState.VALIDATED),
            (ModelLifecycleState.VALIDATED, ModelLifecycleState.DEPLOYED),
            (ModelLifecycleState.VALIDATED, ModelLifecycleState.RETIRED),
            (ModelLifecycleState.DEPLOYED, ModelLifecycleState.RETIRED),
        }
        if (curr_state, target) not in valid_transitions:
            raise ValueError(f"Illegal state transition from {curr_state} to {target}")
        self._registry[model_id]["state"] = target

    def get_model(self, model_id: str) -> tuple[Any, dict[str, Any], ModelLifecycleState]:
        """Retrieve registered model, metadata, and lifecycle status."""
        if model_id not in self._registry:
            raise ValueError(f"Model '{model_id}' not found")
        entry = self._registry[model_id]
        return entry["model"], entry["metadata"], entry["state"]


# ---------------------------------------------------------------------------
# 6. Pipeline Strategy Evaluation with Strictly Positive Lag
# ---------------------------------------------------------------------------


def evaluate_ml_strategy(
    predictions: np.ndarray,
    forward_returns: np.ndarray,
    lag: int = 1,
) -> dict[str, float]:
    """Evaluates an ML predictive signal with strictly positive execution lag."""
    if lag < 1:
        raise ValueError(f"Signal-to-execution lag must be >= 1, got {lag}")

    y_pred = np.asarray(predictions, dtype=np.float64)
    r_fwd = np.asarray(forward_returns, dtype=np.float64)
    if y_pred.ndim != 1 or r_fwd.ndim != 1 or len(y_pred) != len(r_fwd):
        raise ValueError("predictions and forward_returns must be matching 1D arrays")
    if len(y_pred) <= lag:
        raise ValueError("Series length must be greater than execution lag")

    signal = np.sign(y_pred[:-lag])
    strat_returns = signal * r_fwd[lag:]

    mean_ret = float(np.mean(strat_returns))
    std_ret = float(np.std(strat_returns))
    sharpe = (mean_ret / std_ret * math.sqrt(252.0)) if std_ret > 1e-12 else 0.0

    ss_res = float(np.sum((r_fwd - y_pred) ** 2))
    ss_tot = float(np.sum((r_fwd - np.mean(r_fwd)) ** 2))
    oos_r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 1e-12 else 0.0

    equity = np.cumprod(1.0 + strat_returns)
    peak = np.maximum.accumulate(equity)
    drawdown = (equity - peak) / peak
    max_dd = float(np.min(drawdown)) if len(drawdown) > 0 else 0.0

    return {
        "oos_r2": oos_r2,
        "sharpe": sharpe,
        "mean_return": mean_ret,
        "volatility": std_ret * math.sqrt(252.0),
        "max_drawdown": max_dd,
    }
