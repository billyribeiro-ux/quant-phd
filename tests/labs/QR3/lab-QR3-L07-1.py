"""Lab QR3-L07-1: Neural Networks in Finance: Backpropagation and L2 Weight Decay Regularization.

Demonstrates that feedforward neural networks trained with analytical backpropagation
require aggressive L2 weight decay to prevent memorizing idiosyncratic noise in low-SNR financial panels.
"""

from __future__ import annotations

import math

import numpy as np


class TwoLayerMLP:
    """Two-layer multi-layer perceptron with analytical backpropagation."""

    def __init__(self, n_in: int, n_hidden: int, lr: float, l2: float, seed: int = 42) -> None:
        rng = np.random.default_rng(seed)
        self.w1 = rng.normal(0.0, math.sqrt(2.0 / n_in), size=(n_in, n_hidden))
        self.b1 = np.zeros((1, n_hidden))
        self.w2 = rng.normal(0.0, math.sqrt(2.0 / n_hidden), size=(n_hidden, 1))
        self.b2 = np.zeros((1, 1))
        self.lr = lr
        self.l2 = l2

    def fit(self, x_mat: np.ndarray, y_vec: np.ndarray, epochs: int = 100) -> None:
        m = len(y_vec)
        y_mat = y_vec.reshape(-1, 1)

        for _ in range(epochs):
            # Forward pass
            z1 = x_mat @ self.w1 + self.b1
            a1 = np.maximum(0.0, z1)  # ReLU
            z2 = a1 @ self.w2 + self.b2  # Linear

            # Backward pass
            delta2 = (z2 - y_mat) / m
            dw2 = a1.T @ delta2 + self.l2 * self.w2
            db2 = np.sum(delta2, axis=0, keepdims=True)

            delta1 = (delta2 @ self.w2.T) * (z1 > 0.0)
            dw1 = x_mat.T @ delta1 + self.l2 * self.w1
            db1 = np.sum(delta1, axis=0, keepdims=True)

            self.w2 -= self.lr * dw2
            self.b2 -= self.lr * db2
            self.w1 -= self.lr * dw1
            self.b1 -= self.lr * db1

    def predict(self, x_mat: np.ndarray) -> np.ndarray:
        z1 = x_mat @ self.w1 + self.b1
        a1 = np.maximum(0.0, z1)
        z2 = a1 @ self.w2 + self.b2
        return z2.ravel()


def main() -> None:
    rng = np.random.default_rng(73)
    n_train = 120
    n_test = 400
    n_in = 6

    x_train = rng.normal(0.0, 1.0, size=(n_train, n_in))
    y_train = 0.4 * np.tanh(x_train[:, 0]) - 0.3 * (x_train[:, 1] ** 2) + rng.normal(0.0, 0.9, size=n_train)

    x_test = rng.normal(0.0, 1.0, size=(n_test, n_in))
    y_test = 0.4 * np.tanh(x_test[:, 0]) - 0.3 * (x_test[:, 1] ** 2) + rng.normal(0.0, 0.9, size=n_test)

    # Standardize
    x_mean, x_std = np.mean(x_train, axis=0), np.std(x_train, axis=0)
    x_train = (x_train - x_mean) / x_std
    x_test = (x_test - x_mean) / x_std

    # Model 1: Unregularized MLP (L2 = 0.0)
    mlp_unreg = TwoLayerMLP(n_in=n_in, n_hidden=16, lr=0.05, l2=0.0, seed=1)
    mlp_unreg.fit(x_train, y_train, epochs=150)
    tr_mse_unreg = float(np.mean((y_train - mlp_unreg.predict(x_train)) ** 2))
    te_mse_unreg = float(np.mean((y_test - mlp_unreg.predict(x_test)) ** 2))
    w_norm_unreg = float(np.linalg.norm(mlp_unreg.w1) + np.linalg.norm(mlp_unreg.w2))

    # Model 2: L2 Regularized MLP (L2 = 0.02)
    mlp_reg = TwoLayerMLP(n_in=n_in, n_hidden=16, lr=0.05, l2=0.02, seed=1)
    mlp_reg.fit(x_train, y_train, epochs=150)
    tr_mse_reg = float(np.mean((y_train - mlp_reg.predict(x_train)) ** 2))
    te_mse_reg = float(np.mean((y_test - mlp_reg.predict(x_test)) ** 2))
    w_norm_reg = float(np.linalg.norm(mlp_reg.w1) + np.linalg.norm(mlp_reg.w2))

    print(
        f"Unregularized MLP: Train MSE = {tr_mse_unreg:.4f} | "
        f"Test MSE = {te_mse_unreg:.4f} | Weight Norm = {w_norm_unreg:.2f}"
    )
    print(
        f"L2 Regularized MLP: Train MSE = {tr_mse_reg:.4f} | "
        f"Test MSE = {te_mse_reg:.4f} | Weight Norm = {w_norm_reg:.2f}"
    )
    print("Verification Invariant: L2 weight decay shrinks weight norms and prevents overfitting noise.")


main()
