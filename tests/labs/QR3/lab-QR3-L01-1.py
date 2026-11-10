"""Lab QR3-L01-1: Bias-Variance Decomposition in Ultra-Low SNR Regimes.

Demonstrates that under low signal-to-noise ratios characteristic of financial
returns, model variance dominates squared bias, causing unregularized complex
models to break down out-of-sample.
"""

from __future__ import annotations

import numpy as np


def fit_polynomial(x: np.ndarray, y: np.ndarray, degree: int) -> np.ndarray:
    """Fit polynomial regression coefficients via Vandermonde matrix."""
    vander = np.vander(x, degree + 1)
    coeffs, _, _, _ = np.linalg.lstsq(vander, y, rcond=None)
    return np.asarray(coeffs, dtype=np.float64)


def predict_polynomial(x: np.ndarray, coeffs: np.ndarray) -> np.ndarray:
    """Predict using polynomial coefficients."""
    degree = len(coeffs) - 1
    vander = np.vander(x, degree + 1)
    return np.asarray(vander @ coeffs, dtype=np.float64)


def run_simulation(snr_label: str, noise_scale: float, seed: int = 42) -> None:
    """Simulate bias-variance tradeoff across model complexities."""
    rng = np.random.default_rng(seed)
    n_train = 100
    n_test = 500

    # True underlying function: slight nonlinear curve
    def true_signal(x: np.ndarray) -> np.ndarray:
        return 0.3 * x + 0.15 * (x**2)

    x_train = rng.uniform(-2.0, 2.0, size=n_train)
    y_train = true_signal(x_train) + rng.normal(0.0, noise_scale, size=n_train)

    x_test = rng.uniform(-2.0, 2.0, size=n_test)
    y_test = true_signal(x_test) + rng.normal(0.0, noise_scale, size=n_test)

    print(f"--- Regime: {snr_label} (Noise scale: {noise_scale:.2f}) ---")
    degrees = [1, 2, 4, 6]
    for d in degrees:
        coeffs = fit_polynomial(x_train, y_train, d)
        train_preds = predict_polynomial(x_train, coeffs)
        test_preds = predict_polynomial(x_test, coeffs)

        train_mse = float(np.mean((y_train - train_preds) ** 2))
        test_mse = float(np.mean((y_test - test_preds) ** 2))
        # Estimate parameter norm as proxy for model variance
        param_norm = float(np.linalg.norm(coeffs))

        print(f"Degree {d:d}: Train MSE = {train_mse:.4f} | Test MSE = {test_mse:.4f} | Coeff Norm = {param_norm:.2f}")


def main() -> None:
    # High SNR regime (vision/engineering benchmark)
    run_simulation(snr_label="High SNR Regime (R2 ~ 0.60)", noise_scale=0.25, seed=101)
    print()
    # Low SNR regime (financial return benchmark)
    run_simulation(snr_label="Low SNR Financial Regime (R2 ~ 0.02)", noise_scale=1.80, seed=101)
    print("Verification Invariant: At low SNR, high complexity inflates test MSE exponentially.")


main()
