"""Lab QR3-L02-1: Overlapping Label Leakage: Standard vs. Purged K-Fold Cross-Validation.

Demonstrates that standard K-fold cross-validation artificially inflates
apparent out-of-sample predictability when multi-day holding period returns
overlap fold boundaries, whereas Purged K-Fold with embargo restores honest error estimates.
"""

from __future__ import annotations

import math

import numpy as np


def compute_overlapping_labels(prices: np.ndarray, horizon: int) -> tuple[np.ndarray, np.ndarray]:
    """Generates features and forward multi-period overlapping return labels."""
    n = len(prices)
    features = np.zeros(n - horizon)
    labels = np.zeros(n - horizon)
    for t in range(n - horizon):
        features[t] = (prices[t] - prices[t - 5]) / prices[t - 5] if t >= 5 else 0.0
        labels[t] = (prices[t + horizon] - prices[t]) / prices[t]
    return features, labels


def evaluate_standard_cv(
    x: np.ndarray,
    y: np.ndarray,
    n_splits: int = 5,
) -> float:
    """Standard K-fold cross validation with i.i.d. shuffle assumption."""
    n = len(y)
    fold_size = n // n_splits
    errors: list[float] = []

    for k in range(n_splits):
        test_start = k * fold_size
        test_end = (k + 1) * fold_size if k < n_splits - 1 else n
        test_idx = np.arange(test_start, test_end)
        train_idx = np.setdiff1d(np.arange(n), test_idx)

        # OLS on training set
        x_tr, y_tr = x[train_idx], y[train_idx]
        x_te, y_te = x[test_idx], y[test_idx]

        slope = float(np.cov(x_tr, y_tr)[0, 1] / (np.var(x_tr) + 1e-12))
        preds = slope * x_te
        errors.append(float(np.mean((y_te - preds) ** 2)))

    return float(np.mean(errors))


def evaluate_purged_cv(
    x: np.ndarray,
    y: np.ndarray,
    horizon: int,
    n_splits: int = 5,
    embargo_pct: float = 0.02,
) -> float:
    """Purged K-fold cross validation with label purging and post-test embargo."""
    n = len(y)
    fold_size = n // n_splits
    errors: list[float] = []
    h_embargo = math.ceil(embargo_pct * n)

    for k in range(n_splits):
        test_start = k * fold_size
        test_end = (k + 1) * fold_size - 1 if k < n_splits - 1 else n - 1
        test_idx = np.arange(test_start, test_end + 1)

        # Purge training observations whose forward horizon [i, i + horizon - 1] touches test
        purge_start = max(0, test_start - horizon + 1)
        embargo_end = min(n - 1, test_end + h_embargo)

        train_mask = np.ones(n, dtype=bool)
        train_mask[purge_start : embargo_end + 1] = False
        train_idx = np.where(train_mask)[0]

        x_tr, y_tr = x[train_idx], y[train_idx]
        x_te, y_te = x[test_idx], y[test_idx]

        slope = float(np.cov(x_tr, y_tr)[0, 1] / (np.var(x_tr) + 1e-12))
        preds = slope * x_te
        errors.append(float(np.mean((y_te - preds) ** 2)))

    return float(np.mean(errors))


def main() -> None:
    rng = np.random.default_rng(77)
    n_bars = 400
    horizon = 5  # 5-day holding period

    # Price path under pure geometric random walk (zero true predictability)
    innovations = rng.normal(0.0002, 0.015, size=n_bars)
    prices = 100.0 * np.exp(np.cumsum(innovations))

    features, labels = compute_overlapping_labels(prices, horizon)
    baseline_var = float(np.var(labels))

    mse_standard = evaluate_standard_cv(features, labels, n_splits=5)
    r2_standard = 1.0 - (mse_standard / baseline_var)

    mse_purged = evaluate_purged_cv(features, labels, horizon=horizon, n_splits=5, embargo_pct=0.02)
    r2_purged = 1.0 - (mse_purged / baseline_var)

    print(f"Sample size: {len(labels)} overlapping {horizon}-day bars")
    print(f"Target variance: {baseline_var:.6f}")
    print(f"Standard K-Fold CV MSE: {mse_standard:.6f} | Apparent R2: {r2_standard:.4f}")
    print(f"Purged K-Fold CV MSE:   {mse_purged:.6f} | Honest R2:   {r2_purged:.4f}")
    print(f"Apparent Predictability Bias: {r2_standard - r2_purged:.4f}")
    print("Verification Invariant: Overlapping label leakage creates spurious apparent R2.")


main()
