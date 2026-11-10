"""Lab FI2-L08-1: Information matrix condition number and parameter identification diagnostics.

SIMULATED: computes the numerical Hessian of the Kalman log-likelihood for a 3-factor Gaussian
affine model at the calibration optimum, evaluates the Fisher information matrix, calculates its
condition number, and identifies well-determined versus ill-determined parameter directions.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np


def compute_numerical_hessian(
    f: Callable[[np.ndarray], float],
    x0: np.ndarray,
    eps: float = 1e-4,
) -> np.ndarray:
    """Compute central difference Hessian matrix."""
    n = len(x0)
    hessian = np.zeros((n, n), dtype=np.float64)
    f0 = f(x0)

    # Diagonal elements: (f(x+h) - 2f(x) + f(x-h)) / h^2
    for i in range(n):
        dx_i = np.zeros(n, dtype=np.float64)
        dx_i[i] = eps
        f_plus = f(x0 + dx_i)
        f_minus = f(x0 - dx_i)
        hessian[i, i] = (f_plus - 2.0 * f0 + f_minus) / (eps**2)

    # Off-diagonal elements: (f(x+hi+hj) - f(x+hi-hj) - f(x-hi+hj) + f(x-hi-hj)) / (4*h^2)
    for i in range(n):
        for j in range(i + 1, n):
            dx_i = np.zeros(n, dtype=np.float64)
            dx_j = np.zeros(n, dtype=np.float64)
            dx_i[i] = eps
            dx_j[j] = eps

            f_pp = f(x0 + dx_i + dx_j)
            f_pm = f(x0 + dx_i - dx_j)
            f_mp = f(x0 - dx_i + dx_j)
            f_mm = f(x0 - dx_i - dx_j)

            val = (f_pp - f_pm - f_mp + f_mm) / (4.0 * eps * eps)
            hessian[i, j] = val
            hessian[j, i] = val

    return hessian


def main() -> None:
    # 3 key parameters for diagnostic analysis: [delta0, kappa1, sigma1]
    param_names = ["delta0 (short-rate baseline)", "kappa1 (level persistence)", "sigma1 (level vol)"]
    theta_star = np.array([0.025, 0.060, 0.012], dtype=np.float64)

    # Model negative log-likelihood surrogate near optimum (quadratic bowl with ill-conditioned curvature)
    # Empirical reality: level variance is tightly identified while persistence kappa is weakly identified
    # true curvature matrix:
    true_curvature = np.array(
        [
            [1.2e7, 1.5e5, -2.0e5],
            [1.5e5, 4.5e4, -1.0e4],
            [-2.0e5, -1.0e4, 8.5e6],
        ],
        dtype=np.float64,
    )

    def neg_log_likelihood(p: np.ndarray) -> float:
        dp = p - theta_star
        return float(0.5 * dp @ true_curvature @ dp + 1450.0)

    hess = compute_numerical_hessian(neg_log_likelihood, theta_star, eps=1e-4)
    eigvals, eigvecs = np.linalg.eigh(hess)

    # Condition number: ratio of maximum to minimum eigenvalue
    cond_number = float(eigvals[-1] / eigvals[0])
    asymptotic_cov = np.linalg.inv(hess)
    asymptotic_se = np.sqrt(np.diag(asymptotic_cov))

    print("SIMULATED ATSM Parameter Identification Diagnostics (Information Matrix Analysis):")
    print(f"  Calibrated parameters: {theta_star.tolist()}")
    print(f"  Observed Information Matrix Condition Number: {cond_number:.2e}")
    print("\nEigenvalue Decomposition of Information Matrix (Curvature Spectrum):")
    for idx, (val, vec) in enumerate(zip(eigvals, eigvecs.T, strict=True)):
        print(f"  Mode {idx + 1}: Eigenvalue = {val:10.2e}, Eigenvector = {[round(float(v), 3) for v in vec]}")

    print("\nAsymptotic Parameter Precision (Cramer-Rao Lower Bound):")
    print("Parameter                     | Estimate | Asymptotic SE | t-stat")
    print("-" * 65)
    for name, est, se in zip(param_names, theta_star, asymptotic_se, strict=True):
        t_stat = est / se
        print(f"  {name:27s} | {est:8.4f} |   {se:9.6f}   | {t_stat:6.2f}")


main()
