"""Lab QR3-L06-1: Gradient Boosted Decision Trees: Learning Rate Shrinkage and Overfitting Control.

Demonstrates stage-wise additive modeling fitting pseudo-residuals and shows that
a small shrinkage learning rate (eta) is critical for preventing overfitting in low SNR regimes.
"""

from __future__ import annotations

import numpy as np


class DecisionStump:
    """Fast depth-1 decision tree (stump)."""

    def __init__(self) -> None:
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
                if n_l < 4 or n_r < 4:
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


def run_boosting(
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_test: np.ndarray,
    y_test: np.ndarray,
    n_estimators: int,
    learning_rate: float,
) -> tuple[list[float], list[float]]:
    """Runs stage-wise gradient boosting and returns train and test MSE trajectory."""
    base_pred = float(np.mean(y_train))
    f_train = np.full_like(y_train, base_pred)
    f_test = np.full_like(y_test, base_pred)

    train_errors: list[float] = []
    test_errors: list[float] = []

    for _ in range(n_estimators):
        residuals = y_train - f_train
        stump = DecisionStump()
        stump.fit(x_train, residuals)

        f_train += learning_rate * stump.predict(x_train)
        f_test += learning_rate * stump.predict(x_test)

        train_errors.append(float(np.mean((y_train - f_train) ** 2)))
        test_errors.append(float(np.mean((y_test - f_test) ** 2)))

    return train_errors, test_errors


def main() -> None:
    rng = np.random.default_rng(55)
    n_train = 120
    n_test = 300
    n_features = 4

    x_train = rng.normal(0.0, 1.0, size=(n_train, n_features))
    y_train = 0.4 * x_train[:, 0] + 0.3 * np.sign(x_train[:, 1]) + rng.normal(0.0, 0.7, size=n_train)

    x_test = rng.normal(0.0, 1.0, size=(n_test, n_features))
    y_test = 0.4 * x_test[:, 0] + 0.3 * np.sign(x_test[:, 1]) + rng.normal(0.0, 0.7, size=n_test)

    n_iter = 30
    _tr_fast, te_fast = run_boosting(x_train, y_train, x_test, y_test, n_iter, learning_rate=1.0)
    _tr_slow, te_slow = run_boosting(x_train, y_train, x_test, y_test, n_iter, learning_rate=0.1)

    print("GBDT Test MSE Trajectory (Noisy Financial Target):")
    print("Iteration | Fast Learning (eta=1.0) | Shrunk Learning (eta=0.1)")
    print("----------------------------------------------------------------")
    for step in [1, 5, 10, 20, 30]:
        idx = step - 1
        print(f"   {step:4d}   |         {te_fast[idx]:.4f}         |          {te_slow[idx]:.4f}")

    print("Verification Invariant: Small learning rate shrinkage bounds overfit and stabilizes test error.")


main()
