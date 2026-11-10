"""Lab S6-L06-1: Sharp regression discontinuity and local linear bandwidth trade-offs.

SIMULATED: evaluates local linear RDD estimation of a known treatment jump at cutoff c=0,
demonstrating the bias-variance trade-off across varying bandwidths h.
"""

from __future__ import annotations

import random


def fit_local_linear(x: list[float], y: list[float], d: list[int]) -> float:
    """Fit local linear regression: Y = alpha + tau * D + beta_1 * X + beta_2 * (D * X).

    Returns estimated jump tau at the cutoff X=0.
    """
    n = len(x)
    # Design matrix columns: [1, D, X, D*X]
    # Solve 4x4 normal equations using Gauss-Jordan
    cols = [[1.0] * n, [float(di) for di in d], list(x), [float(di) * xi for di, xi in zip(d, x, strict=True)]]
    p = 4
    xtx = [[sum(cols[j][i] * cols[k][i] for i in range(n)) for k in range(p)] for j in range(p)]
    xty = [sum(cols[j][i] * y[i] for i in range(n)) for j in range(p)]

    aug = [xtx[i] + [xty[i]] for i in range(p)]
    for col in range(p):
        pivot = col
        while pivot < p and abs(aug[pivot][col]) < 1e-12:
            pivot += 1
        aug[col], aug[pivot] = aug[pivot], aug[col]

        piv_val = aug[col][col]
        for c in range(col, p + 1):
            aug[col][c] /= piv_val
        for r in range(p):
            if r != col and abs(aug[r][col]) > 1e-12:
                f = aug[r][col]
                for c in range(col, p + 1):
                    aug[r][c] -= f * aug[col][c]

    return aug[1][p]  # tau is coefficient on D (column 1)


def main() -> None:
    rng = random.Random(888)
    n = 6000

    # True parameters
    cutoff = 0.0
    true_tau = 3.50

    # Running variable X ~ Uniform[-2.5, 2.5]
    x = [rng.uniform(-2.5, 2.5) for _ in range(n)]

    # Potential outcomes with nonlinear curvature: Y(0) = 2.0 + 1.2*X + 0.8*X^2 + noise
    # At cutoff X=0, E[Y(0)|X=0] = 2.0, E[Y(1)|X=0] = 2.0 + 3.5 = 5.5
    y: list[float] = []
    d: list[int] = []
    for xi in x:
        di = 1 if xi >= cutoff else 0
        eps = rng.gauss(0.0, 0.6)
        baseline = 2.0 + 1.2 * xi + 0.8 * (xi**2) + eps
        val = baseline + true_tau * di
        y.append(val)
        d.append(di)

    bandwidths = [0.40, 0.75, 1.25, 2.00]

    print("Sharp Regression Discontinuity Local Linear Estimation (SIMULATED):")
    print(f"  Total observations N: {n}")
    print(f"  Cutoff threshold c:   {cutoff:.1f}")
    print(f"  True causal jump tau: {true_tau:.4f}\n")
    print("Bandwidth Sensitivity & Bias Analysis:")
    print("  Bandwidth (h) | Window Obs (N_h) | Estimated Jump (tau_hat) | Bias vs True Jump")
    print("  --------------+------------------+--------------------------+------------------")

    for h in bandwidths:
        # Filter observations in [cutoff - h, cutoff + h]
        idx = [i for i in range(n) if abs(x[i] - cutoff) <= h]
        sub_x = [x[i] for i in idx]
        sub_y = [y[i] for i in idx]
        sub_d = [d[i] for i in idx]

        tau_hat = fit_local_linear(sub_x, sub_y, sub_d)
        bias = tau_hat - true_tau

        print(f"      {h:4.2f}      |       {len(idx):4d}       |          {tau_hat:6.4f}          |     {bias:+6.4f}")


main()
